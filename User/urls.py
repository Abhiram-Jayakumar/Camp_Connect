from django.urls import path

from User import views




app_name = 'User'

urlpatterns = [
        path('User_home/', views.User_home, name='User_home'),
        path('Index/', views.Index, name='Index'),
        path('User_register/', views.User_register, name='User_register'),
        path('Login/', views.Login, name='Login'),
        path('packages/', views.view_all_packages, name='view_all_packages'),
        path('view_package/<int:package_id>/', views.view_Single_package, name='view_Single_package'),
        path('book/<int:package_id>/', views.book_package, name='book_package'),
        path('view_bookings/', views.view_bookings, name='view_bookings'),
        path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
        path('process_payment/<int:booking_id>/', views.process_payment, name='process_payment'),
        path('submit_complaint/', views.submit_complaint, name='submit_complaint'),
        path('profile/', views.view_profile, name='view_profile'),
        path('update-details/', views.update_details, name='update_details'),
        path('update-password/', views.update_password, name='update_password'),
        path('camp/<int:camp_id>/', views.camp_gallery, name='camp_gallery'),
        path('feedback/', views.add_feedback, name='add_feedback'),

]