from urllib import response
from django.test import TestCase

import datetime
# Create your tests here.
from .models import Question
from django.utils import timezone
from django.urls import reverse

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are added')
        self.assertQuerySetEqual(response.context['latest_questions'], [])

    def test_past_questions(self):
        question = create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_questions'], [question],)

    def test_future_questions(self):
        create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are added')
        self.assertQuerySetEqual(response.context['latest_questions'], [])

    def test_future_past_questions(self):
        create_question(question_text='Future question', days=30)
        question = create_question(question_text='Past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_questions'], [question])

    def test_two_past_questions(self):
        question1 = create_question(question_text='First past question', days=-30)
        question2 = create_question(question_text='Second past question', days=-29)
        response = self.client.get(reverse('polls:index'))    
        self.assertQuerySetEqual(response.context['latest_questions'], [question2, question1])