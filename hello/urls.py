from django.urls import path
from hello.views import home_views, about_views, Map_views

urlpatterns = [
    path("", home_views, name="home"),      #default page
    path("home/", home_views, name="home"),
    path("about/",about_views,name="about"),
    path("map/",Map_views,name="map")
]