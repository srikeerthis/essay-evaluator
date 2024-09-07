from openai import  OpenAI
from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from spellchecker import SpellChecker
import os
from dotenv import load_dotenv
import re
import json
from .models import EssaySubmission

load_dotenv()

# Load OpenAI API key from environment variable or Django settings
OPENAI_API_KEY= os.getenv("OPEN_API_KEY")

def clean_text(text):
    # Remove punctuation from text, keeping only words and spaces
    return re.sub(r'[^\w\s]', '', text)

def evaluate_essay(request):
    if request.method == 'POST':
        essay = request.POST.get('essay')
        title = request.POST.get('title')
         # 1. Clean the essay text for spelling checking (removes punctuation)
        cleaned_essay = clean_text(essay)
        
        # 2. Check spelling errors using SpellChecker
        spell = SpellChecker()
        words = cleaned_essay.split()
        misspelled = spell.unknown(words)

        spelling_errors = list(misspelled)
        spelling_errors_count = len(spelling_errors)

        # 2. Ask OpenAI to evaluate the content relevance
        model = os.getenv("MODEL")
        # Load the prompts from .env file
        system_prompt = os.getenv('SYSTEM_PROMPT')
        essay_prompt = os.getenv('ESSAY_PROMPT').format(title=title, essay=essay)
        relevance_prompt = os.getenv('RELEVANCE_PROMPT').format(title=title)
        feedback_prompt = os.getenv('FEEDBACK_PROMPT')
        response_format_prompt = os.getenv('RESPONSE_FORMAT_PROMPT')

        client = OpenAI()
        try:
            response = client.chat.completions.create(
                model=model,
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": essay_prompt},
                    {"role": "user", "content": relevance_prompt},
                    {"role": "user", "content": feedback_prompt},
                    {"role": "user", "content": response_format_prompt}
                ]
            )        
            feedback = response.choices[0].message.content.strip("feedback:").lower()
            # Parse the response content as a JSON object
            response_json = json.loads(feedback)

            # Extract relevance, feedback, and score
            relevance = response_json.get('relevance', 'Error extracting relevance')
            feedback = response_json.get('feedback', {})
            score_of_essay = response_json.get('score_of_essay', 'Error extracting score')
        except Exception as e:
            relevance = "Error in OpenAI API call"

        # 4. Save the result to the database
        EssaySubmission.objects.create(
            title=title,
            essay=essay,
            relevance_to_topic=relevance,
            spelling_errors_count=spelling_errors_count,
            spelling_errors=', '.join(spelling_errors),  # Convert list to string
            feedback_strength=feedback['strength'],
            feedback_weakness=feedback['weakness'],
            feedback_suggestion=feedback['suggestion'],
            score_of_essay=score_of_essay
        )

        # 5. Return the result in JSON format
        result = {
            'relevance_to_topic': relevance,
            'spelling_errors_count': spelling_errors_count,
            'spelling_errors': spelling_errors,
            'feedback': feedback,
            'score_of_essay': score_of_essay
        }
        return JsonResponse(result)

    # If GET request, display form
    return render(request, 'evaluator/form.html')

def submission_history(request):
    submissions = EssaySubmission.objects.all().order_by('-submitted_at')
    return render(request, 'evaluator/history.html', {'submissions': submissions})

def submission_detail(request, submission_id):
    # Retrieve the specific submission based on its ID
    submission = get_object_or_404(EssaySubmission, id=submission_id)
    return render(request, 'evaluator/submission_detail.html', {'submission': submission})
