from django.core.management.base import BaseCommand
from myapp.models import Recipe


class Command(BaseCommand):
    help = 'Load initial recipes into the database'

    def handle(self, *args, **options):
        recipes = [
            # Breakfast
            {
                'name': 'Oatmeal with Berries',
                'description': 'Healthy oatmeal topped with fresh berries and honey',
                'calories': 350,
                'protein_g': 8,
                'carbs_g': 60,
                'fat_g': 5,
                'prep_time_min': 10,
                'ingredients': 'Oats, milk, berries, honey, almonds',
                'instructions': '1. Cook oats according to package directions\n2. Top with fresh berries\n3. Drizzle with honey\n4. Sprinkle almonds',
                'diet_types': 'vegan, vegetarian',
                'meal_type': 'breakfast',
            },
            {
                'name': 'Scrambled Eggs with Toast',
                'description': 'Fluffy scrambled eggs with whole grain toast',
                'calories': 320,
                'protein_g': 15,
                'carbs_g': 35,
                'fat_g': 10,
                'prep_time_min': 15,
                'ingredients': 'Eggs, whole grain bread, butter, salt, pepper',
                'instructions': '1. Toast bread\n2. Scramble eggs in butter\n3. Season with salt and pepper\n4. Serve together',
                'diet_types': 'vegetarian',
                'meal_type': 'breakfast',
            },
            {
                'name': 'Greek Yogurt Parfait',
                'description': 'Creamy yogurt layered with granola and fruit',
                'calories': 280,
                'protein_g': 12,
                'carbs_g': 45,
                'fat_g': 4,
                'prep_time_min': 5,
                'ingredients': 'Greek yogurt, granola, berries, honey',
                'instructions': '1. Layer yogurt in a bowl\n2. Add granola\n3. Top with fresh berries\n4. Drizzle honey',
                'diet_types': 'vegetarian',
                'meal_type': 'breakfast',
            },
            # Lunch
            {
                'name': 'Grilled Chicken Salad',
                'description': 'Fresh salad with grilled chicken breast and mixed greens',
                'calories': 420,
                'protein_g': 35,
                'carbs_g': 25,
                'fat_g': 15,
                'prep_time_min': 25,
                'ingredients': 'Chicken breast, mixed greens, tomatoes, cucumbers, olive oil, lemon juice',
                'instructions': '1. Grill chicken until cooked\n2. Slice chicken\n3. Mix greens with vegetables\n4. Top with chicken\n5. Dress with olive oil and lemon',
                'diet_types': 'keto',
                'meal_type': 'lunch',
            },
            {
                'name': 'Quinoa Buddha Bowl',
                'description': 'Nutrient-packed bowl with quinoa, roasted veggies, and tahini dressing',
                'calories': 450,
                'protein_g': 15,
                'carbs_g': 55,
                'fat_g': 16,
                'prep_time_min': 30,
                'ingredients': 'Quinoa, roasted vegetables, tahini, lemon juice, chickpeas, spinach',
                'instructions': '1. Cook quinoa\n2. Roast vegetables at 400F for 25 minutes\n3. Mix tahini with lemon juice\n4. Assemble bowl\n5. Drizzle with dressing',
                'diet_types': 'vegan, vegetarian',
                'meal_type': 'lunch',
            },
            {
                'name': 'Turkey Sandwich',
                'description': 'Lean turkey breast on whole wheat bread with veggies',
                'calories': 380,
                'protein_g': 28,
                'carbs_g': 40,
                'fat_g': 8,
                'prep_time_min': 10,
                'ingredients': 'Turkey breast, whole wheat bread, lettuce, tomato, mustard',
                'instructions': '1. Toast bread lightly\n2. Layer turkey\n3. Add lettuce and tomato\n4. Spread mustard\n5. Cut and serve',
                'diet_types': 'balanced',
                'meal_type': 'lunch',
            },
            # Dinner
            {
                'name': 'Baked Salmon with Veggies',
                'description': 'Omega-3 rich salmon baked with roasted vegetables',
                'calories': 520,
                'protein_g': 40,
                'carbs_g': 30,
                'fat_g': 22,
                'prep_time_min': 35,
                'ingredients': 'Salmon fillet, broccoli, bell peppers, olive oil, garlic, lemon',
                'instructions': '1. Preheat oven to 400F\n2. Place salmon on baking sheet\n3. Add vegetables\n4. Drizzle with olive oil\n5. Add garlic and lemon\n6. Bake 20-25 minutes',
                'diet_types': 'keto, paleo',
                'meal_type': 'dinner',
            },
            {
                'name': 'Spaghetti with Marinara',
                'description': 'Classic pasta with homemade tomato sauce',
                'calories': 480,
                'protein_g': 15,
                'carbs_g': 70,
                'fat_g': 10,
                'prep_time_min': 30,
                'ingredients': 'Pasta, tomatoes, garlic, onion, olive oil, basil, oregano',
                'instructions': '1. Cook pasta according to directions\n2. Sauté garlic and onion\n3. Add tomatoes\n4. Simmer 15 minutes\n5. Add basil and oregano\n6. Serve with pasta',
                'diet_types': 'vegan, vegetarian',
                'meal_type': 'dinner',
            },
            {
                'name': 'Grilled Chicken Breast with Rice',
                'description': 'Lean protein with brown rice and steamed vegetables',
                'calories': 550,
                'protein_g': 38,
                'carbs_g': 65,
                'fat_g': 8,
                'prep_time_min': 40,
                'ingredients': 'Chicken breast, brown rice, broccoli, carrots, olive oil, garlic',
                'instructions': '1. Cook brown rice\n2. Grill chicken until cooked\n3. Steam vegetables\n4. Combine on plate\n5. Drizzle with olive oil',
                'diet_types': 'balanced, keto',
                'meal_type': 'dinner',
            },
            {
                'name': 'Vegetable Stir Fry',
                'description': 'Colorful mix of fresh vegetables in light sauce',
                'calories': 320,
                'protein_g': 12,
                'carbs_g': 45,
                'fat_g': 8,
                'prep_time_min': 25,
                'ingredients': 'Mixed vegetables, soy sauce, garlic, ginger, sesame oil, rice',
                'instructions': '1. Cook rice\n2. Heat oil in wok\n3. Add garlic and ginger\n4. Add vegetables\n5. Stir fry 10-12 minutes\n6. Add soy sauce\n7. Serve over rice',
                'diet_types': 'vegan, vegetarian',
                'meal_type': 'dinner',
            },
            # Snacks
            {
                'name': 'Almonds & Berries',
                'description': 'Protein-rich almonds with fresh berries',
                'calories': 180,
                'protein_g': 6,
                'carbs_g': 15,
                'fat_g': 12,
                'prep_time_min': 0,
                'ingredients': 'Almonds, mixed berries',
                'instructions': '1. Portion almonds\n2. Add berries\n3. Mix and enjoy',
                'diet_types': 'vegan, vegetarian, keto',
                'meal_type': 'snack',
            },
            {
                'name': 'Hummus with Vegetables',
                'description': 'Creamy hummus with fresh veggie sticks',
                'calories': 160,
                'protein_g': 6,
                'carbs_g': 16,
                'fat_g': 6,
                'prep_time_min': 5,
                'ingredients': 'Hummus, carrots, celery, bell peppers',
                'instructions': '1. Cut vegetables into sticks\n2. Portion hummus\n3. Serve with veggies',
                'diet_types': 'vegan, vegetarian',
                'meal_type': 'snack',
            },
            {
                'name': 'Protein Bar',
                'description': 'Convenient high-protein snack bar',
                'calories': 200,
                'protein_g': 20,
                'carbs_g': 15,
                'fat_g': 6,
                'prep_time_min': 0,
                'ingredients': 'Protein bar',
                'instructions': '1. Open wrapper\n2. Enjoy',
                'diet_types': 'balanced',
                'meal_type': 'snack',
            },
            {
                'name': 'Apple with Peanut Butter',
                'description': 'Fresh apple with creamy peanut butter',
                'calories': 190,
                'protein_g': 7,
                'carbs_g': 20,
                'fat_g': 8,
                'prep_time_min': 2,
                'ingredients': 'Apple, peanut butter',
                'instructions': '1. Slice apple\n2. Serve with peanut butter',
                'diet_types': 'vegan, vegetarian',
                'meal_type': 'snack',
            },
        ]

        for recipe_data in recipes:
            recipe, created = Recipe.objects.get_or_create(
                name=recipe_data['name'],
                defaults=recipe_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created recipe: {recipe.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Recipe already exists: {recipe.name}')
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded all recipes'))
