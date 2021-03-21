import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.shortcuts import reverse

import uuid

from .models import Meeting, Project, User
from .forms import NewPersonForm
from .views import newperson

class MeetingModelTests(TestCase):
    def test_meeting_duration_can_be_negative(self):
        """
        Meeting.get_duration() returns False if the meeting end time
        is before the start time
        """
        start_time = datetime.datetime(2021, 3, 18, 12)
        end_time = datetime.datetime(2021, 3, 18, 11)

        meeting = Meeting(start_time=start_time, end_time=end_time)

        self.assertIs(meeting.get_duration(), False)

    def test_meeting_duration_none_when_missing_time(self):
        """
        Meeting.get_duration() returns None if the meeting end time
        or start time are missing
        """
        start_time = datetime.datetime(2021, 3, 18, 12)

        meeting = Meeting(start_time=start_time)

        self.assertIs(meeting.get_duration(), None)

class ProjectModelTests(TestCase):
    def test_project_duration_can_be_negative(self):
        """
        Project.get_duration() returns False if the project end date
        is before the start date
        """
        start_date = datetime.datetime(2021, 3, 18)
        end_date = datetime.datetime(2021, 3, 17)

        project = Project(start_date_actual=start_date, completion_date_actual=end_date)

        self.assertIs(project.get_duration(), False)

    def test_project_duration_none_when_missing_date(self):
        """
        Project.get_duration() returns None if the project end date
        or start date are missing
        """
        start_date = datetime.datetime(2021, 3, 18)

        project = Project(start_date_actual=start_date)

        self.assertIs(project.get_duration(), None)

################################################################################
#### FORM TESTS ################################################################
################################################################################
class NewTopicTests(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        c = Client()
        logged_in = c.login(username='testuser', password='12345')

    def test_contains_form(self):
        '''
        The new person url should render a new person form
        '''
        url = reverse('newperson')
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewPersonForm)

    def test_new_person_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('newperson')
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)
