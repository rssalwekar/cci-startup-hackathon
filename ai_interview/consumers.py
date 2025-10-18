import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import InterviewSession, ChatMessage, CodeSubmission
from .ai_agent import AIInterviewAgent


class InterviewConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ai_agent = AIInterviewAgent()
        self.session_id = None
        self.session = None

    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.session = await self.get_session(self.session_id)
        
        if not self.session:
            await self.close()
            return
        
        # Join session group
        await self.channel_layer.group_add(
            f"session_{self.session_id}",
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial greeting if this is a new session
        if self.session.status == 'preparing':
            greeting = self.ai_agent.get_initial_greeting()
            await self.send_ai_message(greeting)

    async def disconnect(self, close_code):
        # Leave session group
        if self.session_id:
            await self.channel_layer.group_discard(
                f"session_{self.session_id}",
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'chat_message':
                await self.handle_chat_message(data)
            elif message_type == 'code_submission':
                await self.handle_code_submission(data)
            elif message_type == 'request_hint':
                await self.handle_hint_request(data)
            elif message_type == 'analyze_code':
                await self.handle_code_analysis(data)
            elif message_type == 'end_interview':
                await self.handle_end_interview(data)
                
        except json.JSONDecodeError:
            await self.send_error("Invalid JSON data")
        except Exception as e:
            await self.send_error(f"Error processing message: {str(e)}")

    async def handle_chat_message(self, data):
        """Handle incoming chat messages from the user."""
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return
        
        # Save user message
        await self.save_message('user', user_message)
        
        # Send user message to group
        await self.channel_layer.group_send(
            f"session_{self.session_id}",
            {
                'type': 'chat_message',
                'message': user_message,
                'sender': 'user'
            }
        )
        
        # Process with AI agent
        await self.process_with_ai(user_message)

    async def handle_code_submission(self, data):
        """Handle code submissions from the IDE."""
        code = data.get('code', '')
        language = data.get('language', 'python')
        test_results = data.get('testResults', {})
        
        if not code.strip():
            return
        
        # Save code submission
        await self.save_code_submission(code, language)
        
        # Analyze code with AI (include test results if available)
        analysis = await self.analyze_code_async(code, test_results)
        await self.send_ai_message(analysis)
        
        # Send code to group
        await self.channel_layer.group_send(
            f"session_{self.session_id}",
            {
                'type': 'code_submission',
                'code': code,
                'language': language,
                'testResults': test_results
            }
        )

    async def handle_hint_request(self, data):
        """Handle requests for hints."""
        hint_level = data.get('hint_level', 1)
        hint = await self.provide_hint_async(hint_level)
        await self.send_ai_message(hint)

    async def handle_code_analysis(self, data):
        """Handle requests for code analysis."""
        code = data.get('code', '')
        if not code.strip():
            await self.send_error("No code provided for analysis")
            return
        
        analysis = await self.analyze_code_async(code)
        await self.send_ai_message(analysis)

    async def handle_end_interview(self, data):
        """Handle end interview request."""
        # Update session status
        await self.update_session('completed')
        
        # Send final message
        await self.send_ai_message("Thank you for the interview! Your session has been completed. You can now return to the home page.")
        
        # Close the WebSocket connection
        await self.close()

    async def process_with_ai(self, user_message):
        """Process user message with AI agent."""
        try:
            # Check if we need to select a problem
            if self.session.status == 'preparing' and not self.session.problem:
                # Try to extract preferences from user message
                await self.extract_preferences(user_message)
                
                # Check if we have both difficulty and topic preferences
                has_difficulty = bool(self.session.difficulty_preference)
                has_topics = bool(self.session.topic_preferences)
                
                if not has_difficulty or not has_topics:
                    # Ask for missing preferences
                    missing = []
                    if not has_difficulty:
                        missing.append("difficulty level (easy, medium, or hard)")
                    if not has_topics:
                        missing.append("topic(s) you'd like to work on")
                    
                    await self.send_ai_message(f"I'd like to make sure I select the perfect problem for you. Could you please specify your preferred {' and '.join(missing)}?")
                    return
                
                # We have both preferences, select and present problem
                problem = await self.select_problem_async()
                if problem:
                    await self.update_session_problem(problem)
                    problem_message = await self.present_problem_async(problem)
                    await self.send_ai_message(problem_message)
                else:
                    await self.send_ai_message("I'm sorry, I couldn't find a suitable problem with those preferences. Let me try with different criteria.")
            else:
                # Provide guidance for the current problem
                current_code = await self.get_latest_code()
                guidance = await self.provide_guidance_async(user_message, current_code)
                await self.send_ai_message(guidance)
                
        except Exception as e:
            await self.send_error(f"Error processing with AI: {str(e)}")

    async def extract_preferences(self, user_message):
        """Extract difficulty and topic preferences from user message."""
        # Simple keyword matching for now - could be enhanced with NLP
        user_message_lower = user_message.lower()
        
        # Extract difficulty preference
        if 'easy' in user_message_lower:
            self.session.difficulty_preference = 'easy'
        elif 'medium' in user_message_lower:
            self.session.difficulty_preference = 'medium'
        elif 'hard' in user_message_lower:
            self.session.difficulty_preference = 'hard'
        
        # Extract topic preferences with more comprehensive mapping
        topics = []
        topic_keywords = {
            'array': 'arrays',
            'arrays': 'arrays',
            'string': 'strings',
            'strings': 'strings',
            'tree': 'trees',
            'trees': 'trees',
            'graph': 'graphs',
            'graphs': 'graphs',
            'dynamic programming': 'dynamic-programming',
            'dp': 'dynamic-programming',
            'binary search': 'binary-search',
            'two pointer': 'two-pointers',
            'two pointers': 'two-pointers',
            'sliding window': 'sliding-window',
            'hash': 'hash-table',
            'hash table': 'hash-table',
            'hash tables': 'hash-table',
            'stack': 'stack',
            'stacks': 'stack',
            'queue': 'queue',
            'queues': 'queue',
            'linked list': 'linked-list',
            'linked lists': 'linked-list',
            'recursion': 'recursion',
            'backtracking': 'backtracking',
            'greedy': 'greedy',
            'sorting': 'sorting',
            'heap': 'heap',
            'trie': 'trie',
            'union find': 'union-find',
            'segment tree': 'segment-tree',
            'fenwick tree': 'fenwick-tree'
        }
        
        for keyword, topic in topic_keywords.items():
            if keyword in user_message_lower:
                if topic not in topics:  # Avoid duplicates
                    topics.append(topic)
        
        if topics:
            self.session.topic_preferences = topics
        
        await self.update_session()

    async def send_ai_message(self, message):
        """Send a message from the AI."""
        # Save AI message
        await self.save_message('ai', message)
        
        # Send to group
        await self.channel_layer.group_send(
            f"session_{self.session_id}",
            {
                'type': 'chat_message',
                'message': message,
                'sender': 'ai'
            }
        )

    async def send_error(self, error_message):
        """Send an error message."""
        await self.channel_layer.group_send(
            f"session_{self.session_id}",
            {
                'type': 'error_message',
                'message': error_message
            }
        )

    # WebSocket event handlers
    async def chat_message(self, event):
        """Handle chat message events."""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender': event['sender']
        }))

    async def code_submission(self, event):
        """Handle code submission events."""
        await self.send(text_data=json.dumps({
            'type': 'code_submission',
            'code': event['code'],
            'language': event['language']
        }))

    async def error_message(self, event):
        """Handle error message events."""
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': event['message']
        }))

    # Database operations
    @database_sync_to_async
    def get_session(self, session_id):
        try:
            return InterviewSession.objects.get(id=session_id)
        except InterviewSession.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, message_type, content):
        ChatMessage.objects.create(
            session=self.session,
            message_type=message_type,
            content=content
        )

    @database_sync_to_async
    def save_code_submission(self, code, language):
        CodeSubmission.objects.create(
            session=self.session,
            code=code,
            language=language
        )

    @database_sync_to_async
    def update_session(self):
        self.session.save()

    @database_sync_to_async
    def get_latest_code(self):
        latest_submission = self.session.code_submissions.order_by('-timestamp').first()
        return latest_submission.code if latest_submission else ""

    @database_sync_to_async
    def select_problem_async(self):
        """Async wrapper for AI agent problem selection."""
        return self.ai_agent.select_problem(self.session)

    @database_sync_to_async
    def present_problem_async(self, problem):
        """Async wrapper for AI agent problem presentation."""
        return self.ai_agent.present_problem(problem)

    @database_sync_to_async
    def provide_guidance_async(self, user_message, current_code):
        """Async wrapper for AI agent guidance."""
        return self.ai_agent.provide_guidance(user_message, self.session, current_code)

    @database_sync_to_async
    def update_session_problem(self, problem):
        """Update session with selected problem."""
        self.session.problem = problem
        self.session.status = 'active'
        self.session.save()

    @database_sync_to_async
    def provide_hint_async(self, hint_level):
        """Async wrapper for AI agent hint provision."""
        return self.ai_agent.provide_hint(self.session, hint_level)

    @database_sync_to_async
    def analyze_code_async(self, code, test_results=None):
        """Async wrapper for AI agent code analysis."""
        return self.ai_agent.analyze_code(code, self.session, test_results)

