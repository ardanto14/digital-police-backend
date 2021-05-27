"""digitalpolice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from main.serializers import HistorySerializer
from django.urls import path
from .views import CitySpecificView, HistorySpecificView, HistoryView, VideoView, video_view, HistoryFilterByCity, CityView

urlpatterns = [
    path('', video_view, name='main'),
    path('city/', CityView.as_view()),
    path('city/<int:id>/', CitySpecificView.as_view()),
    path('history/by_city/<int:city_id>/', HistoryFilterByCity.as_view()),
    path('video/', VideoView.as_view()),
    path('history/', HistoryView.as_view()),
    path('history/<int:id>/', HistorySpecificView.as_view()),
]
