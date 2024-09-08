# Essay evaluator - Web Application

This project is a Django-based web application that allows users to submit essays for evaluation. The application uses the OpenAI API to analyze the essay, provide feedback, and score it based on relevance, spelling, and overall quality.
Features:

- Submit essays via a simple web form.
- Receive feedback in the form of strengths, weaknesses, and suggestions.
- Evaluate the essay’s relevance to the provided topic.
- Score essays on a scale of 1 to 10.
- View the history of past submissions, including essay content, feedback, and scores.

## Setup Instructions

### Prerequisites

- Python 3.x
- Django
- OpenAI API Key

## Installation

Clone the repository:

```
git clone <repository-url>
cd <repository-directory>
```

Create a virtual environment:

```
python -m venv env
source env/bin/activate

# On Windows use
`env\Scripts\activate`
```

Install dependencies:

```
pip install -r requirements.txt
```

Create a .env file in the project root and add your configuration:

```
OPENAI_API_KEY=your-openai-api-key
SYSTEM_PROMPT="Your prompt"
ESSAY_PROMPT="Essay Title: {title}\nEssay Body: {essay}"
RELEVANCE_PROMPT="Your prompt"
FEEDBACK_PROMPT="Your prompt"
RESPONSE_FORMAT_PROMPT="Your prompt"
```

## Run database migrations:

```
python manage.py migrate
```

## Run the development server:

```
python manage.py runserver
```

Access the application at http://127.0.0.1:8000/.

How to Use

- **Submit a New Essay**: Navigate to the homepage and fill out the form with an essay title and essay body.
- **View History**: Go to the /history/ URL to view all previous essay submissions, along with feedback and scores.
- **View Submission Details**: Click on any submission in the history page to see full details, including the essay content.

## Environment Variables

Ensure the following variables are present in your .env file:

    OPENAI_API_KEY: Your OpenAI API key for accessing the OpenAI API.

    Prompts for essay evaluation:
    SYSTEM_PROMPT, ESSAY_PROMPT, RELEVANCE_PROMPT, FEEDBACK_PROMPT, and RESPONSE_FORMAT_PROMPT.

## License

This project is licensed under the MIT License.
