from django.db import models
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField
from datetime import datetime, date
import uuid
from . import vars

def get_default_title(type: str):
    return type + ' ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Base model with default fields
class Base(models.Model):
    id = models.UUIDField('ID', primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)
    created_by = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)

    class Meta:
        abstract = True

################################################################################
# Core models ##################################################################
################################################################################

# Person model
class Person(Base):
    first_name = models.CharField('First Name', max_length=100)
    last_name = models.CharField('Last Name', max_length=100)
    email = models.EmailField('Email', blank=True, null=True)
    phone = models.CharField('Phone Number', max_length=20, blank=True, null=True)
    birthday = models.DateField('Birthday', blank=True, null=True)
    title = models.CharField('Title', max_length=50, blank=True, null=True)
    department = models.CharField('Department', max_length=100, blank=True, null=True)
    is_self = models.BooleanField('This is Me', default=False, blank=False)
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name='user_profile')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# Meeting model
class Meeting(Base):
    title = models.CharField('Title', max_length=100, blank=False, default=get_default_title('Meeting'))
    description = RichTextField('Description', max_length=255)
    start_time = models.DateTimeField('Start time', blank=False, null=True)
    end_time = models.DateTimeField('End time', blank=True, null=True)
    location = models.CharField('Location', max_length=100)

    def __str__(self):
        return self.title

    def get_duration(self):
        if self.end_time is None or self.start_time is None:
            return

        duration = (self.end_time - self.start_time).total_seconds()

        return duration if duration >= 0 else False

    duration = property(get_duration)

# Note model
class Note(Base):
    title = models.CharField('Title', max_length=100, blank=False, default=get_default_title('Note'))
    text = RichTextField('Text')

    def __str__(self):
        return self.title

# Project model
class Project(Base):
    title = models.CharField('Title', max_length=100, blank=False, default=get_default_title('Project'))
    description = RichTextField('Description')
    impact = RichTextField('Impact')
    status = models.CharField('Status', max_length = 50, choices=vars.PROJECT_STATUS_CHOICES)
    start_date_proj = models.DateField('Projected Start Date', blank=True, null=True)
    start_date_actual = models.DateField('Actual Start Date', blank=True, null=True)
    completion_date_proj = models.DateField('Projected Completion Date', blank=True, null=True)
    completion_date_actual = models.DateField('Actual Completion Date', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_start_date(self):
        if self.start_date_actual:
            return self.start_date_actual
        elif self.start_date_proj:
            return self.start_date_proj

    def get_start_date_type(self):
        if self.start_date_actual:
            return 'actual'
        elif self.start_date_proj:
            return 'projected'

    def get_completion_date(self):
        if self.completion_date_actual:
            return self.completion_date_actual
        elif self.completion_date_proj:
            return self.completion_date_proj

    def get_completion_date_type(self):
        if self.completion_date_actual:
            return 'actual'
        elif self.completion_date_proj:
            return 'projected'

    start_date = property(get_start_date)
    start_date_type = property(get_start_date_type)
    completion_date = property(get_completion_date)
    completion_date_type = property(get_completion_date_type)

    def get_duration(self):
        if self.start_date is None or self.completion_date is None:
            return

        duration = (self.completion_date - self.start_date).days

        return duration if duration >= 0 else False

    duration = property(get_duration)

# Action Item model
class ActionItem(Base):
    title = models.CharField('Title', max_length=100, blank=False, default=get_default_title('Action Item'))
    description = RichTextField('Description')
    story_points = models.IntegerField(blank=True, null=True)
    status = models.CharField('Status', max_length=50, choices=vars.ACTION_ITEM_STATUS_CHOICES, blank=True, null=True)
    completion_date_proj = models.DateField('Projected Completion Date', blank=True, null=True)
    completion_date_actual = models.DateField('Actual Completion Date', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_completion_date(self):
        if self.completion_date_actual:
            return self.completion_date_actual
        elif self.completion_date_proj:
            return self.completion_date_proj

    def get_completion_date_type(self):
        if self.completion_date_actual:
            return 'actual'
        elif self.completion_date_proj:
            return 'projected'

    completion_date = property(get_completion_date)
    completion_date_type = property(get_completion_date_type)

    def get_days_to_completion(self):
        return (self.completion_date - date.today()).days

    days_to_completion = property(get_days_to_completion)

    def get_state(self):
        if self.days_to_completion > 0:
            return 'ok'
        elif self.days_to_completion == 0:
            return 'soon'
        else:
            return 'overdue'

    state = property(get_state)

# Comment model
class Comment(Base):
    to_action_item = models.ForeignKey(ActionItem, on_delete=models.CASCADE, related_name='com_to_action_item', blank=False)
    text = RichTextField('Text')

    def __str__(self):
        return f'{self.created_by}\'s {self.created_at} comment on {self.to_action_item}'

# Attachment model
class FileUpload(Base):
    title = models.CharField('Title', max_length=100, blank=False, default=get_default_title('Attachment'))
    file = models.FileField('Attachment')
    description = models.TextField('Description')

    def __str__(self):
        return self.title

################################################################################
# Cross-reference models #######################################################
################################################################################

# Relationship model
class Relationship(Base):
    from_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='rel_from_person', blank=False)
    to_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='rel_to_person', blank=False)
    type = models.CharField('Type',max_length=100)
    description = models.TextField('Description', blank=True, null=True)

    def __str__(self):
        return f'{self.from_person}\'s relationship to {self.to_person}'

