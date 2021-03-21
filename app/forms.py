from django import forms
from .models import Person, Project, ActionItem, Stakeholder, Comment, Task

from djrichtextfield.widgets import RichTextWidget

class NewPersonForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(), required=False)
    birthday = forms.DateField(widget=forms.DateInput(), required=False)

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'phone', 'birthday', 'title', 'department', 'is_self']

class NewProjectForm(forms.ModelForm):
    description = forms.CharField(widget=RichTextWidget())

    class Meta:
        model = Project
        fields = ['title', 'description', 'impact', 'status', 'start_date_proj', 'start_date_actual', 'completion_date_proj', 'completion_date_actual']

class NewActionItemForm(forms.ModelForm):
    description = forms.CharField(widget=RichTextWidget())

    class Meta:
        model = ActionItem
        fields = ['title', 'description', 'story_points', 'status', 'completion_date_proj', 'completion_date_actual']

class NewStakeholderForm(forms.ModelForm):
    class Meta:
        model = Stakeholder
        fields = ['from_person', 'to_project', 'type', 'description', 'is_poc']

class NewProjectStakeholderForm(forms.ModelForm):
    class Meta:
        model = Stakeholder
        fields = ['from_person', 'type', 'description', 'is_poc']

    def __init__(self, project_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        project_id = project_id

        project = Project.objects.get(id=project_id)

        linked_stakeholders = Stakeholder.objects.filter(to_project=project).values('from_person')
        unlinked_people = Person.objects.exclude(id__in=linked_stakeholders).exclude(user__username='admin').all()

        self.fields['from_person'].queryset = unlinked_people

class NewCommentForm(forms.ModelForm):
    text = forms.CharField(widget=RichTextWidget())

    class Meta:
        model = Comment
        fields = ['text']

class NewProjectTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['from_action_item', 'type', 'description']

    def __init__(self, project_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        project_id = project_id

        project = Project.objects.get(id=project_id)

        linked_tasks = Task.objects.filter(to_project=project).values('from_action_item_id')
        unlinked_action_items = ActionItem.objects.exclude(id__in=linked_tasks).all()

        self.fields['from_action_item'].queryset  = unlinked_action_items
