"""
Constants file for Sahachari application
Contains language mappings, menu items, and other configuration constants
"""

# Language Configuration
LANGUAGES = {
    'english': {
        'code': 'en',
        'name': 'English',
        'native_name': 'English',
        'rtl': False
    },
    'telugu': {
        'code': 'te',
        'name': 'Telugu',
        'native_name': 'తెలుగు',
        'rtl': False
    }
}

# Menu Items with translations
MENU_ITEMS = {
    'recipes': {
        'english': '📖 Translate & Listen to Recipes',
        'telugu': '📖 వంటకాలను అనువదించండి మరియు వినండి'
    },
    'ingredients': {
        'english': '📷 Recognize Ingredients from Image',
        'telugu': '📷 చిత్రం నుండి పదార్థాలను గుర్తించండి'
    },
    'generate': {
        'english': '🍳 Generate Dishes',
        'telugu': '🍳 వంటకాలను రూపొందించండి'
    },
    'newspapers': {
        'english': '📰 Explore Historic Newspapers',
        'telugu': '📰 చారిత్రక వార్తాపత్రికలను అన్వేషించండి'
    }
}

# Application Text Translations
APP_TEXT = {
    'app_title': {
        'english': 'Sahachari: Bilingual Food & Culture Companion',
        'telugu': 'సహచారి: ద్విభాషా ఆహార మరియు సంస్కృతి సహచరుడు'
    },
    'app_subtitle': {
        'english': 'Bridging Food, Language, and Culture',
        'telugu': 'ఆహారం, భాష మరియు సంస్కృతిని కలుపుతోంది'
    },
    'language_toggle': {
        'english': '🌐 Language / భాష',
        'telugu': '🌐 భాష / Language'
    },
    'select_language': {
        'english': 'Select Language',
        'telugu': 'భాష ఎంచుకోండి'
    },
    'choose_feature': {
        'english': 'Choose Feature:',
        'telugu': 'ఫీచర్ ఎంచుకోండి:'
    },
    'footer_text': {
        'english': '🍽️ **Sahachari** - Bridging Food & Culture',
        'telugu': '🍽️ **సహచారి** - ఆహారం మరియు సంస్కృతిని కలుపుతోంది'
    }
}

# Recipe Module Text
RECIPE_TEXT = {
    'select_recipe': {
        'english': 'Select a recipe:',
        'telugu': 'వంటకం ఎంచుకోండి:'
    },
    'original': {
        'english': 'Original',
        'telugu': 'మూలం'
    },
    'translation': {
        'english': 'Translation',
        'telugu': 'అనువాదం'
    },
    'listen_original': {
        'english': '🔊 Listen (Original)',
        'telugu': '🔊 వినండి (మూలం)'
    },
    'listen_translation': {
        'english': '🔊 Listen (Translation)',
        'telugu': '🔊 వినండి (అనువాదం)'
    },
    'name': {
        'english': 'Name',
        'telugu': 'పేరు'
    },
    'ingredients': {
        'english': 'Ingredients',
        'telugu': 'పదార్థాలు'
    },
    'instructions': {
        'english': 'Instructions',
        'telugu': 'సూచనలు'
    },
    'cooking_time': {
        'english': 'Cooking Time',
        'telugu': 'వంట సమయం'
    },
    'difficulty': {
        'english': 'Difficulty',
        'telugu': 'కష్టతనం'
    },
    'servings': {
        'english': 'Servings',
        'telugu': 'వర్గాలు'
    }
}

# Ingredient Recognition Text
INGREDIENT_TEXT = {
    'upload_image': {
        'english': 'Upload a food image:',
        'telugu': 'ఆహార చిత్రాన్ని అప్‌లోడ్ చేయండి:'
    },
    'analyzing_image': {
        'english': 'Analyzing image...',
        'telugu': 'చిత్రాన్ని విశ్లేషిస్తోంది...'
    },
    'ingredients_identified': {
        'english': 'Ingredients identified!',
        'telugu': 'పదార్థాలు గుర్తించబడ్డాయి!'
    },
    'identified_ingredients': {
        'english': 'Identified Ingredients:',
        'telugu': 'గుర్తించిన పదార్థాలు:'
    },
    'suggest_recipes': {
        'english': 'Suggest Recipes',
        'telugu': 'వంటకాలను సూచించండి'
    },
    'suggested_recipes': {
        'english': 'Suggested Recipes:',
        'telugu': 'సూచించిన వంటకాలు:'
    },
    'no_ingredients_found': {
        'english': 'No ingredients could be identified in the image.',
        'telugu': 'చిత్రంలో పదార్థాలు గుర్తించబడలేదు.'
    },
    'no_recipes_for_ingredients': {
        'english': 'No recipes found for these ingredients.',
        'telugu': 'ఈ పదార్థాలకు వంటకాలు కనుగొనబడలేదు.'
    }
}

