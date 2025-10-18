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
        self.system_prompt = """You are a technical interviewer conducting a coding interview. Be CONCISE and helpful.

Your role:
1. Guide candidates through problem-solving
2. Provide brief hints when stuck
3. Ask clarifying questions
4. Give constructive feedback

Keep responses short (2-3 sentences max). Be encouraging but don't give away solutions."""

    def get_initial_greeting(self) -> str:
        """Get the initial greeting message from the AI."""
        return """Hi! I'm your AI interviewer. Let's start!

**Difficulty:** Easy, Medium, or Hard?
**Topic:** Arrays, Strings, Trees, Graphs, DP, etc.

Tell me both and I'll pick a problem for you!"""

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
        
        print(f"AI Agent: Selecting problem with difficulty={difficulty}, topics={topics}")
        
        # Get problems this user has already been given
        user_problems = UserProblem.objects.filter(user=session.user)
        exclude_ids = [up.problem.leetcode_id for up in user_problems if up.problem.leetcode_id]
        print(f"AI Agent: Excluding {len(exclude_ids)} previously assigned problems")
        
        # Get a random problem from LeetCode
        topic = topics[0] if topics else None
        leetcode_problem = leetcode_service.get_random_problem(
            difficulty=difficulty,
            topic=topic,
            exclude_ids=exclude_ids
        )
        
        if not leetcode_problem:
            print("AI Agent: No problem found from LeetCode service")
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
        return f"""Perfect! Here's your {problem.difficulty} problem: **{problem.title}**

Read the details in the left panel. What's your approach?"""

    def provide_guidance(self, user_message: str, session: InterviewSession, current_code: str = "") -> str:
        """Provide guidance based on user's current progress."""
        problem = session.problem
        if not problem:
            return "No problem selected yet. Let's start!"
        
        # Get recent chat history for context (limit to last 5 messages)
        recent_messages = ChatMessage.objects.filter(session=session).order_by('-timestamp')[:5]
        chat_history = []
        for msg in recent_messages:
            role = "user" if msg.message_type == "user" else "assistant"
            chat_history.append({"role": role, "content": msg.content})
        
        # Reverse to get chronological order
        chat_history.reverse()
        
        # Build concise context for the AI
        context = f"""Coding interview coach. Be CONCISE and helpful.

Problem: {problem.title}
User: {user_message}
Code: {current_code[:150] if current_code else "None"}

Give brief guidance. Max 2-3 sentences. Ask one clarifying question."""
        
        prompt = f"{self.system_prompt}\n\n{context}"
        
        response = self.client.chat.completions.create(
            prompt=prompt,
            model="hermes",
            temperature=0.5,
            is_stream=False
        )
        
        return response.choices[0].message.content

    def provide_hint(self, session: InterviewSession, hint_level: int = 1) -> str:
        """Provide a progressive hint for the current problem."""
        problem = session.problem
        if not problem or not problem.hints:
            return "No specific hints available. What's your current approach?"
        
        # Get hint based on level (1-indexed)
        hint_index = min(hint_level - 1, len(problem.hints) - 1)
        hint = problem.hints[hint_index]
        
        return f"Hint: {hint}"

    def analyze_code(self, code: str, session: InterviewSession, test_results: dict = None) -> str:
        """Analyze the user's code and provide feedback."""
        problem = session.problem
        if not problem:
            return "No problem to compare against."
        
        # Build test results context if available
        test_context = ""
        if test_results:
            passed = test_results.get('passed', 0)
            total = test_results.get('total', 0)
            test_context = f" Tests: {passed}/{total} passed."
        
        context = f"""Code review for: {problem.title}

Code:
{code[:300]}{test_context}

Give brief feedback on correctness, complexity, and improvements. Max 3 sentences."""
        
        prompt = f"Technical interviewer. Be CONCISE and helpful.\n\n{context}"
        
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
