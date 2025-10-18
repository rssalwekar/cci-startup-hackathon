import requests
import json
import re
from typing import List, Dict, Optional
from django.conf import settings


class LeetCodeService:
    """Service to interact with LeetCode API and fetch problems"""
    
    BASE_URL = "https://leetcode.com"
    GRAPHQL_URL = f"{BASE_URL}/graphql"
    
    # GraphQL query to get problems
    PROBLEMS_QUERY = """
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
        problemsetQuestionList: questionList(
            categorySlug: $categorySlug
            limit: $limit
            skip: $skip
            filters: $filters
        ) {
            total: totalNum
            questions: data {
                acRate
                difficulty
                freqBar
                frontendQuestionId: questionFrontendId
                isFavor
                paidOnly: isPaidOnly
                status
                title
                titleSlug
                topicTags {
                    name
                    id
                    slug
                }
                hasSolution
                hasVideoSolution
            }
        }
    }
    """
    
    # GraphQL query to get problem details
    PROBLEM_DETAILS_QUERY = """
    query questionContent($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            content
            mysqlSchemas
            dataSchemas
        }
    }
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })
    
    def get_problems(self, difficulty: str = None, topic: str = None, limit: int = 50) -> List[Dict]:
        """Get list of problems from LeetCode"""
        try:
            filters = {}
            if difficulty:
                difficulty_map = {'easy': 'EASY', 'medium': 'MEDIUM', 'hard': 'HARD'}
                filters['difficulty'] = difficulty_map.get(difficulty.lower())
            
            variables = {
                'categorySlug': '',
                'limit': limit,
                'skip': 0,
                'filters': filters
            }
            
            response = self.session.post(
                self.GRAPHQL_URL,
                json={'query': self.PROBLEMS_QUERY, 'variables': variables}
            )
            
            if response.status_code == 200:
                data = response.json()
                questions = data.get('data', {}).get('problemsetQuestionList', {}).get('questions', [])
                
                # Filter out paid-only problems
                questions = [q for q in questions if not q.get('paidOnly', False)]
                
                # Filter by topic if specified
                if topic:
                    topic_lower = topic.lower()
                    questions = [q for q in questions if any(
                        topic_lower in tag.get('slug', '').lower() or 
                        topic_lower in tag.get('name', '').lower()
                        for tag in q.get('topicTags', [])
                    )]
                
                return questions
            else:
                print(f"Error fetching problems: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Exception in get_problems: {e}")
            return []
    
    def get_problem_details(self, title_slug: str) -> Optional[Dict]:
        """Get detailed problem content from LeetCode"""
        try:
            variables = {'titleSlug': title_slug}
            
            response = self.session.post(
                self.GRAPHQL_URL,
                json={'query': self.PROBLEM_DETAILS_QUERY, 'variables': variables}
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', {}).get('question', {})
            else:
                print(f"Error fetching problem details: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Exception in get_problem_details: {e}")
            return None
    
    def parse_problem_content(self, content: str) -> Dict:
        """Parse LeetCode problem content to extract structured data with proper formatting"""
        if not content:
            return {}
        
        # Extract examples using multiple regex patterns
        examples = []
        
        # Try different patterns for examples
        example_patterns = [
            # Pattern 1: <strong>Example X:</strong> with <pre> blocks
            r'<strong>Example\s*(\d+):</strong>.*?<pre>.*?<strong>Input:</strong>\s*(.*?)<strong>Output:</strong>\s*(.*?)(?:<strong>Explanation:</strong>\s*(.*?))?</pre>',
            # Pattern 2: <b>Example X:</b> with <pre> blocks  
            r'<b>Example\s*(\d+):</b>.*?<pre>.*?<b>Input:</b>\s*(.*?)<b>Output:</b>\s*(.*?)(?:<b>Explanation:</b>\s*(.*?))?</pre>',
            # Pattern 3: Plain text examples without <pre>
            r'<strong>Example\s*(\d+):</strong>.*?<strong>Input:</strong>\s*(.*?)<strong>Output:</strong>\s*(.*?)(?:<strong>Explanation:</strong>\s*(.*?))?(?=<strong>Example|$)',
            # Pattern 4: More flexible pattern
            r'Example\s*(\d+):.*?Input:\s*(.*?)Output:\s*(.*?)(?:Explanation:\s*(.*?))?(?=Example|\Z)'
        ]
        
        for pattern in example_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            if matches:
                for match in matches:
                    example_num = match[0]
                    input_text = self._clean_html_text(match[1])
                    output_text = self._clean_html_text(match[2])
                    explanation = self._clean_html_text(match[3]) if match[3] else None
                    
                    examples.append({
                        'input': input_text,
                        'output': output_text,
                        'explanation': explanation
                    })
                break  # Use first pattern that finds matches
        
        # Extract constraints using multiple patterns
        constraints = ""
        constraints_patterns = [
            r'<strong>Constraints:</strong>(.*?)(?:<p>|<br>|$)',
            r'<b>Constraints:</b>(.*?)(?:<p>|<br>|$)',
            r'Constraints:(.*?)(?:<p>|<br>|$)'
        ]
        
        for pattern in constraints_patterns:
            constraints_match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if constraints_match:
                constraints = self._clean_html_text(constraints_match.group(1))
                break
        
        # Extract the main description by removing examples and constraints
        description = content
        
        # Remove all example patterns from description
        for pattern in example_patterns:
            description = re.sub(pattern, '', description, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove constraints from description
        for pattern in constraints_patterns:
            description = re.sub(pattern, '', description, flags=re.DOTALL | re.IGNORECASE)
        
        # Clean up the description while preserving some formatting
        description = self._clean_html_text(description)
        
        return {
            'description': description,
            'constraints': constraints,
            'examples': examples
        }
    
    def _clean_html_text(self, text: str) -> str:
        """Clean HTML text while preserving important formatting"""
        if not text:
            return ""
        
        import html
        
        # Decode HTML entities first
        text = html.unescape(text)
        
        # Preserve line breaks and paragraphs
        text = re.sub(r'<br\s*/?>', '\n', text)
        text = re.sub(r'<p[^>]*>', '\n', text)
        text = re.sub(r'</p>', '\n', text)
        
        # Remove other HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Clean up whitespace but preserve structure
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Multiple newlines to double newlines
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces to single space
        text = text.strip()
        
        return text
    
    def get_random_problem(self, difficulty: str = None, topic: str = None, exclude_ids: List[int] = None) -> Optional[Dict]:
        """Get a random problem matching criteria"""
        print(f"Getting random problem with difficulty={difficulty}, topic={topic}, exclude_ids={exclude_ids}")
        
        problems = self.get_problems(difficulty=difficulty, topic=topic, limit=100)
        print(f"Found {len(problems)} problems from LeetCode API")
        
        if not problems:
            print("No problems found, trying without topic filter...")
            # Try without topic filter if no problems found
            problems = self.get_problems(difficulty=difficulty, topic=None, limit=100)
            print(f"Found {len(problems)} problems without topic filter")
        
        if not problems:
            print("Still no problems found, trying with any difficulty...")
            # Try with any difficulty if still no problems
            problems = self.get_problems(difficulty=None, topic=topic, limit=100)
            print(f"Found {len(problems)} problems with any difficulty")
        
        if not problems:
            print("No problems found at all, returning None")
            return None
        
        # Filter out excluded problems
        if exclude_ids:
            original_count = len(problems)
            problems = [p for p in problems if p.get('frontendQuestionId') not in exclude_ids]
            print(f"Filtered out excluded problems: {original_count} -> {len(problems)}")
        
        if not problems:
            print("All problems were excluded, returning None")
            return None
        
        # Return a random problem
        import random
        selected = random.choice(problems)
        print(f"Selected problem: {selected.get('title', 'Unknown')} (ID: {selected.get('frontendQuestionId', 'Unknown')})")
        return selected


# Global instance
leetcode_service = LeetCodeService()
