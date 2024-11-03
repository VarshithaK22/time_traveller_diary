from django.urls import path
from . import views, entry_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
                                                  next_page='/',
                                                  http_method_names=['get', 'post'],
                                                #   template_name='logout.html'
                                                  ), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('', views.EntryListView.as_view(), name='home'),
    path('new/', entry_views.EntryCreateView.as_view(), name='entry_create'),
    
]