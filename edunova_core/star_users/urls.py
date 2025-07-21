from django.urls import path,include
from . import views  # your app's views
from rest_framework.authtoken.views import obtain_auth_token
from star_users import views as star_users_views  # star_users app views
from django.contrib import admin

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', star_users_views.about_view, name='about'),  # correct usage
    path('admin/', admin.site.urls),
    # ... your other URLs ...
    path('api/login/', obtain_auth_token, name='api_token_auth'),  # ✅ Add this line


]
