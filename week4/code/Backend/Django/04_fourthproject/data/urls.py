from django.urls import path
from . import views

urlpatterns = [
    path('', views.data_views, name='data_views')  # ✅ correct
 # Maps the root URL of the app to the view
]
