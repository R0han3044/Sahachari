import os
import json
import random
import streamlit as st
import requests

class RecipeGenerator:
    """Recipe generation service for creating traditional and modern dishes"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY", None)
        self.spoonacular_api_key = os.getenv("SPOONACULAR_API_KEY", None)
        
        # Load recipe templates and patterns
        self.recipe_templates = self._load_recipe_templates()
        self.traditional_dishes = self._load_traditional_dishes()
        self.cooking_methods = self._load_cooking_methods()
        
    def generate_from_ingredients(self, ingredients):
        """
        Generate recipes based on available ingredients
        
        Args:
            ingredients (list): List of available ingredients
            
        Returns:
            list: List of generated recipes
        """
        try:
            # Try external API first
            if self.spoonacular_api_key:
                return self._generate_with_spoonacular(ingredients)
            elif self.openai_api_key:
                return self._generate_with_openai(ingredients)
            else:
                # Use local template-based generation
                return self._generate_with_templates(ingredients)
                
        except Exception as e:
            st.error(f"Recipe generation failed: {str(e)}")
            return []
    
    def generate_by_type(self, recipe_type):
        """
        Generate recipe by type (traditional, modern, etc.)
        
        Args:
            recipe_type (str): Type of recipe to generate
            
        Returns:
            dict: Generated recipe
        """
        try:
            if recipe_type.lower() == 'traditional':
                return self._generate_traditional_recipe()
            elif recipe_type.lower() == 'modern':
                return self._generate_modern_recipe()
            elif recipe_type.lower() == 'fusion':
                return self._generate_fusion_recipe()
            elif recipe_type.lower() == 'healthy':
                return self._generate_healthy_recipe()
            elif recipe_type.lower() == 'quick':
                return self._generate_quick_recipe()
            else:
                return self._generate_random_recipe()
                
        except Exception as e:
            st.error(f"Recipe generation failed: {str(e)}")
            return None
    
    def suggest_recipes(self, ingredients):
        """
        Suggest existing recipes that can be made with given ingredients
        
        Args:
            ingredients (list): Available ingredients
            
        Returns:
            list: List of suggested recipe names
        """
        suggestions = []
        
        # Simple ingredient matching
        for recipe in self.traditional_dishes:
            recipe_ingredients = recipe.get('ingredients', [])
            
            # Check how many ingredients match
            matches = sum(1 for ing in ingredients 
                         if any(ing.lower() in recipe_ing.lower() 
                               for recipe_ing in recipe_ingredients))
            
            # If at least 50% of ingredients match, suggest the recipe
            if matches >= len(recipe_ingredients) * 0.5:
                suggestions.append(recipe['name'])
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def _generate_with_spoonacular(self, ingredients):
        """Generate recipes using Spoonacular API"""
        url = "https://api.spoonacular.com/recipes/findByIngredients"
        
        params = {
            'apiKey': self.spoonacular_api_key,
            'ingredients': ','.join(ingredients),
            'number': 3,
            'ranking': 1,
            'ignorePantry': True
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            recipes_data = response.json()
            recipes = []
            
            for recipe_data in recipes_data:
                # Get detailed recipe information
                recipe_detail = self._get_spoonacular_recipe_detail(recipe_data['id'])
                if recipe_detail:
                    recipes.append(recipe_detail)
            
            return recipes
        else:
            raise Exception(f"Spoonacular API failed with status {response.status_code}")
    
    def _get_spoonacular_recipe_detail(self, recipe_id):
        """Get detailed recipe information from Spoonacular"""
        url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
        
        params = {
            'apiKey': self.spoonacular_api_key,
            'includeNutrition': False
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract instructions
            instructions = []
            if 'analyzedInstructions' in data and data['analyzedInstructions']:
                for instruction_group in data['analyzedInstructions']:
                    for step in instruction_group.get('steps', []):
                        instructions.append(f"{step['number']}. {step['step']}")
            
            return {
                'name': data.get('title', 'Unknown Recipe'),
                'ingredients': [ing['original'] for ing in data.get('extendedIngredients', [])],
                'instructions': ' '.join(instructions),
                'cooking_time': f"{data.get('readyInMinutes', 'Unknown')} minutes",
                'servings': data.get('servings', 'Unknown'),
                'source': 'Spoonacular'
            }
        
        return None
    
    def _generate_with_openai(self, ingredients):
        """Generate recipes using OpenAI API"""
        # This would require OpenAI API implementation
        # For now, fall back to template-based generation
        return self._generate_with_templates(ingredients)
    
    def _generate_with_templates(self, ingredients):
        """Generate recipes using local templates"""
        recipes = []
        
        # Filter templates based on available ingredients
        suitable_templates = []
        for template in self.recipe_templates:
            template_ingredients = template.get('required_ingredients', [])
            
            # Check if we have enough ingredients
            available_count = sum(1 for ing in template_ingredients
                                if any(ing.lower() in avail_ing.lower() 
                                      for avail_ing in ingredients))
            
            if available_count >= len(template_ingredients) * 0.6:  # 60% match
                suitable_templates.append(template)
        
        # Generate recipes from suitable templates
        for template in suitable_templates[:3]:  # Max 3 recipes
            recipe = self._generate_from_template(template, ingredients)
            if recipe:
                recipes.append(recipe)
        
        return recipes
    
    def _generate_from_template(self, template, available_ingredients):
        """Generate a recipe from a template"""
        recipe = {
            'name': template['name'],
            'type': template.get('type', 'traditional'),
            'cooking_time': template.get('cooking_time', '30 minutes'),
            'difficulty': template.get('difficulty', 'medium'),
            'servings': template.get('servings', '4'),
            'source': 'Generated'
        }
        
        # Build ingredients list
        ingredients_list = []
        for req_ing in template.get('required_ingredients', []):
            # Try to match with available ingredients
            for avail_ing in available_ingredients:
                if req_ing.lower() in avail_ing.lower() or avail_ing.lower() in req_ing.lower():
                    ingredients_list.append(avail_ing)
                    break
            else:
                ingredients_list.append(req_ing)  # Add required ingredient anyway
        
        # Add optional ingredients if available
        for opt_ing in template.get('optional_ingredients', []):
            for avail_ing in available_ingredients:
                if opt_ing.lower() in avail_ing.lower():
                    ingredients_list.append(avail_ing)
                    break
        
        recipe['ingredients'] = ', '.join(ingredients_list)
        recipe['instructions'] = template.get('instructions', 'Instructions not available')
        
        return recipe
    
    def _generate_traditional_recipe(self):
        """Generate a traditional recipe"""
        if self.traditional_dishes:
            recipe = random.choice(self.traditional_dishes)
            return {
                'name': recipe['name'],
                'type': 'Traditional',
                'ingredients': ', '.join(recipe.get('ingredients', [])),
                'instructions': recipe.get('instructions', 'Instructions not available'),
                'cooking_time': recipe.get('cooking_time', '45 minutes'),
                'difficulty': recipe.get('difficulty', 'medium'),
                'cultural_significance': recipe.get('cultural_significance', ''),
                'source': 'Traditional Recipe Database'
            }
        return None
    
    def _generate_modern_recipe(self):
        """Generate a modern recipe"""
        modern_techniques = [
            'sous vide', 'air frying', 'pressure cooking', 'steaming',
            'grilling', 'roasting', 'quick sautéing'
        ]
        
        modern_ingredients = [
            'quinoa', 'avocado', 'kale', 'chia seeds', 'coconut oil',
            'almond milk', 'Greek yogurt', 'sweet potato', 'spinach'
        ]
        
        return {
            'name': f"Modern {random.choice(['Bowl', 'Wrap', 'Salad', 'Stir-fry'])}",
            'type': 'Modern',
            'ingredients': ', '.join(random.sample(modern_ingredients, 5)),
            'instructions': f"1. Prepare ingredients using {random.choice(modern_techniques)}. 2. Combine in a modern style. 3. Season and serve fresh.",
            'cooking_time': '20 minutes',
            'difficulty': 'easy',
            'health_benefits': 'High in nutrients and antioxidants',
            'source': 'Modern Recipe Generator'
        }
    
    def _generate_fusion_recipe(self):
        """Generate a fusion recipe"""
        cuisines = ['Indian', 'Italian', 'Mexican', 'Asian', 'Mediterranean']
        fusion_pair = random.sample(cuisines, 2)
        
        return {
            'name': f"{fusion_pair[0]}-{fusion_pair[1]} Fusion Dish",
            'type': 'Fusion',
            'ingredients': 'Mix of traditional ingredients from both cuisines',
            'instructions': f"Combine cooking techniques and flavors from {fusion_pair[0]} and {fusion_pair[1]} cuisines.",
            'cooking_time': '35 minutes',
            'difficulty': 'medium',
            'fusion_style': f"{fusion_pair[0]} meets {fusion_pair[1]}",
            'source': 'Fusion Recipe Generator'
        }
    
    def _generate_healthy_recipe(self):
        """Generate a healthy recipe"""
        healthy_ingredients = [
            'fresh vegetables', 'lean protein', 'whole grains', 'healthy fats',
            'herbs and spices', 'low-fat dairy', 'legumes', 'nuts and seeds'
        ]
        
        return {
            'name': f"Healthy {random.choice(['Power Bowl', 'Nutrition Wrap', 'Wellness Salad'])}",
            'type': 'Healthy',
            'ingredients': ', '.join(random.sample(healthy_ingredients, 4)),
            'instructions': "1. Choose fresh, organic ingredients. 2. Use minimal oil and healthy cooking methods. 3. Balance proteins, carbs, and healthy fats.",
            'cooking_time': '25 minutes',
            'difficulty': 'easy',
            'calories': 'Low to moderate',
            'health_benefits': 'High in vitamins, minerals, and antioxidants',
            'source': 'Healthy Recipe Generator'
        }
    
    def _generate_quick_recipe(self):
        """Generate a quick recipe"""
        quick_methods = ['stir-fry', 'pan-sear', 'microwave', 'no-cook', 'one-pot']
        
        return {
            'name': f"Quick {random.choice(['Meal', 'Fix', 'Bite', 'Dish'])}",
            'type': 'Quick',
            'ingredients': 'Ready-to-use ingredients, pre-cooked items',
            'instructions': f"Use {random.choice(quick_methods)} method for fastest preparation.",
            'cooking_time': '10 minutes',
            'difficulty': 'very easy',
            'prep_time': '5 minutes',
            'source': 'Quick Recipe Generator'
        }
    
    def _generate_random_recipe(self):
        """Generate a random recipe"""
        types = ['traditional', 'modern', 'fusion', 'healthy', 'quick']
        return self.generate_by_type(random.choice(types))
    
    def _load_recipe_templates(self):
        """Load recipe templates"""
        return [
            {
                'name': 'Vegetable Curry',
                'type': 'traditional',
                'required_ingredients': ['vegetables', 'onion', 'tomato', 'spices'],
                'optional_ingredients': ['garlic', 'ginger', 'coconut'],
                'cooking_time': '30 minutes',
                'difficulty': 'medium',
                'instructions': '1. Heat oil in pan. 2. Add onions and cook until golden. 3. Add tomatoes and spices. 4. Add vegetables and cook until tender. 5. Serve hot with rice.'
            },
            {
                'name': 'Rice Bowl',
                'type': 'modern',
                'required_ingredients': ['rice', 'vegetables', 'protein'],
                'optional_ingredients': ['sauce', 'herbs', 'nuts'],
                'cooking_time': '20 minutes',
                'difficulty': 'easy',
                'instructions': '1. Cook rice according to package instructions. 2. Prepare vegetables and protein. 3. Combine in bowl. 4. Add sauce and garnish.'
            }
        ]
    
    def _load_traditional_dishes(self):
        """Load traditional dish database"""
        return [
            {
                'name': 'Dal Tadka',
                'ingredients': ['lentils', 'onion', 'tomato', 'garlic', 'ginger', 'turmeric', 'cumin'],
                'instructions': '1. Boil lentils with turmeric. 2. Prepare tadka with cumin, garlic, ginger. 3. Add onions and tomatoes. 4. Mix with cooked lentils.',
                'cooking_time': '30 minutes',
                'difficulty': 'easy',
                'cultural_significance': 'Traditional Indian comfort food'
            },
            {
                'name': 'Vegetable Biryani',
                'ingredients': ['basmati rice', 'mixed vegetables', 'yogurt', 'biryani spices', 'fried onions'],
                'instructions': '1. Soak rice. 2. Cook vegetables with spices. 3. Layer rice and vegetables. 4. Cook on dum.',
                'cooking_time': '60 minutes',
                'difficulty': 'hard',
                'cultural_significance': 'Royal dish from Mughal cuisine'
            }
        ]
    
    def _load_cooking_methods(self):
        """Load cooking methods database"""
        return [
            'boiling', 'steaming', 'frying', 'sautéing', 'roasting', 'grilling',
            'baking', 'pressure cooking', 'slow cooking', 'stir-frying'
        ]
