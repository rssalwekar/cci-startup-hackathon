import json
from .ai_providers import KronosProvider


class ReportGenerator:
    """Report generation using Kronos Labs API"""
    
    def __init__(self, api_key=None):
        """Initialize with Kronos API"""
        self.provider = KronosProvider(api_key)
    
    def analyze_interview(self, interview_data):
        """
        Generate report from interview data
        
        Args:
            interview_data: Dict with interview info
            
        Returns:
            Dict with report data
        """
        
        # Create AI prompt
        prompt = self._create_prompt(interview_data)
        
        # Call Kronos API
        ai_response = self.provider.generate_analysis(prompt)
        
        # Parse response
        if ai_response:
            report = self._parse_response(ai_response, interview_data)
        else:
            report = self._fallback_report()
        
        return report
    
    def _create_prompt(self, data):
        """Create the prompt for Kronos AI"""
        
        prompt = f"""You are an expert technical interviewer analyzing a coding interview session. 
Provide a detailed, constructive analysis in JSON format.

**Interview Data:**
- Problem: {data.get('problem_title', 'Unknown')}
- Difficulty: {data.get('difficulty', 'medium')}
- Time Taken: {data.get('time_taken', 0)} seconds
- Test Cases Passed: {data.get('test_cases_passed', 0)}/{data.get('total_test_cases', 0)}

**Code Submitted:**
```{data.get('programming_language', 'python')}
{data.get('code_submission', '')}
```

**Chat Transcript:**
{data.get('chat_transcript', '')}

Please analyze and return ONLY a valid JSON object with this exact structure:
{{
    "overall_score": 8.5,
    "code_quality_score": 8.0,
    "communication_score": 9.0,
    "problem_solving_score": 8.5,
    "code_analysis": {{
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "code_quality": "Clean and readable code",
        "best_practices": ["Good naming", "Edge cases handled"],
        "issues_found": ["Could optimize loop"],
        "optimization_suggestions": ["Use hash map for O(1) lookups"]
    }},
    "communication_analysis": {{
        "clarity": "Explained approach clearly",
        "technical_terminology": "Used appropriate terms",
        "explanation_quality": "Good step-by-step logic",
        "problem_approach": "Systematic problem solving"
    }},
    "strengths": ["Strong logic", "Good communication", "Clean code"],
    "weaknesses": ["Time complexity analysis needed", "Missed edge case"],
    "improvement_tips": [
        {{"area": "Algorithms", "tip": "Practice pattern recognition"}},
        {{"area": "Communication", "tip": "Verbalize thought process more"}}
    ],
    "recommended_resources": [
        {{"title": "LeetCode Patterns", "type": "article", "url": ""}},
        {{"title": "Time Complexity Guide", "type": "video", "url": ""}}
    ],
    "detailed_feedback": "Strong performance with good problem-solving skills and clear communication..."
}}

Return ONLY the JSON object, no additional text."""
        
        return prompt
    
    def _parse_response(self, ai_text, interview_data):
        """Parse Kronos response into structured data"""
        try:
            # Extract JSON
            start = ai_text.find('{')
            end = ai_text.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = ai_text[start:end]
                report = json.loads(json_str)
            else:
                report = json.loads(ai_text)
            
            # Set defaults
            report.setdefault('overall_score', 7.0)
            report.setdefault('code_quality_score', 7.0)
            report.setdefault('communication_score', 7.0)
            report.setdefault('problem_solving_score', 7.0)
            
            # Calculate time management score
            expected_time = {'easy': 900, 'medium': 1800, 'hard': 2700}
            difficulty = interview_data.get('difficulty', 'medium')
            expected = expected_time.get(difficulty, 1800)
            time_taken = max(interview_data.get('time_taken', 1), 1)
            time_score = min(10, (expected / time_taken) * 10)
            report['time_management_score'] = round(time_score, 2)
            
            return report
            
        except Exception as e:
            print(f"Parse error: {e}")
            return self._fallback_report()
    
    def _fallback_report(self):
        """Default report if API fails"""
        return {
            "overall_score": 7.0,
            "code_quality_score": 7.0,
            "communication_score": 7.0,
            "problem_solving_score": 7.0,
            "time_management_score": 7.0,
            "code_analysis": {
                "time_complexity": "Analysis pending",
                "space_complexity": "Analysis pending",
                "code_quality": "Unable to analyze",
                "best_practices": [],
                "issues_found": [],
                "optimization_suggestions": []
            },
            "communication_analysis": {
                "clarity": "Pending",
                "technical_terminology": "Pending",
                "explanation_quality": "Pending",
                "problem_approach": "Pending"
            },
            "strengths": ["Completed interview"],
            "weaknesses": ["Analysis pending"],
            "improvement_tips": [{"area": "General", "tip": "Keep practicing!"}],
            "recommended_resources": [],
            "detailed_feedback": "Report generation unavailable. Please try again."
        }