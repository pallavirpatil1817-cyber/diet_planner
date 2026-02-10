from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime, timedelta
from collections import defaultdict
from .models import HealthGoal, Recipe, MealPlan, DailyMeal, GroceryItem
from .forms import HealthGoalForm, RecipeForm
import random


def create_health_goal(request):
    """Create a new health goal and generate meal plan"""
    if request.method == 'POST':
        form = HealthGoalForm(request.POST)
        if form.is_valid():
            health_goal = form.save()
            
            # Create meal plan
            meal_plan = MealPlan.objects.create(
                health_goal=health_goal,
                start_date=datetime.now().date()
            )
            
            # Generate 7-day meal plan
            generate_meal_plan(meal_plan, health_goal)
            
            # Generate grocery list
            generate_grocery_list(meal_plan)
            
            messages.success(request, 'Health goal created! Meal plan generated.')
            return redirect('view_meal_plan', pk=meal_plan.pk)
    else:
        form = HealthGoalForm()
    
    return render(request, 'myapp/create_health_goal.html', {'form': form})


def generate_meal_plan(meal_plan, health_goal):
    """Generate intelligent 7-day meal plan based on health goals"""
    
    # Get recipes matching the user's diet type
    diet_types = health_goal.diet_type
    breakfast_recipes = Recipe.objects.filter(
        meal_type='breakfast'
    ).exclude(
        diet_types__icontains='_not_' + diet_types
    )
    
    lunch_recipes = Recipe.objects.filter(
        meal_type='lunch'
    )
    
    dinner_recipes = Recipe.objects.filter(
        meal_type='dinner'
    )
    
    snack_recipes = Recipe.objects.filter(
        meal_type='snack'
    )
    
    # Filter by calories based on health goal
    if health_goal.daily_calories > 0:
        target_per_meal = health_goal.daily_calories / 3.5
    else:
        target_per_meal = 500
    
    # Create 7 daily meals
    for day in range(1, 8):
        daily_meal = DailyMeal.objects.create(
            meal_plan=meal_plan,
            day_number=day,
            breakfast=select_random_recipe(breakfast_recipes, target_per_meal * 0.25) or breakfast_recipes.first(),
            lunch=select_random_recipe(lunch_recipes, target_per_meal * 0.35) or lunch_recipes.first(),
            dinner=select_random_recipe(dinner_recipes, target_per_meal * 0.35) or dinner_recipes.first(),
            snack=select_random_recipe(snack_recipes, target_per_meal * 0.05) or snack_recipes.first(),
        )


def select_random_recipe(recipes, target_calories):
    """Select a random recipe close to target calories"""
    if not recipes.exists():
        return None
    
    # Try to find recipes within 20% of target calories
    similar = recipes.filter(
        calories__gte=target_calories * 0.8,
        calories__lte=target_calories * 1.2
    )
    
    if similar.exists():
        return similar.order_by('?').first()
    
    return recipes.order_by('?').first()


def generate_grocery_list(meal_plan):
    """Generate grocery list from meal plan"""
    
    grocery_items = defaultdict(list)
    
    # Collect all ingredients from meals
    for daily_meal in meal_plan.meals.all():
        for meal in [daily_meal.breakfast, daily_meal.lunch, daily_meal.dinner, daily_meal.snack]:
            if meal:
                ingredients = [ing.strip() for ing in meal.ingredients.split(',')]
                for ingredient in ingredients:
                    # Parse quantity if present (simple parsing)
                    parts = ingredient.rsplit(' ', 1)
                    if len(parts) == 2 and parts[1].isdigit():
                        item_name = parts[0]
                        quantity = int(parts[1])
                    else:
                        item_name = ingredient
                        quantity = 1
                    
                    grocery_items[item_name].append(quantity)
    
    # Create grocery items, consolidating duplicates
    category_map = {
        'vegetable': 'produce',
        'fruit': 'produce',
        'chicken': 'meat',
        'beef': 'meat',
        'fish': 'meat',
        'milk': 'dairy',
        'cheese': 'dairy',
        'yogurt': 'dairy',
        'rice': 'grains',
        'bread': 'grains',
        'oil': 'pantry',
        'salt': 'pantry',
    }
    
    for item_name, quantities in grocery_items.items():
        total_quantity = sum(quantities)
        
        # Determine category
        category = 'pantry'
        item_lower = item_name.lower()
        for keyword, cat in category_map.items():
            if keyword in item_lower:
                category = cat
                break
        
        GroceryItem.objects.create(
            meal_plan=meal_plan,
            name=item_name,
            quantity=f"{total_quantity} units",
            category=category
        )


def view_meal_plan(request, pk):
    """View the generated meal plan"""
    meal_plan = get_object_or_404(MealPlan, pk=pk)
    daily_meals = meal_plan.meals.all().order_by('day_number')
    
    context = {
        'meal_plan': meal_plan,
        'daily_meals': daily_meals,
        'health_goal': meal_plan.health_goal,
    }
    
    return render(request, 'myapp/meal_plan.html', context)


def view_grocery_list(request, pk):
    """View grocery list for meal plan"""
    meal_plan = get_object_or_404(MealPlan, pk=pk)
    
    # Group items by category
    items_by_category = defaultdict(list)
    for item in meal_plan.grocery_items.all():
        items_by_category[item.get_category_display()].append(item)
    
    total_price = sum(item.estimated_price for item in meal_plan.grocery_items.all())
    
    context = {
        'meal_plan': meal_plan,
        'items_by_category': dict(items_by_category),
        'total_price': total_price,
    }
    
    return render(request, 'myapp/grocery_list.html', context)


def dashboard(request):
    """Dashboard showing all health goals and meal plans"""
    health_goals = HealthGoal.objects.all().order_by('-created_at')
    meal_plans = MealPlan.objects.all().order_by('-created_at')[:5]
    
    context = {
        'health_goals': health_goals,
        'meal_plans': meal_plans,
    }
    
    return render(request, 'myapp/dashboard.html', context)


def recipe_list(request):
    """List all recipes"""
    recipes = Recipe.objects.all()
    meal_type_filter = request.GET.get('meal_type')
    
    if meal_type_filter:
        recipes = recipes.filter(meal_type=meal_type_filter)
    
    context = {
        'recipes': recipes,
        'meal_types': Recipe._meta.get_field('meal_type').choices,
    }
    
    return render(request, 'myapp/recipe_list.html', context)


def recipe_detail(request, pk):
    """View recipe details"""
    recipe = get_object_or_404(Recipe, pk=pk)
    
    context = {
        'recipe': recipe,
        'ingredients': [ing.strip() for ing in recipe.ingredients.split(',')],
    }
    
    return render(request, 'myapp/recipe_detail.html', context)


def mark_grocery_purchased(request, pk):
    """Mark grocery item as purchased"""
    item = get_object_or_404(GroceryItem, pk=pk)
    item.purchased = not item.purchased
    item.save()
    
    return redirect('view_grocery_list', pk=item.meal_plan.pk)