# Attendance model
class Attendance(Base):
    from_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='att_from_person', blank=False)
    to_meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='att_to_meeting', blank=False)
    type = models.CharField('Type', max_length=20)

    def __str__(self):
        return f'{self.from_person}\'s attendance at {self.to_meeting}'

# Document model
class Document(Base):
    from_note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='doc_from_note', blank=False)
    to_meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='doc_to_meeting', blank=False)
    type = models.CharField('Type', max_length=20, choices=vars.DOCUMENT_TYPE_CHOICES)
    origin = models.BooleanField('Origin?', default=True, blank=False)

    def __str__(self):
        return f'{self.from_note} from {self.to_meeting}'

# Stakeholder model
class Stakeholder(Base):
    from_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='sta_from_person', blank=False)
    to_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sta_to_project', blank=False)
    type = models.CharField('Type', max_length=100, choices=vars.STAKEHOLDER_TYPE_CHOICES)
    description = models.TextField('Description', blank=True, null=True)
    is_poc = models.BooleanField('Point of Contact?', default=False, blank=False)

    def __str__(self):
        return f'{self.from_person}\'s stake in {self.to_project}'

# Contributor model
class Contributor(Base):
    from_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='con_from_person', blank=False)
    to_action_item = models.ForeignKey(ActionItem, on_delete=models.CASCADE, related_name='con_to_action_item', blank=False)
    type = models.CharField('Type', max_length=100, choices=vars.CONTRIBUTOR_TYPE_CHOICES)
    description = models.TextField('Description', blank=True, null=True)
    is_poc = models.BooleanField('Point of Contact?', default=False, blank=False)

    def __str__(self):
        return f'{self.from_person}\'s contribution to {self.to_action_item}'

# Discussion model
class Discussion(Base):
    from_meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='dis_from_meeting', blank=False)
    to_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='dis_to_project', blank=False)
    type = models.CharField('Type', max_length=100, choices=vars.DISCUSSION_TYPE_CHOICES)
    description = models.TextField('Description', blank=True, null=True)

    def __str__(self):
        return f'{self.from_meeting} discussion of {self.to_project}'

# Task model
class Task(Base):
    from_action_item = models.ForeignKey(ActionItem, on_delete=models.CASCADE, related_name='tas_from_action_item', blank=False)
    to_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tas_to_project', blank=False)
    type = models.CharField('Type', max_length=100, choices=vars.TASK_TYPE_CHOICES)
    description = models.TextField('Description', blank=True, null=True)

    def __str__(self):
        return f'{self.from_action_item}\'s contribution to {self.to_project}'
