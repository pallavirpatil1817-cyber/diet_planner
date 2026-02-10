from django.db import models

class HealthGoal(models.Model):
    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('maintenance', 'Maintenance'),
        ('energy', 'Increase Energy'),
        ('general_health', 'General Health'),
    ]
    
    DIET_TYPE_CHOICES = [
        ('balanced', 'Balanced Diet'),
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('keto', 'Keto'),
        ('paleo', 'Paleo'),
        ('gluten_free', 'Gluten Free'),
        ('mediterranean', 'Mediterranean'),
    ]

    user_name = models.CharField(max_length=100)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    diet_type = models.CharField(max_length=20, choices=DIET_TYPE_CHOICES)
    daily_calories = models.IntegerField(default=2000)
    allergies = models.TextField(blank=True, help_text="Comma-separated list of allergies")
    dislikes = models.TextField(blank=True, help_text="Comma-separated list of foods to avoid")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_name} - {self.get_goal_display()}"

    class Meta:
        verbose_name_plural = "Health Goals"


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    calories = models.IntegerField()
    protein_g = models.FloatField(default=0)  # grams
    carbs_g = models.FloatField(default=0)
    fat_g = models.FloatField(default=0)
    prep_time_min = models.IntegerField(default=15)  # minutes
    ingredients = models.TextField(help_text="Comma-separated ingredients")
    instructions = models.TextField()
    diet_types = models.CharField(
        max_length=100,
        blank=True,
        help_text="Comma-separated diet types (e.g., vegan, keto)"
    )
    meal_type = models.CharField(
        max_length=20,
        choices=[
            ('breakfast', 'Breakfast'),
            ('lunch', 'Lunch'),
            ('dinner', 'Dinner'),
            ('snack', 'Snack'),
        ]
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['meal_type', 'name']


class MealPlan(models.Model):
    health_goal = models.ForeignKey(HealthGoal, on_delete=models.CASCADE)
    start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Meal Plan for {self.health_goal.user_name} - {self.start_date}"

    class Meta:
        ordering = ['-start_date']


class DailyMeal(models.Model):
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='meals')
    day_number = models.IntegerField(choices=[(i, f"Day {i}") for i in range(1, 8)])
    breakfast = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, blank=True, related_name='breakfast_meals')
    lunch = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, blank=True, related_name='lunch_meals')
    dinner = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, blank=True, related_name='dinner_meals')
    snack = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, blank=True, related_name='snack_meals')

    def __str__(self):
        return f"Day {self.day_number} - {self.meal_plan.health_goal.user_name}"

    class Meta:
        ordering = ['meal_plan', 'day_number']
        unique_together = ('meal_plan', 'day_number')

    def get_total_calories(self):
        total = 0
        for meal in [self.breakfast, self.lunch, self.dinner, self.snack]:
            if meal:
                total += meal.calories
        return total

    def get_total_nutrition(self):
        nutrition = {'protein': 0, 'carbs': 0, 'fat': 0}
        for meal in [self.breakfast, self.lunch, self.dinner, self.snack]:
            if meal:
                nutrition['protein'] += meal.protein_g
                nutrition['carbs'] += meal.carbs_g
                nutrition['fat'] += meal.fat_g
        return nutrition


class GroceryItem(models.Model):
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='grocery_items')
    name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=100, help_text="e.g., 2 kg, 1 bunch, 1 liter")
    category = models.CharField(
        max_length=50,
        choices=[
            ('produce', 'Produce'),
            ('dairy', 'Dairy'),
            ('meat', 'Meat & Fish'),
            ('grains', 'Grains & Cereals'),
            ('pantry', 'Pantry'),
            ('frozen', 'Frozen'),
            ('beverages', 'Beverages'),
        ]
    )
    estimated_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'name']
