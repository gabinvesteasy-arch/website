from django.contrib import admin
from django.urls import path
from accounts import views as account_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Auth (custom views)
    path('login/', account_views.login_view, name='login'),
    path('logout/', account_views.logout_view, name='logout'),
    path('signup/', account_views.signup_view, name='signup'),

    # Dashboard (homepage after login)
    path('', account_views.dashboard, name='dashboard'),

    # Banking views
    path('transfer/', account_views.transfer, name='transfer'),

    # Temporary admin creation (REMOVE AFTER USE)
    path('createadmin/', account_views.create_admin, name='create_admin'),
]