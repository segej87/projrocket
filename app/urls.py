from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    path('', views.index, name='home'),
    path('projects', views.projectlist, name='project list'),
    path('projects/<uuid:project_id>', views.projectdetail, name='project detail'),
    path('projects/new', views.newproject, name='new project'),
    path('actionitems', views.actionitemlist, name='action item list'),
    path('actionitems/<uuid:action_item_id>', views.actionitemdetail, name='action item detail'),
    path('actionitems/new', views.newactionitem, name='new action item'),
    path('actionitems/new/<uuid:project_id>', views.newactionitem, name='new project action item'),
    path('people', views.peoplelist, name='people list'),
    path('people/<uuid:person_id>', views.persondetail, name='person detail'),
    path('people/new/<uuid:project_id>', views.newperson, name='new project person'),
    path('comments/new/<uuid:action_item_id>', views.newcomment, name='new comment'),
    path('stakeholders/new/<uuid:project_id>', views.newstakeholder, name='new project stakeholder'),
    path('tasks/new/<uuid:project_id>/', views.newtask, name='new project task'),
]
