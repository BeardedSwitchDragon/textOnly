#community urlresolvers
from django.urls import path, include
from . import views

app_name = "communities"

urlpatterns = [
    path("", views.ListCommunities.as_view(), name="all"),
    path("new/", views.CreateCommunity.as_view(), name="create"),
    path("posts/in/<slug>/", views.SingleCommunity.as_view(),name="single"),
    path("join/<slug>/", views.JoinCommunity.as_view(), name="join"),
    path("leave/<slug>/", views.LeaveCommunity.as_view(), name="leave")
]
#README: if not working, add /$ to the end of single community url
