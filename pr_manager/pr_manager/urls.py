"""
URL configuration for pr_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from django.urls import re_path
from pr.views import homepage, contactpage
from pr.views import show_recipes as recipes_list
from pr.views import (
    RecipeView,
)
from pr.views import loginview2, logout_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('contact/', contactpage, name='contactpage'),
    path('api/login/',obtain_auth_token ,name='login'),
    path('login/', loginview2, name='loginview'),
    path('logout/', logout_view, name='logout'),
    path('recipes/', recipes_list, name='recipes_list'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api', RecipeView.as_view()),

]
