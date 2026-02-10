from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create-goal/', views.create_health_goal, name='create_health_goal'),
    path('meal-plan/<int:pk>/', views.view_meal_plan, name='view_meal_plan'),
    path('grocery-list/<int:pk>/', views.view_grocery_list, name='view_grocery_list'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('grocery/<int:pk>/toggle/', views.mark_grocery_purchased, name='mark_grocery_purchased'),
]
