from django.urls import path

from .views import index, search_item

urlpatterns = [
    path("", index, name="home"),
    path("search/", search_item, name="search")
]