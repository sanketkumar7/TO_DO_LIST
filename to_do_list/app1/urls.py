from django.urls import path
from . import views

app_name='app1'

urlpatterns = [
    path('sign-in/',views.signin_register,name='sign_in'),
    path('',views.all_tasks,name='all_tasks'),
    path('delete-task/<int:pk>',views.delete_task,name='delete_task'),
    path('update-task/<int:pk>',views.update_task,name='update_task'),
    path('update-title/',views.update_title,name='update_title'),
    path('logout/',views.logout,name='logout'),

    #ajax calls
    path('update-completed-status',views.update_completed_status,name='update_completed_status')
]
