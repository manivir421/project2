
#comp 3450 <Ashima,ripan>-->
from django.urls import path
from .views import home , detail,posts
urlpatterns = [
    path("",home, name="home"),
    path("detail/", detail,name="detail"),
    path("posts/"posts,name="posts")
]