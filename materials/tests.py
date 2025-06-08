from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from materials.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.course = Course.objects.create(
            title="Python developer", description="Develop on python", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Validators, pagination and tests",
            description="lesson 1",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    def test_course_create(self):
        self.assertEqual(Course.objects.all().count(), 1)

    @patch('materials.views.course_update.delay')  # Mock the Celery task
    def test_course_update(self, mock_task):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {"title": "Javascript"}