# Recipe Generation Text
GENERATION_TEXT = {
    'input_method': {
        'english': 'Choose input method:',
        'telugu': 'ఇన్‌పుట్ పద్ధతిని ఎంచుకోండి:'
    },
    'ingredients_list': {
        'english': 'Ingredients List',
        'telugu': 'పదార్థాల జాబితా'
    },
    'recipe_type': {
        'english': 'Recipe Type',
        'telugu': 'వంటకం రకం'
    },
    'enter_ingredients': {
        'english': 'Enter available ingredients (comma-separated):',
        'telugu': 'అందుబాటులో ఉన్న పదార్థాలను నమోదు చేయండి (కామాతో వేరు చేయబడిన):'
    },
    'ingredients_placeholder': {
        'english': 'tomato, onion, rice, chicken...',
        'telugu': 'టమాటా, ఉల్లిపాయ, అన్నం, చికెన్...'
    },
    'generate_recipes': {
        'english': 'Generate Recipes',
        'telugu': 'వంటకాలను రూపొందించండి'
    },
    'generating_recipes': {
        'english': 'Generating recipes...',
        'telugu': 'వంటకాలను రూపొందిస్తోంది...'
    },
    'select_recipe_type': {
        'english': 'Select recipe type:',
        'telugu': 'వంటకం రకాన్ని ఎంచుకోండి:'
    },
    'generate_recipe': {
        'english': 'Generate Recipe',
        'telugu': 'వంటకం రూపొందించండి'
    },
    'generating_recipe': {
        'english': 'Generating recipe...',
        'telugu': 'వంటకం రూపొందిస్తోంది...'
    },
    'recipe_generated': {
        'english': 'Recipe generated!',
        'telugu': 'వంటకం రూపొందించబడింది!'
    },
    'no_recipe_generated': {
        'english': 'No recipes could be generated with the provided ingredients.',
        'telugu': 'అందించిన పదార్థాలతో వంటకాలు రూపొందించబడలేదు.'
    },
    'recipe_type_failed': {
        'english': 'Could not generate a recipe of this type.',
        'telugu': 'ఈ రకమైన వంటకం రూపొందించబడలేదు.'
    }
}

# Recipe Types with translations
RECIPE_TYPES = {
    'traditional': {
        'english': 'Traditional',
        'telugu': 'సాంప్రదాయ'
    },
    'modern': {
        'english': 'Modern',
        'telugu': 'ఆధునిక'
    },
    'fusion': {
        'english': 'Fusion',
        'telugu': 'మిశ్రమ'
    },
    'healthy': {
        'english': 'Healthy',
        'telugu': 'ఆరోగ్యకరమైన'
    },
    'quick': {
        'english': 'Quick',
        'telugu': 'త్వరిత'
    }
}

