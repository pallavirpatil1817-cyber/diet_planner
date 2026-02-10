from django.contrib import admin
from .models import HealthGoal, Recipe, MealPlan, DailyMeal, GroceryItem


@admin.register(HealthGoal)
class HealthGoalAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'goal', 'diet_type', 'daily_calories', 'created_at')
    list_filter = ('goal', 'diet_type', 'created_at')
    search_fields = ('user_name', 'allergies')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'meal_type', 'calories', 'protein_g', 'prep_time_min')
    list_filter = ('meal_type', 'diet_types')
    search_fields = ('name', 'description', 'ingredients')
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'description', 'meal_type')}),
        ('Nutrition', {'fields': ('calories', 'protein_g', 'carbs_g', 'fat_g')}),
        ('Cooking', {'fields': ('prep_time_min', 'ingredients', 'instructions')}),
        ('Diets', {'fields': ('diet_types',)}),
    )


@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('health_goal', 'start_date', 'created_at')
    list_filter = ('start_date', 'created_at')
    search_fields = ('health_goal__user_name',)
    readonly_fields = ('created_at',)


@admin.register(DailyMeal)
class DailyMealAdmin(admin.ModelAdmin):
    list_display = ('meal_plan', 'day_number', 'get_total_calories')
    list_filter = ('meal_plan', 'day_number')
    search_fields = ('meal_plan__health_goal__user_name',)

    def get_total_calories(self, obj):
        return obj.get_total_calories()
    get_total_calories.short_description = 'Total Calories'


@admin.register(GroceryItem)
class GroceryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'meal_plan', 'purchased')
    list_filter = ('category', 'purchased', 'meal_plan')
    search_fields = ('name',)
    readonly_fields = ('meal_plan',)
