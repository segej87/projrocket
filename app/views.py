from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Project, Task, ActionItem


# TODO: replace with main view
def index(request):
    context = {
        'temp': 'delete'
    }

    return render(request, 'app/index.html', context)

def projectlist(request):
    # Get the project list
    upcoming_projects_list = Project.objects.order_by('-completion_date_proj')[:10]

    for p in upcoming_projects_list:
        p.pending_tasks = Task.objects.filter(to_project = p).exclude(from_action_item__status='complete').count()
        p.completed_tasks = Task.objects.filter(to_project = p, from_action_item__status='complete').count()

    context = {
        'upcoming_projects_list': upcoming_projects_list
    }

    return render(request, 'app/projects.html', context)


def projectdetail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tas_to_project.order_by('from_action_item__completion_date_proj', 'from_action_item__status')
    open_action_items_list = [t.from_action_item for t in tasks if t.from_action_item.status != 'complete']
    completed_action_items_list = [t.from_action_item for t in tasks if t.from_action_item.status == 'complete']

    context = {
        'project': project,
        'open_action_items_list': open_action_items_list,
        'completed_action_items_list': completed_action_items_list
    }

    return render(request, 'app/projects/detail.html', context)

def actionitemdetail(request, action_item_id):
    action_item = get_object_or_404(ActionItem, id=action_item_id)

    context = {
        'action_item': action_item
    }

    return render(request, 'app/actionitems/detail.html', context)
