from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('create/', views.create_group, name='create_group'),
    path('<uuid:group_id>/', views.group_detail, name='group_detail'),
    path('join/<uuid:invite_code>/', views.join_group, name='join_group'),
]