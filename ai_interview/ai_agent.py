from kronoslabs import KronosLabs
import json
import random
from typing import List, Dict, Optional
from django.conf import settings
from .models import Problem, InterviewSession, ChatMessage, UserProblem
from .leetcode_service import leetcode_service


class AIInterviewAgent:
    def __init__(self):
        self.client = KronosLabs(api_key=settings.KRONOS_API_KEY)
        self.system_prompt = """You are an experienced technical interviewer conducting a coding interview. Your role is to:

1. Assess the candidate's skill level through conversation
2. Select an appropriate LeetCode-style problem based on their preferences
3. Guide the candidate through the problem-solving process
4. Provide hints when they get stuck, but let them lead the solution
5. Ask clarifying questions about their approach
6. Give constructive feedback

Be encouraging, professional, and helpful. Don't give away the solution directly - guide them to discover it themselves."""

    def get_initial_greeting(self) -> str:
        """Get the initial greeting message from the AI."""
        return "Hello! I'm your AI interviewer today. I'm excited to conduct this coding interview with you. Let's start by getting to know your coding background and preferences. What difficulty level would you like to work on today - easy, medium, or hard?"

    def assess_skill_level(self, user_message: str, session: InterviewSession) -> str:
        """Assess user's skill level and preferences based on their message."""
        prompt = f"{self.system_prompt}\n\nUser said: {user_message}. Please respond appropriately to assess their skill level and preferences."
        
        response = self.client.chat.completions.create(
            prompt=prompt,
            model="hermes",
            temperature=0.7,
            is_stream=False
        )
        
        return response.choices[0].message.content

    def select_problem(self, session: InterviewSession) -> Optional[Problem]:
        """Select an appropriate problem from LeetCode based on user preferences."""
        difficulty = session.difficulty_preference or 'medium'
        topics = session.topic_preferences or []
        
        # Get problems this user has already been given
        user_problems = UserProblem.objects.filter(user=session.user)
        exclude_ids = [up.problem.leetcode_id for up in user_problems if up.problem.leetcode_id]
        
        # Get a random problem from LeetCode
        topic = topics[0] if topics else None
        leetcode_problem = leetcode_service.get_random_problem(
            difficulty=difficulty,
            topic=topic,
            exclude_ids=exclude_ids
        )
        
        if not leetcode_problem:
            return None
        
        # Check if we already have this problem in our database
        problem = Problem.objects.filter(leetcode_id=leetcode_problem['frontendQuestionId']).first()
        
        if not problem:
            # Fetch detailed problem content
            details = leetcode_service.get_problem_details(leetcode_problem['titleSlug'])
            if not details:
                return None
            
            # Parse the content
            parsed_content = leetcode_service.parse_problem_content(details.get('content', ''))
            
            # Create new problem in database
            problem = Problem.objects.create(
                leetcode_id=leetcode_problem['frontendQuestionId'],
                title_slug=leetcode_problem['titleSlug'],
                title=leetcode_problem['title'],
                description=parsed_content.get('description', ''),
                difficulty=leetcode_problem['difficulty'].lower(),
                topics=[tag['slug'] for tag in leetcode_problem.get('topicTags', [])],
                constraints=parsed_content.get('constraints', ''),
                examples=parsed_content.get('examples', [])
            )
        
        # Record that this user has been given this problem
        UserProblem.objects.get_or_create(
            user=session.user,
            problem=problem,
            session=session
        )
        
        return problem

    def present_problem(self, problem: Problem) -> str:
        """Present the problem to the user."""
        message = f"""Great! I've selected a {problem.difficulty} problem for you: **{problem.title}**

The problem details are now displayed in the problem window on the left. Take your time to read through the problem description, constraints, and examples.

When you're ready, let me know your approach or if you have any questions about the problem!"""
        
        return message

    def provide_guidance(self, user_message: str, session: InterviewSession, current_code: str = "") -> str:
        """Provide guidance based on user's current progress."""
        problem = session.problem
        if not problem:
            return "I don't have a problem selected yet. Let me help you get started."
        
        # Get recent chat history for context
        recent_messages = ChatMessage.objects.filter(session=session).order_by('-timestamp')[:10]
        chat_history = []
        for msg in recent_messages:
            role = "user" if msg.message_type == "user" else "assistant"
            chat_history.append({"role": role, "content": msg.content})
        
        # Reverse to get chronological order
        chat_history.reverse()
        
        # Build context for the AI
        context = f"""You are conducting a coding interview. The current problem is:

**{problem.title}**
{problem.description}

The user's current code:
```python
{current_code}
```

Recent conversation:
{json.dumps(chat_history, indent=2)}

User's latest message: {user_message}

Provide helpful guidance without giving away the solution. Ask clarifying questions, suggest approaches, or provide hints if they seem stuck."""
        
        prompt = f"{self.system_prompt}\n\n{context}"
        
        response = self.client.chat.completions.create(
            prompt=prompt,
            model="hermes",
            temperature=0.7,
            is_stream=False
        )
        
        return response.choices[0].message.content

    def provide_hint(self, session: InterviewSession, hint_level: int = 1) -> str:
        """Provide a progressive hint for the current problem."""
        problem = session.problem
        if not problem or not problem.hints:
            return "I don't have specific hints for this problem, but I can help guide you through your approach. What are you thinking so far?"
        
        # Get hint based on level (1-indexed)
        hint_index = min(hint_level - 1, len(problem.hints) - 1)
        hint = problem.hints[hint_index]
        
        return f"Here's a hint to help you along: {hint}"

    def analyze_code(self, code: str, session: InterviewSession) -> str:
        """Analyze the user's code and provide feedback."""
        problem = session.problem
        if not problem:
            return "I don't have a problem to compare your code against."
        
        context = f"""Analyze this code for the problem: {problem.title}

Problem description: {problem.description}

User's code:
```python
{code}
```

Provide constructive feedback on:
1. Correctness of the approach
2. Time/space complexity
3. Code quality and style
4. Potential improvements
5. Whether it solves the problem

Be encouraging but honest. Don't give away the solution if it's incorrect."""
        
        prompt = f"You are a technical interviewer providing code review feedback. Be constructive and educational.\n\n{context}"
        
        response = self.client.chat.completions.create(
            prompt=prompt,
            model="hermes",
            temperature=0.5,
            is_stream=False
        )
        
        return response.choices[0].message.content

    def generate_feedback(self, session: InterviewSession) -> str:
        """Generate comprehensive feedback for the completed interview."""
        # Get all messages and code submissions
        messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
        code_submissions = session.code_submissions.all().order_by('timestamp')
        
        # Build context for feedback generation
        conversation_summary = "Interview Conversation:\n"
        for msg in messages:
            conversation_summary += f"{msg.message_type.upper()}: {msg.content}\n"
        
        code_summary = "Code Submissions:\n"
        for submission in code_submissions:
            code_summary += f"Submission at {submission.timestamp}:\n{submission.code}\n\n"
        
        context = f"""Generate comprehensive interview feedback based on this coding interview session.

Problem: {session.problem.title if session.problem else 'No problem selected'}
Difficulty: {session.difficulty_preference}

{conversation_summary}

{code_summary}

Provide feedback on:
1. Problem-solving approach
2. Communication skills
3. Code quality
4. Areas of strength
5. Areas for improvement
6. Overall performance rating (1-10)
7. Specific recommendations for future practice

Be constructive, specific, and encouraging."""
        
        prompt = f"You are an experienced technical interviewer providing comprehensive feedback. Be detailed, constructive, and encouraging.\n\n{context}"
        
        response = self.client.chat.completions.create(
            prompt=prompt,
            model="hermes",
            temperature=0.5,
            is_stream=False
        )
        
        return response.choices[0].message.content