# Newspaper Module Text
NEWSPAPER_TEXT = {
    'search_content': {
        'english': 'Search historic content:',
        'telugu': 'చారిత్రక కంటెంట్‌ను వెతకండి:'
    },
    'search_placeholder': {
        'english': 'Enter keywords...',
        'telugu': 'కీలక పదాలను నమోదు చేయండి...'
    },
    'search': {
        'english': 'Search',
        'telugu': 'వెతకండి'
    },
    'searching': {
        'english': 'Searching...',
        'telugu': 'వెతుకుతోంది...'
    },
    'show_all': {
        'english': 'Show All',
        'telugu': 'అన్నీ చూపించు'
    },
    'articles_found': {
        'english': 'Found {count} articles',
        'telugu': '{count} వ్యాసాలు కనుగొనబడ్డాయి'
    },
    'no_articles': {
        'english': 'No articles found. Try a different search term or load all articles.',
        'telugu': 'వ్యాసాలు కనుగొనబడలేదు. వేరే వెతుకు పదం ప్రయత్నించండి లేదా అన్ని వ్యాసాలను లోడ్ చేయండి.'
    },
    'source': {
        'english': 'Source',
        'telugu': 'మూలం'
    },
    'date': {
        'english': 'Date',
        'telugu': 'తేదీ'
    },
    'content': {
        'english': 'Content',
        'telugu': 'కంటెంట్'
    },
    'translate': {
        'english': 'Translate',
        'telugu': 'అనువదించండి'
    },
    'translation_result': {
        'english': 'Translation',
        'telugu': 'అనువాదం'
    }
}

# Accessibility Text
ACCESSIBILITY_TEXT = {
    'accessibility': {
        'english': '♿ Accessibility',
        'telugu': '♿ అందుబాటు'
    },
    'accessibility_notice': {
        'english': 'This app supports screen readers, keyboard navigation, and high contrast mode.',
        'telugu': 'ఈ యాప్ స్క్రీన్ రీడర్లు, కీబోర్డ్ నావిగేషన్ మరియు హై కాంట్రాస్ట్ మోడ్‌ను సపోర్ట్ చేస్తుంది.'
    },
    'accessibility_options': {
        'english': 'Accessibility Options',
        'telugu': 'అందుబాటు ఎంపికలు'
    },
    'high_contrast': {
        'english': 'High Contrast Mode',
        'telugu': 'హై కాంట్రాస్ట్ మోడ్'
    },
    'large_text': {
        'english': 'Large Text',
        'telugu': 'పెద్ద టెక్స్ట్'
    },
    'screen_reader': {
        'english': 'Screen Reader Optimized',
        'telugu': 'స్క్రీన్ రీడర్ ఆప్టిమైజ్డ్'
    },
    'keyboard_shortcuts': {
        'english': '⌨️ Keyboard Shortcuts',
        'telugu': '⌨️ కీబోర్డ్ షార్ట్‌కట్‌లు'
    }
}

# Error Messages
ERROR_MESSAGES = {
    'translation_failed': {
        'english': 'Translation failed: {error}',
        'telugu': 'అనువాదం విఫలమైంది: {error}'
    },
    'audio_generation_failed': {
        'english': 'Audio generation failed: {error}',
        'telugu': 'ఆడియో జనరేషన్ విఫలమైంది: {error}'
    },
    'image_analysis_failed': {
        'english': 'Image analysis failed: {error}',
        'telugu': 'చిత్ర విశ్లేషణ విఫలమైంది: {error}'
    },
    'recipe_generation_failed': {
        'english': 'Recipe generation failed: {error}',
        'telugu': 'వంటకం రూపొందింపు విఫలమైంది: {error}'
    },
    'search_failed': {
        'english': 'Search failed: {error}',
        'telugu': 'వెతుకు విఫలమైంది: {error}'
    },
    'no_data_available': {
        'english': 'No data available. Please check your data source.',
        'telugu': 'డేటా అందుబాటులో లేదు. దయచేసి మీ డేటా మూలాన్ని తనిఖీ చేయండి.'
    },
    'file_upload_failed': {
        'english': 'File upload failed. Please try again.',
        'telugu': 'ఫైల్ అప్‌లోడ్ విఫలమైంది. దయచేసి మళ్లీ ప్రయత్నించండి.'
    }
}

# Success Messages
SUCCESS_MESSAGES = {
    'recipes_generated': {
        'english': 'Generated {count} recipes!',
        'telugu': '{count} వంటకాలు రూపొందించబడ్డాయి!'
    },
    'ingredients_identified': {
        'english': 'Ingredients identified successfully!',
        'telugu': 'పదార్థాలు విజయవంతంగా గుర్తించబడ్డాయి!'
    },
    'translation_completed': {
        'english': 'Translation completed successfully!',
        'telugu': 'అనువాదం విజయవంతంగా పూర్తైంది!'
    },
    'audio_generated': {
        'english': 'Audio generated successfully!',
        'telugu': 'ఆడియో విజయవంతంగా రూపొందించబడింది!'
    }
}

