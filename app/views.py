from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Project, Task, ActionItem


# TODO: replace with main view
def index(request):
    return HttpResponse("Hello, world. You're at the app index.")

def projectlist(request):
    # Get the project list
    upcoming_projects_list = Project.objects.order_by('-completion_date_proj')[:10]

    for p in upcoming_projects_list:
        p.pending_tasks = len(Task.objects.filter(to_project = p).exclude(from_action_item__status='complete'))
        p.completed_tasks = len(Task.objects.filter(to_project = p, from_action_item__status='complete'))

    context = {
        'upcoming_projects_list': upcoming_projects_list
    }

    return render(request, 'app/projects.html', context)


def projectdetail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tas_to_project.all()
    action_items = [t.from_action_item for t in tasks]

    context = {
        'project': project,
        'action_items': action_items
    }

    return render(request, 'app/projects/detail.html', context)

def actionitemdetail(request, action_item_id):
    action_item = get_object_or_404(ActionItem, id=action_item_id)

    context = {
        'action_item': action_item
    }

    return render(request, 'app/actionitems/detail.html', context)
