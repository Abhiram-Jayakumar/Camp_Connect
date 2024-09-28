from django.urls import path

from Camp import views




app_name = 'Camp'

urlpatterns = [
        path('Camp_home/', views.Camp_home, name='Camp_home'),
        path('Camp_register/', views.Camp_register, name='Camp_register'),
        path('add_facility', views.add_facility, name='add_facility'),
        path('Add_camp_profile/', views.Add_camp_profile, name='Add_camp_profile'),
        path('upload_images/', views.upload_images, name='upload_images'),
        path('add_package/', views.add_package, name='add_package'),
        path('packages/', views.view_all_packages, name='view_all_packages'),
        path('package/<int:package_id>/', views.view_package, name='view_package'),
        path('camper_view_bookings/', views.camper_view_bookings, name='camper_view_bookings'),
        path('submit_complaint/', views.submit_complaint, name='submit_complaint'),
        path('profile/',views. camp_profile_view, name='camp_profile'),
        path('profile/<int:camp_id>/edit/',views. edit_camp_details_view, name='edit_camp_details'),
        path('profile/<int:camp_id>/change-password/',views. change_camp_password_view, name='change_camp_password'),
        path('profile_update/', views.camp_profile_update_detailed, name='camp_profile_update'),
        path('profile_view_detailed/', views.profile_view_detailed, name='profile_view_detailed'),
        path('package/<int:package_id>/edit/',views.edit_camp_package, name='edit_package'),


]