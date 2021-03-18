from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('projects', views.projectlist, name='project list'),
    path('projects/<uuid:project_id>/', views.projectdetail, name='project detail'),
    path('actionitems/<uuid:action_item_id>/', views.actionitemdetail, name='action item detail')
]
