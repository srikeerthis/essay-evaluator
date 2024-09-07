from django.db import models

class EssaySubmission(models.Model):
    title = models.CharField(max_length=255)
    essay = models.TextField()
    relevance_to_topic = models.CharField(max_length=10)  # Store Yes/No
    spelling_errors_count = models.IntegerField()
    spelling_errors = models.TextField()  # Store list of errors as a string
    feedback_strength = models.TextField()
    feedback_weakness = models.TextField()
    feedback_suggestion = models.TextField()
    score_of_essay = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (Relevance: {self.relevance_to_topic}, Spelling Errors: {self.spelling_errors_count})"
