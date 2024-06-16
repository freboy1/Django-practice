from django.test import TestCase

import datetime
# Create your tests here.
from .models import Question
from django.utils import timezone


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=31)
        future_question = Question(pub_date=time)
        self.assertIsInstance(future_question.was_published_recently(), False)