from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Subquery

from plotly.offline import plot
import plotly.graph_objs as go

from numpy import linspace, median
from scipy.stats.kde import gaussian_kde

from .models import Project, Task, ActionItem, User, Person, Stakeholder
from .forms import NewPersonForm, NewProjectForm, NewActionItemForm, NewStakeholderForm, NewProjectStakeholderForm, NewCommentForm, NewProjectTaskForm

# TODO: replace with main view
def index(request):
    context = {
        'temp': 'delete'
    }

    return render(request, 'app/index.html', context)

def projectlist(request):
    # Current user and their Person
    user = request.user
    profile = get_object_or_404(Person, user=user)

    # Projects the person has created
    if request.user.username == 'admin':
        projects_list = Project.objects.order_by('completion_date_proj').all()
    else:
        created_projects = Project.objects.filter(created_by=request.user).order_by('completion_date_proj').all()

        # Projects the person has a stake in
        stakes = Stakeholder.objects.filter(from_person=profile).values('to_project')
        stakeholder_projects = Project.objects.filter(id__in=stakes)

        projects_list = created_projects.union(stakeholder_projects)

    for p in projects_list:
        p.pending_tasks = Task.objects.filter(to_project = p).exclude(from_action_item__status='complete').count()
        p.completed_tasks = Task.objects.filter(to_project = p, from_action_item__status='complete').count()

    context = {
        'projects_list': projects_list
    }

    return render(request, 'app/projects.html', context)


