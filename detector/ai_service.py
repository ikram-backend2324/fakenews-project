import requests
import json
import time
from django.conf import settings


SYSTEM_PROMPT = """You are an expert fake news detection AI. Your task is to analyze news text and determine if it is real, fake, or uncertain.

Analyze the provided news text carefully for:
1. Sensationalist language and emotional manipulation
2. Lack of credible sources or specific details
3. Logical inconsistencies or factual impossibilities
4. Common misinformation patterns
5. Writing style and journalistic quality

Respond ONLY with a valid JSON object in this exact format:
{
  "verdict": "fake" | "real" | "uncertain",
  "confidence": <integer 0-100>,
  "reasoning": "<detailed explanation in 2-4 sentences>"
}

Do not include any other text, markdown, or explanation outside the JSON object."""


def analyze_news(text: str, lang: str = 'en') -> dict:
    """
    Send news text to OpenRouter (DeepSeek) and return analysis result.
    Returns dict with verdict, confidence, reasoning.
    """
    api_key = settings.OPENROUTER_API_KEY
    model = settings.OPENROUTER_MODEL

    if not api_key:
        return {
            'verdict': 'uncertain',
            'confidence': 0,
            'reasoning': 'API key not configured. Please set OPENROUTER_API_KEY in environment variables.',
            'error': True,
        }

    lang_instructions = {
        'en': 'Respond in English.',
        'ru': 'Respond in Russian (Русский язык).',
        'uz': 'Respond in Uzbek (O\'zbek tili).',
    }
    lang_note = lang_instructions.get(lang, lang_instructions['en'])

    user_prompt = f"""Analyze the following news text for authenticity. {lang_note}

NEWS TEXT:
\"\"\"{text}\"\"\"

Return your analysis as JSON only."""

    start_time = time.time()

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://fakenews-ai.onrender.com",
                "X-Title": "FakeNews AI Detector",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.1,
                "max_tokens": 500,
            },
            timeout=60,
        )
        elapsed = time.time() - start_time

        if response.status_code != 200:
            return {
                'verdict': 'uncertain',
                'confidence': 0,
                'reasoning': f'AI service error: {response.status_code}. Please try again.',
                'processing_time': elapsed,
                'error': True,
            }

        data = response.json()
        content = data['choices'][0]['message']['content'].strip()

        # Strip markdown code fences if present
        if content.startswith('```'):
            content = content.split('```')[1]
            if content.startswith('json'):
                content = content[4:]
        content = content.strip()

        result = json.loads(content)

        # Validate and sanitize
        verdict = result.get('verdict', 'uncertain').lower()
        if verdict not in ('fake', 'real', 'uncertain'):
            verdict = 'uncertain'

        confidence = int(result.get('confidence', 50))
        confidence = max(0, min(100, confidence))

        reasoning = str(result.get('reasoning', ''))[:1000]

        return {
            'verdict': verdict,
            'confidence': confidence,
            'reasoning': reasoning,
            'processing_time': elapsed,
            'error': False,
        }

    except json.JSONDecodeError:
        elapsed = time.time() - start_time
        return {
            'verdict': 'uncertain',
            'confidence': 0,
            'reasoning': 'Could not parse AI response. Please try again.',
            'processing_time': elapsed,
            'error': True,
        }
    except requests.exceptions.Timeout:
        elapsed = time.time() - start_time
        return {
            'verdict': 'uncertain',
            'confidence': 0,
            'reasoning': 'Request timed out. Please try again.',
            'processing_time': elapsed,
            'error': True,
        }
    except Exception as e:
        elapsed = time.time() - start_time
        return {
            'verdict': 'uncertain',
            'confidence': 0,
            'reasoning': f'An unexpected error occurred: {str(e)}',
            'processing_time': elapsed,
            'error': True,
        }
