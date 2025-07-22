import os
import io
import json
import streamlit as st
import requests
from PIL import Image
import base64

class ImageRecognitionService:
    """Image recognition service for identifying food ingredients"""
    
    def __init__(self):
        self.google_vision_api_key = os.getenv("GOOGLE_VISION_API_KEY", None)
        self.azure_computer_vision_key = os.getenv("AZURE_COMPUTER_VISION_KEY", None)
        self.azure_endpoint = os.getenv("AZURE_COMPUTER_VISION_ENDPOINT", None)
        
        # Food-related keywords for filtering results
        self.food_keywords = [
            'food', 'ingredient', 'vegetable', 'fruit', 'meat', 'spice', 'grain',
            'dairy', 'herb', 'oil', 'rice', 'wheat', 'tomato', 'onion', 'potato',
            'carrot', 'pepper', 'garlic', 'ginger', 'chicken', 'fish', 'egg',
            'milk', 'cheese', 'yogurt', 'bread', 'flour', 'sugar', 'salt'
        ]
    
    def identify_ingredients(self, image_file):
        """
        Identify ingredients from uploaded image
        
        Args:
            image_file: Streamlit uploaded file object
            
        Returns:
            list: List of identified ingredients with confidence scores
        """
        try:
            # Process image
            image = Image.open(image_file)
            
            # Try different APIs in order of preference
            if self.google_vision_api_key:
                return self._identify_with_google_vision(image)
            elif self.azure_computer_vision_key:
                return self._identify_with_azure(image)
            else:
                # Fallback to basic image analysis
                return self._identify_with_fallback(image)
                
        except Exception as e:
            st.error(f"Image recognition failed: {str(e)}")
            return []
    
    def _identify_with_google_vision(self, image):
        """Identify ingredients using Google Vision API"""
        # Convert image to base64
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='JPEG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        url = f"https://vision.googleapis.com/v1/images:annotate?key={self.google_vision_api_key}"
        
        data = {
            'requests': [{
                'image': {
                    'content': img_base64
                },
                'features': [
                    {'type': 'LABEL_DETECTION', 'maxResults': 20},
                    {'type': 'OBJECT_LOCALIZATION', 'maxResults': 20}
                ]
            }]
        }
        
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            ingredients = []
            
            # Process label annotations
            if 'responses' in result and result['responses']:
                annotations = result['responses'][0]
                
                # Process labels
                if 'labelAnnotations' in annotations:
                    for label in annotations['labelAnnotations']:
                        description = label['description'].lower()
                        score = label['score']
                        
                        if self._is_food_related(description):
                            ingredients.append({
                                'name': label['description'],
                                'confidence': score,
                                'type': 'label'
                            })
                
                # Process objects
                if 'localizedObjectAnnotations' in annotations:
                    for obj in annotations['localizedObjectAnnotations']:
                        name = obj['name'].lower()
                        score = obj['score']
                        
                        if self._is_food_related(name):
                            ingredients.append({
                                'name': obj['name'],
                                'confidence': score,
                                'type': 'object'
                            })
            
            # Remove duplicates and sort by confidence
            ingredients = self._deduplicate_ingredients(ingredients)
            return sorted(ingredients, key=lambda x: x['confidence'], reverse=True)
        
        else:
            raise Exception(f"Google Vision API failed with status {response.status_code}")
    
    def _identify_with_azure(self, image):
        """Identify ingredients using Azure Computer Vision"""
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='JPEG')
        img_data = img_buffer.getvalue()
        
        url = f"{self.azure_endpoint}/vision/v3.2/analyze"
        
        headers = {
            'Ocp-Apim-Subscription-Key': self.azure_computer_vision_key,
            'Content-Type': 'application/octet-stream'
        }
        
        params = {
            'visualFeatures': 'Categories,Description,Objects,Tags',
            'details': 'Food'
        }
        
        response = requests.post(url, headers=headers, params=params, data=img_data)
        
        if response.status_code == 200:
            result = response.json()
            ingredients = []
            
            # Process tags
            if 'tags' in result:
                for tag in result['tags']:
                    name = tag['name'].lower()
                    confidence = tag['confidence']
                    
                    if self._is_food_related(name):
                        ingredients.append({
                            'name': tag['name'],
                            'confidence': confidence,
                            'type': 'tag'
                        })
            
            # Process objects
            if 'objects' in result:
                for obj in result['objects']:
                    name = obj['object'].lower()
                    confidence = obj['confidence']
                    
                    if self._is_food_related(name):
                        ingredients.append({
                            'name': obj['object'],
                            'confidence': confidence,
                            'type': 'object'
                        })
            
            ingredients = self._deduplicate_ingredients(ingredients)
            return sorted(ingredients, key=lambda x: x['confidence'], reverse=True)
        
        else:
            raise Exception(f"Azure Computer Vision failed with status {response.status_code}")
    
    def _identify_with_fallback(self, image):
        """Fallback method using basic image properties"""
        st.warning("No API keys available. Using basic image analysis.")
        
        # Analyze image properties
        width, height = image.size
        mode = image.mode
        
        # Get dominant colors
        colors = self._get_dominant_colors(image)
        
        # Basic ingredient suggestions based on colors
        ingredients = self._suggest_from_colors(colors)
        
        return ingredients
    
    def _is_food_related(self, text):
        """Check if text is food-related"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.food_keywords)
    
    def _deduplicate_ingredients(self, ingredients):
        """Remove duplicate ingredients"""
        seen = set()
        unique_ingredients = []
        
        for ingredient in ingredients:
            name_lower = ingredient['name'].lower()
            if name_lower not in seen:
                seen.add(name_lower)
                unique_ingredients.append(ingredient)
        
        return unique_ingredients
    
    def _get_dominant_colors(self, image, num_colors=5):
        """Get dominant colors from image"""
        # Resize image for faster processing
        image = image.resize((150, 150))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Get colors
        colors = image.getcolors(maxcolors=256*256*256)
        
        if colors:
            # Sort by frequency and get top colors
            colors.sort(key=lambda x: x[0], reverse=True)
            return [color[1] for color in colors[:num_colors]]
        
        return []
    
    def _suggest_from_colors(self, colors):
        """Suggest ingredients based on dominant colors"""
        color_to_ingredients = {
            # Red colors
            (255, 0, 0): ['tomato', 'red pepper', 'strawberry'],
            (200, 0, 0): ['tomato', 'red chili'],
            # Green colors
            (0, 255, 0): ['lettuce', 'spinach', 'green pepper'],
            (0, 128, 0): ['broccoli', 'green beans', 'cucumber'],
            # Orange colors
            (255, 165, 0): ['carrot', 'orange', 'pumpkin'],
            (255, 140, 0): ['carrot', 'sweet potato'],
            # Yellow colors
            (255, 255, 0): ['corn', 'banana', 'lemon'],
            (255, 215, 0): ['corn', 'squash'],
            # Brown colors
            (139, 69, 19): ['potato', 'onion', 'mushroom'],
            (160, 82, 45): ['bread', 'wheat', 'rice'],
            # White colors
            (255, 255, 255): ['rice', 'flour', 'milk', 'egg'],
        }
        
        ingredients = []
        
        for color in colors:
            # Find closest color match
            closest_color = min(color_to_ingredients.keys(), 
                              key=lambda c: sum((a-b)**2 for a, b in zip(color, c)))
            
            # Add ingredients for this color
            for ingredient in color_to_ingredients[closest_color]:
                ingredients.append({
                    'name': ingredient,
                    'confidence': 0.5,  # Lower confidence for color-based detection
                    'type': 'color_analysis'
                })
        
        return self._deduplicate_ingredients(ingredients)[:5]  # Return top 5
    
    def preprocess_image(self, image, max_size=(800, 800)):
        """
        Preprocess image for better recognition
        
        Args:
            image: PIL Image object
            max_size: Maximum image dimensions
            
        Returns:
            PIL Image: Preprocessed image
        """
        # Resize if too large
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        return image
    
    def get_nutrition_info(self, ingredient_name):
        """
        Get basic nutrition information for an ingredient
        
        Args:
            ingredient_name (str): Name of the ingredient
            
        Returns:
            dict: Basic nutrition information
        """
        # Basic nutrition data for common ingredients
        nutrition_db = {
            'tomato': {'calories': 18, 'vitamin_c': 'high', 'lycopene': 'high'},
            'onion': {'calories': 40, 'vitamin_c': 'medium', 'quercetin': 'high'},
            'carrot': {'calories': 41, 'vitamin_a': 'very_high', 'beta_carotene': 'high'},
            'potato': {'calories': 77, 'potassium': 'high', 'vitamin_c': 'medium'},
            'rice': {'calories': 130, 'carbohydrates': 'high', 'protein': 'medium'},
            'chicken': {'calories': 165, 'protein': 'very_high', 'vitamin_b6': 'high'},
        }
        
        return nutrition_db.get(ingredient_name.lower(), {
            'calories': 'unknown',
            'notes': 'Nutrition data not available'
        })
