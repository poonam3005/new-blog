from unicodedata import name
from .import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index' ),
    path('registration', views.registration, name='registration' ),
    path('login', views.loginuser, name='login' ),
    path('logout', views.logoutuser, name='logout' ),
    path('selected_blog/<id>', views.selected_blog,name='selected_blog'),
    path('upload-blog',views.upload_blog,name='upload-blog'),
    path('search',views.search,name='search'),
    path('like_blog/<int:id>',views.like_blog,name='like_blog'),
    path('profile',views.profile,name='profile'),
    path('edit_blog/<int:id>',views.edit_blog,name='edit_blog'),
    path('delete_blog/<int:id>',views.delete_blog,name='delete_blog'),
    path('category/<str:cat>',views.category,name='category')
]