from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('accounts/login/', views.login_view, name='login'),

    # Password reset URLS
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'), 
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Other URLS
    path('', views.signup, name='signup'), # Redirect to signup page by default
    path('home/', views.home, name= 'home'),
    path('search/', views.search, name='search'),
    path('ticket/booking/<int:route_id>/', views.ticket_booking, name='ticket_booking'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('ticket/history/', views.ticket_history, name='ticket_history'),
    path('cancel_ticket/', views.cancel_ticket, name='cancel_ticket'),
    path('account/', views.account, name='account'),
    path('logout/', views.logout_view, name='logout'), # URL for logout
]