# File Upload Configuration
FILE_UPLOAD = {
    'max_size_mb': 10,
    'supported_image_formats': ['jpg', 'jpeg', 'png'],
    'supported_audio_formats': ['mp3', 'wav'],
    'supported_text_formats': ['txt', 'csv', 'json']
}

# API Configuration
API_CONFIG = {
    'google_translate': {
        'supported_languages': ['en', 'te', 'hi', 'ta', 'kn', 'ml'],
        'max_text_length': 5000
    },
    'google_vision': {
        'supported_formats': ['jpeg', 'png', 'gif', 'bmp', 'webp'],
        'max_file_size_mb': 20
    },
    'google_tts': {
        'supported_languages': ['en', 'te', 'hi', 'ta'],
        'audio_format': 'mp3'
    }
}

# UI Configuration
UI_CONFIG = {
    'sidebar_width': 300,
    'main_content_width': 800,
    'image_display_width': 400,
    'audio_player_width': 300
}

# Data Validation Rules
VALIDATION_RULES = {
    'recipe_name_min_length': 3,
    'recipe_name_max_length': 100,
    'ingredients_min_length': 10,
    'instructions_min_length': 20,
    'search_query_min_length': 2,
    'search_query_max_length': 200
}

# Default Values
DEFAULTS = {
    'language': 'english',
    'recipe_servings': '4',
    'cooking_time': '30 minutes',
    'difficulty': 'medium',
    'recipe_type': 'traditional'
}

# Navigation and Menu Structure
NAVIGATION = {
    'main_sections': ['recipes', 'ingredients', 'generate', 'newspapers'],
    'admin_sections': ['config', 'statistics', 'data_management'],
    'help_sections': ['keyboard_shortcuts', 'accessibility', 'about']
}

# Food Categories for better organization
FOOD_CATEGORIES = {
    'vegetables': {
        'english': 'Vegetables',
        'telugu': 'కూరగాయలు'
    },
    'fruits': {
        'english': 'Fruits',
        'telugu': 'పండ్లు'
    },
    'grains': {
        'english': 'Grains',
        'telugu': 'ధాన్యాలు'
    },
    'legumes': {
        'english': 'Legumes',
        'telugu': 'పప్పులు'
    },
    'spices': {
        'english': 'Spices',
        'telugu': 'మసాలాలు'
    },
    'dairy': {
        'english': 'Dairy',
        'telugu': 'పాల ఉత్పత్తులు'
    },
    'meat': {
        'english': 'Meat',
        'telugu': 'మాంసం'
    },
    'seafood': {
        'english': 'Seafood',
        'telugu': 'సముద్ర ఆహారం'
    }
}

# Cooking Methods
COOKING_METHODS = {
    'boiling': {
        'english': 'Boiling',
        'telugu': 'ఉడకబెట్టడం'
    },
    'frying': {
        'english': 'Frying',
        'telugu': 'వేయించడం'
    },
    'steaming': {
        'english': 'Steaming',
        'telugu': 'ఆవిరిపై వండటం'
    },
    'roasting': {
        'english': 'Roasting',
        'telugu': 'కాల్చడం'
    },
    'grilling': {
        'english': 'Grilling',
        'telugu': 'గ్రిల్లింగ్'
    },
    'baking': {
        'english': 'Baking',
        'telugu': 'బేకింగ్'
    }
}

# Nutritional Information Categories
NUTRITION_CATEGORIES = {
    'calories': {
        'english': 'Calories',
        'telugu': 'కేలరీలు'
    },
    'protein': {
        'english': 'Protein',
        'telugu': 'ప్రోటీన్'
    },
    'carbohydrates': {
        'english': 'Carbohydrates',
        'telugu': 'కార్బోహైడ్రేట్లు'
    },
    'fat': {
        'english': 'Fat',
        'telugu': 'కొవ్వు'
    },
    'fiber': {
        'english': 'Fiber',
        'telugu': 'ఫైబర్'
    },
    'vitamins': {
        'english': 'Vitamins',
        'telugu': 'విటమిన్లు'
    },
    'minerals': {
        'english': 'Minerals',
        'telugu': 'ఖనిజాలు'
    }
}

