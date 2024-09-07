from django.urls import path
from . import views

urlpatterns = [
    path('', views.evaluate_essay, name='evaluate_essay'),
    path('history/',views.submission_history,name="submission_history"),
    path('history/<int:submission_id>/', views.submission_detail, name='submission_detail'),
]
