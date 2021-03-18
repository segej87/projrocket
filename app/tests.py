import datetime

from django.test import TestCase

from .models import Meeting, Project

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
