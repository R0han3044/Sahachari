import os
import json
import csv
import pandas as pd
import streamlit as st
from typing import List, Dict, Any

class DataHandler:
    """Data handling service for managing recipes and newspaper content"""
    
    def __init__(self, data_source='temporary'):
        self.data_source = data_source
        self.recipes_data = []
        self.newspapers_data = []
        
        # Load data based on source
        self._load_data()
    
    def _load_data(self):
        """Load data from the specified source"""
        try:
            if self.data_source == 'temporary':
                self._load_temporary_data()
            else:
                self._load_production_data()
        except Exception as e:
            st.error(f"Failed to load data: {str(e)}")
            # Initialize with empty data
            self.recipes_data = []
            self.newspapers_data = []
    
    def _load_temporary_data(self):
        """Load temporary sample data"""
        # Try to load from sample_data.json
        try:
            with open('data/sample_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.recipes_data = data.get('recipes', [])
                self.newspapers_data = data.get('newspapers', [])
        except FileNotFoundError:
            # Create sample data if file doesn't exist
            self._create_sample_data()
    
    def _load_production_data(self):
        """Load production data from database or files"""
        # This would connect to actual database in production
        # For now, fall back to temporary data
        st.warning("Production data source not configured. Using temporary data.")
        self._load_temporary_data()
    
    def _create_sample_data(self):
        """Create sample data for demonstration"""
        st.warning("No data file found. Using minimal sample data.")
        
        self.recipes_data = [
            {
                'id': 1,
                'name': 'Simple Dal',
                'ingredients': 'Lentils, Onion, Tomato, Turmeric, Salt, Oil',
                'instructions': 'Boil lentils with turmeric. In a pan, heat oil, add onions, then tomatoes. Mix with cooked lentils and add salt.',
                'cooking_time': '30 minutes',
                'difficulty': 'Easy',
                'language': 'english',
                'cuisine': 'Indian'
            },
            {
                'id': 2,
                'name': 'పప్పు పులుసు',
                'ingredients': 'పప్పు, ఉల్లిపాయ, టమాటా, పసుపు, ఉప్పు, నూనె',
                'instructions': 'పప్పును పసుపుతో వండాలి. వేరే పాత్రలో నూనె వేసి, ఉల్లిపాయలు వేసి, తర్వాత టమాటాలు వేయాలి. వండిన పప్పుతో కలపాలి.',
                'cooking_time': '30 నిమిషాలు',
                'difficulty': 'సులభం',
                'language': 'telugu',
                'cuisine': 'తెలుగు వంటకాలు'
            }
        ]
        
        self.newspapers_data = [
            {
                'id': 1,
                'title': 'Traditional Cooking Methods',
                'content': 'In the past, traditional cooking methods were used to prepare nutritious meals. Clay pots and wood fire gave unique flavors to food.',
                'date': '1950-01-15',
                'source': 'Heritage Daily',
                'language': 'english',
                'category': 'food_culture'
            },
            {
                'id': 2,
                'title': 'సాంప్రదాయ వంట పద్ధతులు',
                'content': 'పూర్వకాలంలో సాంప్రదాయ వంట పద్ధతులను ఉపయోగించి పోషకమైన భోజనం తయారు చేసేవారు. మట్టి పాత్రలు మరియు కట్టెల మంట ఆహారానికి ప్రత్యేక రుచిని ఇచ్చేవి.',
                'date': '1950-01-15',
                'source': 'వారసత్వ దినపత్రిక',
                'language': 'telugu',
                'category': 'ఆహార_సంస్కృతి'
            }
        ]
    
    def get_recipes(self) -> List[Dict[str, Any]]:
        """Get all recipes"""
        return self.recipes_data
    
    def get_recipe_by_id(self, recipe_id: int) -> Dict[str, Any]:
        """Get a specific recipe by ID"""
        for recipe in self.recipes_data:
            if recipe.get('id') == recipe_id:
                return recipe
        return {}
    
    def search_recipes(self, query: str, language: str = None) -> List[Dict[str, Any]]:
        """
        Search recipes by query
        
        Args:
            query (str): Search query
            language (str): Filter by language
            
        Returns:
            List[Dict]: Matching recipes
        """
        if not query:
            return self.recipes_data
        
        query_lower = query.lower()
        results = []
        
        for recipe in self.recipes_data:
            # Check if query matches any field
            matches = (
                query_lower in recipe.get('name', '').lower() or
                query_lower in recipe.get('ingredients', '').lower() or
                query_lower in recipe.get('instructions', '').lower() or
                query_lower in recipe.get('cuisine', '').lower()
            )
            
            # Filter by language if specified
            if language and recipe.get('language') != language:
                continue
            
            if matches:
                results.append(recipe)
        
        return results
    
    def get_newspapers(self) -> List[Dict[str, Any]]:
        """Get all newspaper articles"""
        return self.newspapers_data
    
    def search_newspapers(self, query: str, language: str = None) -> List[Dict[str, Any]]:
        """
        Search newspaper articles by query
        
        Args:
            query (str): Search query
            language (str): Filter by language
            
        Returns:
            List[Dict]: Matching articles
        """
        if not query:
            return self.newspapers_data
        
        query_lower = query.lower()
        results = []
        
        for article in self.newspapers_data:
            # Check if query matches any field
            matches = (
                query_lower in article.get('title', '').lower() or
                query_lower in article.get('content', '').lower() or
                query_lower in article.get('category', '').lower()
            )
            
            # Filter by language if specified
            if language and article.get('language') != language:
                continue
            
            if matches:
                results.append(article)
        
        return results
    
    def add_recipe(self, recipe_data: Dict[str, Any]) -> bool:
        """Add a new recipe"""
        try:
            # Generate new ID
            max_id = max([r.get('id', 0) for r in self.recipes_data] + [0])
            recipe_data['id'] = max_id + 1
            
            self.recipes_data.append(recipe_data)
            self._save_data()
            return True
        except Exception as e:
            st.error(f"Failed to add recipe: {str(e)}")
            return False
    
    def update_recipe(self, recipe_id: int, updated_data: Dict[str, Any]) -> bool:
        """Update an existing recipe"""
        try:
            for i, recipe in enumerate(self.recipes_data):
                if recipe.get('id') == recipe_id:
                    self.recipes_data[i].update(updated_data)
                    self._save_data()
                    return True
            return False
        except Exception as e:
            st.error(f"Failed to update recipe: {str(e)}")
            return False
    
    def delete_recipe(self, recipe_id: int) -> bool:
        """Delete a recipe"""
        try:
            self.recipes_data = [r for r in self.recipes_data if r.get('id') != recipe_id]
            self._save_data()
            return True
        except Exception as e:
            st.error(f"Failed to delete recipe: {str(e)}")
            return False
    
    def import_recipes_from_csv(self, csv_file) -> bool:
        """Import recipes from CSV file"""
        try:
            df = pd.read_csv(csv_file)
            
            for _, row in df.iterrows():
                recipe = {
                    'name': row.get('name', ''),
                    'ingredients': row.get('ingredients', ''),
                    'instructions': row.get('instructions', ''),
                    'cooking_time': row.get('cooking_time', ''),
                    'difficulty': row.get('difficulty', ''),
                    'language': row.get('language', 'english'),
                    'cuisine': row.get('cuisine', '')
                }
                self.add_recipe(recipe)
            
            return True
        except Exception as e:
            st.error(f"Failed to import CSV: {str(e)}")
            return False
    
    def export_recipes_to_csv(self, filename: str = 'recipes_export.csv') -> bool:
        """Export recipes to CSV file"""
        try:
            df = pd.DataFrame(self.recipes_data)
            df.to_csv(filename, index=False, encoding='utf-8')
            return True
        except Exception as e:
            st.error(f"Failed to export CSV: {str(e)}")
            return False
    
    def get_recipe_statistics(self) -> Dict[str, Any]:
        """Get statistics about the recipe collection"""
        total_recipes = len(self.recipes_data)
        
        # Count by language
        language_counts = {}
        cuisine_counts = {}
        difficulty_counts = {}
        
        for recipe in self.recipes_data:
            lang = recipe.get('language', 'unknown')
            cuisine = recipe.get('cuisine', 'unknown')
            difficulty = recipe.get('difficulty', 'unknown')
            
            language_counts[lang] = language_counts.get(lang, 0) + 1
            cuisine_counts[cuisine] = cuisine_counts.get(cuisine, 0) + 1
            difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
        
        return {
            'total_recipes': total_recipes,
            'languages': language_counts,
            'cuisines': cuisine_counts,
            'difficulties': difficulty_counts
        }
    
    def _save_data(self):
        """Save current data to file"""
        try:
            if self.data_source == 'temporary':
                data = {
                    'recipes': self.recipes_data,
                    'newspapers': self.newspapers_data
                }
                
                # Ensure directory exists
                os.makedirs('data', exist_ok=True)
                
                with open('data/sample_data.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            st.error(f"Failed to save data: {str(e)}")
    
    def switch_data_source(self, new_source: str):
        """Switch between data sources"""
        if new_source != self.data_source:
            self.data_source = new_source
            self._load_data()
            st.success(f"Switched to {new_source} data source")
    
    def validate_recipe_data(self, recipe_data: Dict[str, Any]) -> List[str]:
        """Validate recipe data and return list of errors"""
        errors = []
        
        required_fields = ['name', 'ingredients', 'instructions']
        for field in required_fields:
            if not recipe_data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Validate cooking time format
        cooking_time = recipe_data.get('cooking_time', '')
        if cooking_time and not any(unit in cooking_time.lower() 
                                   for unit in ['minute', 'hour', 'min', 'hr', 'నిమిషం', 'గంట']):
            errors.append("Cooking time should include time units")
        
        return errors
