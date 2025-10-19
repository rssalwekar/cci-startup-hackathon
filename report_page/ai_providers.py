import os


class KronosProvider:
    """Kronos Labs API Provider"""
    
    def __init__(self, api_key=None):
        try:
            from kronoslabs import Kronos
            self.client = Kronos(api_key=api_key or os.environ.get('KRONOS_API_KEY'))
        except ImportError:
            raise ImportError("Install kronoslabs: pip install kronoslabs")
    
    def generate_analysis(self, prompt):
        """Call Kronos API to generate analysis"""
        try:
            response = self.client.chat.completions.create(
                model="hermes-3-llama-3.1-405b-fp8",
                messages=[
                    {"role": "system", "content": "You are an expert technical interviewer providing detailed, constructive feedback."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Kronos API Error: {e}")
            return None