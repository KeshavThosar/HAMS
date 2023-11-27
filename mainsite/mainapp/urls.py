from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('store/', views.store, name='store'),
    path('orders/', views.orders, name='orders'),
    path('addAsset/', views.addAsset, name='addAsset'),
    path('api/getAssetName', views.getAsset, name='getAssetName'),

]