def projectdetail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    tasks = Task.objects.filter(to_project=project).values('from_action_item')
    open_action_items_list = ActionItem.objects.filter(id__in=tasks).exclude(status='complete').order_by('completion_date_proj')
    # completed_action_items_list = ActionItem.objects.filter(id__in=tasks, status='complete') # TODO: allow toggle show completed
    completed_action_items_list = None

    #### Create completion gauge chart #########################################
    total_action_items = ActionItem.objects.filter(id__in=tasks).all().count()

    if total_action_items > 0:
        completion_rate = 100 * (1 - len(open_action_items_list) / total_action_items)
    else:
        completion_rate = 0

    fig = go.Figure()

    gauge = go.Indicator(
        mode = "gauge+number",
        value = completion_rate,
        number = { 'suffix': "%" },
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [None, 100]},
             'steps' : [
                 {'range': [0, 75], 'color': "lightgray"},
                 {'range': [75, 90], 'color': "gray"}],
             'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 100}}
    )

    fig.add_trace(gauge)

    fig.update_layout(
        autosize=False,
        width=250,
        height=175,
        margin=dict(l=50, r=50, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    plot_div = plot(fig, output_type='div', config={"modeBarButtonsToRemove": ['toImage', 'sendDataToCloud'], 'displaylogo': False})

    ############################################################################

    #### Create due date density plot ##########################################

    action_item_dtcs = [a.days_to_completion for a in open_action_items_list]

    kde = gaussian_kde(action_item_dtcs)

    x_range = linspace(min(action_item_dtcs), max(action_item_dtcs), len(action_item_dtcs))
    x_kde = kde(x_range)

    dtcs_fig = go.Figure()

    if median(action_item_dtcs) > 0:
        line_color = '#2E8B57'
    elif median(action_item_dtcs) == 0:
        line_color = '#FF7F50'
    else:
        line_color = '#B22222'

    line = go.Scatter(
        x=x_range,
        y=x_kde,
        fill='tozeroy',
        hoverinfo='none',
        line=dict(width=0.5, color=line_color),
        mode='lines',
    )

    dtcs_fig.update_layout(
            autosize=False,
            width=250,
            height=150,
            margin=dict(l=50, r=50, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis= dict(
                showgrid= False,
                zeroline=False,
                visible=False,
            ),
            shapes=[
                # dict(
                #     type='rect',
                #     yref='paper', y0=0, y1=1,
                #     xref='x', x0=-5, x1=5,
                #     fillcolor='lightgray'
                # ),
                # dict(
                #     type='rect',
                #     yref='paper', y0=0, y1=1,
                #     xref='x', x0=-2, x1=2,
                #     fillcolor='gray'
                # ),
                dict(
                    type= 'line',
                    yref= 'paper', y0=0, y1=1,
                    xref= 'x', x0=0, x1=0
                ),
            ],
        )

    dtcs_fig.add_trace(line)

    dtcs_div = plot(dtcs_fig, output_type='div', config={"displayModeBar": False, "modeBarButtonsToRemove": ['toImage', 'sendDataToCloud'], 'displaylogo': False})

    ############################################################################

    stakeholders = Stakeholder.objects.filter(to_project=project).exclude(from_person__user=request.user)

    context = {
        'project': project,
        'plot_div': plot_div,
        'dtcs_div': dtcs_div,
        'open_action_items_list': open_action_items_list,
        'completed_action_items_list': completed_action_items_list,
        'stakeholders': stakeholders
    }

    return render(request, 'app/projects/detail.html', context)

def newproject(request):
    user = request.user
    profile = Person.objects.get(user=user)

    if request.method == 'POST':
        form = NewProjectForm(request.POST)

        project = form.save(commit=False)
        project.created_by = user
        project.save()

        stakeholder = Stakeholder(from_person = profile, to_project=project, type='participant', description='Created this project')
        stakeholder.created_by = user
        stakeholder.save()

        return redirect('app:project detail', project_id=project.id)
    else:
        form = NewProjectForm()

    context = {
        'form': form
    }

    return render(request, 'app/projects/new.html', context)

def peoplelist(request):
    # Current user and their Person
    user = request.user
    profile = Person.objects.get(user=user)

    people_list = Person.objects.exclude(id=profile.id).all()

    for p in people_list:
        p.stakes = Stakeholder.objects.filter(from_person=p).count()

    context = {
        'people_list': people_list
    }

    return render(request, 'app/people.html', context)

def persondetail(request, person_id):
    person = get_object_or_404(Person, id=person_id)

    context = {
        'person': person
    }

    return render(request, 'app/people/detail.html', context)

def newperson(request, project_id=None):
    user = request.user

    if request.method == 'POST':
        form = NewPersonForm(request.POST)

        if form.is_valid():
            person = form.save(commit=False)
            person.created_by = user
            person.save()

            if project_id:
                project = Project.objects.get(id=project_id)

                stakeholder = Stakeholder(from_person=person, to_project=project, type='user')
                stakeholder.created_by = user
                stakeholder.save()

                return redirect('app:project detail', project_id=project_id)

            return redirect('app:person detail', person_id=person.id)
    else:
        form = NewPersonForm()

    context = {
        'form': form
    }

    return render(request, 'app/people/new.html', context)

def actionitemlist(request):
    context = {

    }

    return render(request, 'app/actionitems.html', context)

def actionitemdetail(request, action_item_id):
    action_item = get_object_or_404(ActionItem, id=action_item_id)

    comments = action_item.com_to_action_item.order_by('created_at')

    tasks = Task.objects.filter(from_action_item=action_item).values('to_project')

    projects_list = Project.objects.filter(id__in=tasks)

    context = {
        'action_item': action_item,
        'comments': comments,
        'projects_list': projects_list
    }

    return render(request, 'app/actionitems/detail.html', context)

def newactionitem(request, project_id=None):
    user = request.user

    if request.method == 'POST':
        form = NewActionItemForm(request.POST)

        actionitem = form.save(commit=False)
        actionitem.created_by = user
        actionitem.save()

        if project_id:
            project = Project.objects.get(id=project_id)

            task = Task(from_action_item=actionitem, to_project=project, type='requirement')
            task.created_by = user
            task.save()

            return redirect('app:project detail', project_id=project_id)

        return redirect('app:actionitem detail', action_item_id=actionitem.id)
    else:
        form = NewActionItemForm()

    context = {
        'form': form
    }

    return render(request, 'app/actionitems/new.html', context)

def newtask(request, project_id = None, action_item_id = None):
    user = request.user

    if request.method == 'POST':
        if project_id:
            form = NewProjectTaskForm(project_id, request.POST)

            task = form.save(commit=False)

            project = get_object_or_404(Project, id=project_id)

            task.to_project = project
            task.created_by = user
            task.save()

            return redirect('app:project detail', project_id=project_id)
        else:
            return redirect('app:project list')
    else:
        form = NewProjectTaskForm(project_id=project_id)

    context = {
        'form': form
    }

    return render(request, 'app/tasks/new.html', context)

def newstakeholder(request, project_id):
    user = request.user

    if request.method == 'POST':
        if project_id:
            form = NewProjectStakeholderForm(project_id, request.POST)

            stakeholder = form.save(commit=False)

            project = get_object_or_404(Project, id=project_id)

            stakeholder.to_project = project
            stakeholder.created_by = user
            stakeholder.save()

            return redirect('app:project detail', project_id=project_id)
        else:
            return redirect('app:stakeholder list')
    else:
        form = NewProjectStakeholderForm(project_id=project_id)

    context = {
        'form': form
    }

    return render(request, 'app/stakeholders/new.html', context)

def newcomment(request, action_item_id):
    user = request.user

    if request.method == 'POST':
        if action_item_id:
            form = NewCommentForm(request.POST)

            comment = form.save(commit=False)
            action_item = get_object_or_404(ActionItem, id=action_item_id)
            comment.to_action_item = action_item
            comment.created_by = user
            comment.save()

            return redirect('app:action item detail', action_item_id=action_item_id)
        else:
            return redirect('app:action item list')
    else:
        form = NewCommentForm()

    context = {
        'form': form
    }

    return(render(request, 'app/comments/new.html', context))
