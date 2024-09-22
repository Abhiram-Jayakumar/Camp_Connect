from django.urls import path

from Admin import views



app_name = 'Admin'

urlpatterns = [
        path('Admin_home/', views.Admin_home, name='Admin_home'),
        path('view_registered_Camp/', views.view_registered_Camp, name='view_registered_Camp'),
        path('handle_camp_registration/<int:camp_id>/<str:action>/', views.handle_camp_registration, name='handle_camp_registration'),
        path('complaints/', views.complaint_list, name='complaint_list'),
        path('resolve_complaint/<int:complaint_id>/', views.resolve_complaint, name='resolve_complaint'),
        path('Graph/', views.Graph, name='Graph'),
]