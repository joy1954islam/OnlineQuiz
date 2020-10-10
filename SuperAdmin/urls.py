from django.urls import path

from SuperAdmin import views

urlpatterns = [
    path('SuperAdminHome/', views.SuperAdminHome, name='SuperAdminHome'),
    path('SuperAdminProfile/',views.SuperAdminProfile, name='SuperAdminProfile'),
    path('users/',views.users_list, name='users_list'),
    path('users_views/<int:pk>/',views.users_view, name='users_view'),
    path('users_updae/<int:pk>/',views.users_update, name='users_update'),

    path('change/password/', views.ChangePasswordView.as_view(), name='SuperAdmin_change_password'),
    path('change/email/', views.ChangeEmailView.as_view(), name='SuperAdmin_change_email'),
    path('change/email/<code>/', views.ChangeEmailActivateView.as_view(), name='change_email_activation'),
]