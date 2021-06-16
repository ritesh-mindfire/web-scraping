from django.urls import path
from products import views
# from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)