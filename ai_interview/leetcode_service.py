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
            codeSnippets {
                lang
                langSlug
                code
            }
            exampleTestcases
            metaData
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
    
    def get_official_function_signature(self, title_slug: str) -> str:
        """Get the official Python function signature from LeetCode"""
        try:
            details = self.get_problem_details(title_slug)
            if not details:
                return ""
            
            # Get Python code snippet
            code_snippets = details.get('codeSnippets', [])
            python_snippet = None
            
            for snippet in code_snippets:
                if snippet.get('langSlug') == 'python3' or snippet.get('lang') == 'Python3':
                    python_snippet = snippet.get('code', '')
                    break
            
            if python_snippet:
                print(f"Found official Python snippet for {title_slug}")
                return python_snippet
            else:
                print(f"No Python snippet found for {title_slug}")
                return ""
                
        except Exception as e:
            print(f"Exception getting official function signature: {e}")
            return ""
    
    def get_official_test_cases(self, title_slug: str) -> List[Dict]:
        """Get the official test cases from LeetCode"""
        try:
            details = self.get_problem_details(title_slug)
            if not details:
                return []
            
            # First try to get test cases from parsed content (more reliable)
            parsed_content = self.parse_problem_content(details.get('content', ''))
            examples = parsed_content.get('examples', [])
            
            if examples:
                test_cases = []
                for example in examples:
                    # Clean up the input and output
                    input_text = example.get('input', '').replace('columnNumber = ', '').strip()
                    output_text = example.get('output', '').strip()
                    
                    # Remove HTML tags and extra text from output
                    output_text = self._clean_html_text(output_text)
                    output_text = output_text.replace('"', '').strip()
                    
                    # Extract just the first line if there are multiple lines
                    if '\n' in output_text:
                        output_text = output_text.split('\n')[0].strip()
                    
                    # Remove any remaining HTML-like content (more aggressive)
                    output_text = re.sub(r'<[^>]*>', '', output_text).strip()
                    output_text = re.sub(r'&[a-zA-Z]+;', '', output_text)  # Remove HTML entities
                    
                    # Remove any text that looks like HTML attributes or classes
                    output_text = re.sub(r'<span[^>]*>', '', output_text)
                    output_text = re.sub(r'<div[^>]*>', '', output_text)
                    output_text = re.sub(r'<p[^>]*>', '', output_text)
                    output_text = re.sub(r'<strong[^>]*>', '', output_text)
                    output_text = re.sub(r'<em[^>]*>', '', output_text)
                    
                    # Clean up common formatting issues
                    output_text = re.sub(r'\s+', ' ', output_text)  # Normalize whitespace
                    output_text = output_text.strip()
                    
                    # Fix common boolean values
                    if output_text.lower() in ['true', 'false']:
                        output_text = output_text.capitalize()
                    
                    # Remove any remaining quotes if they're not part of the actual value
                    if output_text.startswith("'") and output_text.endswith("'"):
                        output_text = output_text[1:-1]
                    
                    # If the output still contains HTML-like content, try to extract just the value
                    if '<' in output_text or 'class=' in output_text:
                        # Try to extract just the boolean or numeric value
                        if 'true' in output_text.lower():
                            output_text = 'True'
                        elif 'false' in output_text.lower():
                            output_text = 'False'
                        elif re.search(r'\d+', output_text):
                            # Extract the first number found
                            number_match = re.search(r'\d+', output_text)
                            if number_match:
                                output_text = number_match.group()
                    
                    if input_text and output_text:
                        test_cases.append({
                            'input': input_text,
                            'expected': output_text
                        })
                
                if test_cases:
                    print(f"Found {len(test_cases)} test cases from parsed content for {title_slug}")
                    return test_cases
            
            # Fallback to exampleTestcases field if parsed content doesn't work
            example_testcases = details.get('exampleTestcases', '')
            if not example_testcases:
                return []
            
            # Parse the test cases string
            # LeetCode returns test cases as a newline-separated string
            # Format is usually: "input1\noutput1\ninput2\noutput2\n..."
            test_cases = []
            lines = example_testcases.strip().split('\n')
            
            for i in range(0, len(lines), 2):
                if i + 1 < len(lines):
                    input_line = lines[i].strip()
                    output_line = lines[i + 1].strip()
                    
                    test_cases.append({
                        'input': input_line,
                        'expected': output_line
                    })
            
            print(f"Found {len(test_cases)} official test cases from exampleTestcases for {title_slug}")
            return test_cases
            
        except Exception as e:
            print(f"Exception getting official test cases: {e}")
            return []
    
    def parse_problem_content(self, content: str) -> Dict:
        """Parse LeetCode problem content to extract structured data with proper formatting"""
        if not content:
            return {}
        
        # Extract examples using multiple regex patterns
        examples = []
        
        # Try different patterns for examples (ordered by specificity)
        example_patterns = [
            # Pattern 1: Handle the new LeetCode format with example-block divs (most specific)
            r'<strong class="example">Example\s*(\d+):</strong>.*?<div class="example-block">.*?<strong>Input:</strong>\s*<span[^>]*>(.*?)</span>.*?<strong>Output:</strong>\s*<span[^>]*>(.*?)</span>.*?</div>',
            # Pattern 2: <strong>Example X:</strong> with <pre> blocks
            r'<strong>Example\s*(\d+):</strong>.*?<pre>.*?<strong>Input:</strong>\s*(.*?)<strong>Output:</strong>\s*(.*?)(?:<strong>Explanation:</strong>\s*(.*?))?</pre>',
            # Pattern 3: <b>Example X:</b> with <pre> blocks  
            r'<b>Example\s*(\d+):</b>.*?<pre>.*?<b>Input:</b>\s*(.*?)<b>Output:</b>\s*(.*?)(?:<b>Explanation:</b>\s*(.*?))?</pre>',
            # Pattern 4: Plain text examples without <pre>
            r'<strong>Example\s*(\d+):</strong>.*?<strong>Input:</strong>\s*(.*?)<strong>Output:</strong>\s*(.*?)(?:<strong>Explanation:</strong>\s*(.*?))?(?=<strong>Example|$)',
            # Pattern 5: More flexible pattern
            r'Example\s*(\d+):.*?Input:\s*(.*?)Output:\s*(.*?)(?:Explanation:\s*(.*?))?(?=Example|\Z)',
            # Pattern 6: Handle cases where output might be in different format
            r'<strong>Example\s*(\d+):</strong>.*?<strong>Input:</strong>\s*(.*?)<strong>Output:</strong>\s*(.*?)(?=<strong>Example|$)',
            # Pattern 7: Handle cases with different HTML structure
            r'<b>Example\s*(\d+):</b>.*?<b>Input:</b>\s*(.*?)<b>Output:</b>\s*(.*?)(?=<b>Example|$)'
        ]
        
        for pattern in example_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            if matches:
                for match in matches:
                    example_num = match[0]
                    input_text = self._clean_html_text(match[1])
                    output_text = self._clean_html_text(match[2])
                    explanation = self._clean_html_text(match[3]) if len(match) > 3 and match[3] else None
                    
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
    
    def extract_function_signature(self, content: str, title: str) -> str:
        """Extract function signature from LeetCode problem content"""
        if not content:
            return self._generate_generic_signature(title)
        
        # Try to find function signature in the content
        # Look for common patterns like "def functionName(" or "public int functionName("
        signature_patterns = [
            r'def\s+(\w+)\s*\([^)]*\)\s*:',
            r'public\s+\w+\s+(\w+)\s*\([^)]*\)',
            r'int\s+(\w+)\s*\([^)]*\)',
            r'string\s+(\w+)\s*\([^)]*\)',
            r'bool\s+(\w+)\s*\([^)]*\)',
            r'List<.*?>\s+(\w+)\s*\([^)]*\)'
        ]
        
        for pattern in signature_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                function_name = match.group(1)
                return self._generate_python_signature(function_name, content)
        
        # If no signature found, generate based on title
        return self._generate_generic_signature(title)
    
    def _generate_python_signature(self, function_name: str, content: str) -> str:
        """Generate Python function signature based on function name and content"""
        # Try to extract parameter types from content
        params = self._extract_parameters(content)
        
        # Generate the signature
        signature = f"class Solution(object):\n    def {function_name}(self"
        
        if params:
            signature += f", {', '.join(params)}"
        
        signature += "):\n        \"\"\"\n"
        
        # Add type hints based on parameters and content analysis
        for param in params:
            param_type = self._infer_parameter_type(param, content)
            signature += f"        :type {param}: {param_type}\n"
        
        # Infer return type from content
        return_type = self._infer_return_type(content)
        signature += f"        :rtype: {return_type}\n        \"\"\"\n        # Your code here\n        pass"
        
        return signature
    
    def _infer_parameter_type(self, param: str, content: str) -> str:
        """Infer parameter type from parameter name and content"""
        param_lower = param.lower()
        content_lower = content.lower()
        
        if param_lower in ['nums', 'digits', 'arr', 'array'] or 'list' in content_lower:
            return 'List[int]'
        elif param_lower in ['s', 'str', 'string'] or 'string' in content_lower:
            return 'str'
        elif param_lower in ['root', 'node'] or 'tree' in content_lower:
            return 'TreeNode'
        elif param_lower in ['target', 'k', 'n'] or 'integer' in content_lower:
            return 'int'
        elif param_lower in ['matrix', 'grid'] or 'matrix' in content_lower:
            return 'List[List[int]]'
        else:
            return 'Any'
    
    def _infer_return_type(self, content: str) -> str:
        """Infer return type from content analysis"""
        content_lower = content.lower()
        
        if 'return' in content_lower and ('list' in content_lower or 'array' in content_lower):
            return 'List[int]'
        elif 'return' in content_lower and ('string' in content_lower or 'str' in content_lower):
            return 'str'
        elif 'return' in content_lower and ('boolean' in content_lower or 'bool' in content_lower):
            return 'bool'
        elif 'return' in content_lower and ('integer' in content_lower or 'int' in content_lower):
            return 'int'
        else:
            return 'Any'
    
    def _extract_parameters(self, content: str) -> List[str]:
        """Extract parameter names from content"""
        # Common parameter patterns
        param_patterns = [
            r'(\w+)\s*:\s*str',
            r'(\w+)\s*:\s*int',
            r'(\w+)\s*:\s*List',
            r'(\w+)\s*:\s*bool',
            r'(\w+)\s*=\s*"[^"]*"',
            r'(\w+)\s*=\s*\[[^\]]*\]',
            r'(\w+)\s*=\s*\d+'
        ]
        
        params = []
        for pattern in param_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if match not in params:
                    params.append(match)
        
        # If no parameters found, try common ones based on content
        if not params:
            if 'nums' in content.lower():
                params.append('nums')
            if 'target' in content.lower():
                params.append('target')
            if 's' in content.lower() and 'string' in content.lower():
                params.append('s')
            if 'root' in content.lower():
                params.append('root')
        
        return params[:3]  # Limit to 3 parameters
    
    def _generate_generic_signature(self, title: str) -> str:
        """Generate a generic function signature based on title"""
        # Convert title to function name using camelCase
        function_name = title.lower().replace(' ', '').replace('-', '')
        function_name = re.sub(r'[^a-zA-Z0-9]', '', function_name)
        
        # Convert to camelCase (first letter lowercase)
        if function_name:
            function_name = function_name[0].lower() + function_name[1:]
        else:
            function_name = 'solution'
        
        return f"""class Solution(object):
    def {function_name}(self, input):
        \"\"\"
        :type input: Any
        :rtype: Any
        \"\"\"
        # Your code here
        pass"""
    
    def generate_test_cases(self, examples: List[Dict], title: str) -> List[Dict]:
        """Generate test cases from LeetCode examples"""
        if not examples:
            return self._generate_fallback_test_cases(title)
        
        test_cases = []
        for i, example in enumerate(examples, 1):
            # Parse input and output
            input_text = example.get('input', '').strip()
            output_text = example.get('output', '').strip()
            
            # Clean and format the input/output
            input_text = self._format_test_input(input_text)
            output_text = self._format_test_output(output_text)
            
            test_cases.append({
                'input': input_text,
                'expected': output_text
            })
        
        return test_cases
    
    def _format_test_input(self, input_text: str) -> str:
        """Format test input for Python execution"""
        if not input_text:
            return ""
        
        # Clean the input text
        input_text = input_text.strip()
        
        # Handle common input formats
        # If it's already in the right format, return as is
        if '=' in input_text and not input_text.startswith('['):
            return input_text
        
        # If it's a list or array, format it properly
        if input_text.startswith('[') and input_text.endswith(']'):
            # Try to determine the parameter name
            if 'nums' in input_text.lower():
                return f"nums = {input_text}"
            elif 'digits' in input_text.lower():
                return f"digits = {input_text}"
            elif 'strs' in input_text.lower():
                return f"strs = {input_text}"
            else:
                return f"input = {input_text}"
        
        # If it's a string, format it properly
        if input_text.startswith('"') and input_text.endswith('"'):
            return f's = {input_text}'
        
        # Default formatting
        return input_text
    
    def _format_test_output(self, output_text: str) -> str:
        """Format test output for comparison"""
        if not output_text:
            return ""
        
        # Clean the output text
        output_text = output_text.strip()
        
        # If it's already quoted, return as is
        if output_text.startswith('"') and output_text.endswith('"'):
            return output_text
        
        # If it's a boolean, format it
        if output_text.lower() in ['true', 'false']:
            return output_text.capitalize()
        
        # If it's a number, return as is
        if output_text.isdigit() or (output_text.startswith('-') and output_text[1:].isdigit()):
            return output_text
        
        # If it's a list, return as is
        if output_text.startswith('[') and output_text.endswith(']'):
            return output_text
        
        # Default: wrap in quotes
        return f'"{output_text}"'
    
    def _generate_fallback_test_cases(self, title: str) -> List[Dict]:
        """Generate fallback test cases when no examples are available"""
        title_lower = title.lower()
        
        if 'two sum' in title_lower:
            return [
                {'input': 'nums = [2,7,11,15]\ntarget = 9', 'expected': '[0,1]'},
                {'input': 'nums = [3,2,4]\ntarget = 6', 'expected': '[1,2]'}
            ]
        elif 'reverse' in title_lower and 'vowels' in title_lower:
            return [
                {'input': 's = "hello"', 'expected': '"holle"'},
                {'input': 's = "leetcode"', 'expected': '"leotcede"'}
            ]
        elif 'add binary' in title_lower:
            return [
                {'input': 'a = "11"\nb = "1"', 'expected': '"100"'},
                {'input': 'a = "1010"\nb = "1011"', 'expected': '"10101"'}
            ]
        else:
            return [
                {'input': 'input = "test"', 'expected': '"result"'},
                {'input': 'input = "example"', 'expected': '"output"'}
            ]
    
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
    
    def search_problem_by_name(self, problem_name: str) -> Optional[Dict]:
        """Search for a problem by name (case-insensitive partial match)"""
        try:
            # Get all problems to search through
            problems = self.get_problems(limit=1000)  # Get more problems for search
            
            if not problems:
                return None
            
            # Normalize the search term
            search_term = problem_name.lower().strip()
            
            # Search for exact matches first
            for problem in problems:
                if problem['title'].lower() == search_term:
                    print(f"Found exact match for '{problem_name}': {problem['title']}")
                    return problem
            
            # Search for partial matches
            matches = []
            for problem in problems:
                title_lower = problem['title'].lower()
                if search_term in title_lower:
                    matches.append(problem)
            
            if matches:
                # Return the first match (most relevant)
                print(f"Found {len(matches)} partial matches for '{problem_name}': {matches[0]['title']}")
                return matches[0]
            
            # If no matches found, try searching by title slug
            title_slug = search_term.replace(' ', '-').replace('_', '-')
            for problem in problems:
                if problem['titleSlug'].lower() == title_slug:
                    print(f"Found match by title slug for '{problem_name}': {problem['title']}")
                    return problem
            
            print(f"No matches found for '{problem_name}'")
            return None
            
        except Exception as e:
            print(f"Error searching for problem by name: {e}")
            return None


# Global instance
leetcode_service = LeetCodeService()
