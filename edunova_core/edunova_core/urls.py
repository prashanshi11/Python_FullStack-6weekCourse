# edunova_core/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token  # Token-based auth

urlpatterns = [
    # 🛠️ Admin Panel
    path('admin/', admin.site.urls),

    # 🔐 Password Reset Flow
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # 🔑 Authentication & Modules
    path('', include('star_users.urls')),                # 🌟 Custom Auth (Login/Register)
    path('courses/', include('course_galaxy.urls')),     # 📚 Course Module
    path('quiz/', include('quizverse.urls')),            # 🧠 Quiz Module
    path('api/', include('nova_api.urls')),              # 🌐 API Routes

    # 🔐 Token Authentication Endpoint
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # 🌐 DRF Browsable API (Login/Logout)
    path('api-auth/', include('rest_framework.urls')),
]

# 🖼️ Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
