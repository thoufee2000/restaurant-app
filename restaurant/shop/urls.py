from django.urls import path
from . import views
app_name='shop'
urlpatterns = [
    path('',views.home,name='home'),
    path('menu/',views.menu,name='menu'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path('logout',views.user_logout,name='logout'),
    path('search',views.search_menu,name='search')

]