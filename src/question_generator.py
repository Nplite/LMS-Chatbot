import ollama
import json
import re

class QuestionGenerator:
    def __init__(self, model_name="qwen3:8b"):
        self.model_name = model_name
    
    def generate_mcqs(self, content, num_questions=5):
        """Generate MCQ questions from content"""
        prompt = f"""Based on the following educational content, generate {num_questions} multiple-choice questions (MCQs).

Content:
{content[:3000]}

For each question, provide:
1. The question text
2. Four options (A, B, C, D)
3. The correct answer
4. Difficulty level (Easy/Medium/Hard)
5. A brief explanation

Format your response as a JSON array with this structure:
[
  {{
    "question": "Question text here?",
    "options": {{
      "A": "Option A",
      "B": "Option B",
      "C": "Option C",
      "D": "Option D"
    }},
    "correct_answer": "A",
    "difficulty": "Medium",
    "explanation": "Brief explanation"
  }}
]

Generate exactly {num_questions} MCQs. Return ONLY the JSON array, no additional text."""

        response = ollama.chat(
            model=self.model_name,
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        return self._parse_json_response(response['message']['content'])
    
    def generate_short_answer(self, content, num_questions=2):
        """Generate short answer questions"""
        prompt = f"""Based on the following educational content, generate {num_questions} short-answer questions that require 2-3 sentence responses.

Content:
{content[:3000]}

For each question, provide:
1. The question text
2. A model answer (2-3 sentences)
3. Difficulty level (Easy/Medium/Hard)

Format your response as a JSON array:
[
  {{
    "question": "Question text here?",
    "model_answer": "Expected answer here",
    "difficulty": "Medium"
  }}
]

Generate exactly {num_questions} short-answer questions. Return ONLY the JSON array."""

        response = ollama.chat(
            model=self.model_name,
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        return self._parse_json_response(response['message']['content'])
    
    def _parse_json_response(self, response_text):
        """Extract JSON from response"""
        try:
            # Try to find JSON array in response
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(f"Response was: {response_text[:500]}")
            return []