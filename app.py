import streamlit as st
import json
import os
from modules.translation import TranslationService
from modules.text_to_speech import TTSService
from modules.image_recognition import ImageRecognitionService
from modules.recipe_generator import RecipeGenerator
from modules.data_handler import DataHandler
from modules.accessibility import AccessibilityHelper
from utils.config import Config
from utils.constants import LANGUAGES, MENU_ITEMS

# Page configuration
st.set_page_config(
    page_title="Sahachari - Food & Culture Bridge",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize services
@st.cache_resource
def init_services():
    """Initialize all services with caching for better performance"""
    config = Config()
    data_handler = DataHandler(config.data_source)
    translation_service = TranslationService()
    tts_service = TTSService()
    image_service = ImageRecognitionService()
    recipe_generator = RecipeGenerator()
    accessibility_helper = AccessibilityHelper()
    
    return {
        'data_handler': data_handler,
        'translation': translation_service,
        'tts': tts_service,
        'image': image_service,
        'recipe_generator': recipe_generator,
        'accessibility': accessibility_helper
    }

def initialize_session_state():
    """Initialize session state variables"""
    if 'language' not in st.session_state:
        st.session_state.language = 'english'
    if 'current_recipe' not in st.session_state:
        st.session_state.current_recipe = None
    if 'search_results' not in st.session_state:
        st.session_state.search_results = []

def render_language_toggle():
    """Render language toggle in sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🌐 Language / భాష")
    
    language_options = {
        'english': 'English',
        'telugu': 'తెలుగు'
    }
    
    selected_language = st.sidebar.selectbox(
        "Select Language",
        options=list(language_options.keys()),
        format_func=lambda x: language_options[x],
        index=0 if st.session_state.language == 'english' else 1,
        key="language_selector"
    )
    
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.rerun()

def get_localized_text(text_key, services):
    """Get localized text based on current language"""
    translations = {
        'app_title': {
            'english': 'Sahachari: Bilingual Food & Culture Companion',
            'telugu': 'సహచారి: ద్విభాషా ఆహార మరియు సంస్కృతి సహచరుడు'
        },
        'menu_recipes': {
            'english': '📖 Translate & Listen to Recipes',
            'telugu': '📖 వంటకాలను అనువదించండి మరియు వినండి'
        },
        'menu_ingredients': {
            'english': '📷 Recognize Ingredients from Image',
            'telugu': '📷 చిత్రం నుండి పదార్థాలను గుర్తించండి'
        },
        'menu_generate': {
            'english': '🍳 Generate Dishes',
            'telugu': '🍳 వంటకాలను రూపొందించండి'
        },
        'menu_newspapers': {
            'english': '📰 Explore Historic Newspapers',
            'telugu': '📰 చారిత్రక వార్తాపత్రికలను అన్వేషించండి'
        }
    }
    
    return translations.get(text_key, {}).get(st.session_state.language, text_key)

def render_recipe_module(services):
    """Render recipe translation and TTS module"""
    st.header(get_localized_text('menu_recipes', services))
    
    # Get recipes from data handler
    recipes = services['data_handler'].get_recipes()
    
    if not recipes:
        st.error("No recipes available. Please check your data source.")
        return
    
    # Recipe selection
    recipe_names = [recipe.get('name', f"Recipe {i+1}") for i, recipe in enumerate(recipes)]
    selected_recipe_idx = st.selectbox(
        "Select a recipe:" if st.session_state.language == 'english' else "వంటకం ఎంచుకోండి:",
        range(len(recipe_names)),
        format_func=lambda x: recipe_names[x]
    )
    
    if selected_recipe_idx is not None:
        recipe = recipes[selected_recipe_idx]
        st.session_state.current_recipe = recipe
        
        # Display recipe
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original" if st.session_state.language == 'english' else "మూలం")
            st.write(f"**Name:** {recipe.get('name', 'N/A')}")
            st.write(f"**Ingredients:** {recipe.get('ingredients', 'N/A')}")
            st.write(f"**Instructions:** {recipe.get('instructions', 'N/A')}")
            
            # TTS for original
            if st.button("🔊 Listen (Original)" if st.session_state.language == 'english' else "🔊 వినండి (మూలం)"):
                try:
                    audio_file = services['tts'].generate_audio(
                        recipe.get('instructions', ''), 
                        'en' if recipe.get('language', 'english') == 'english' else 'te'
                    )
                    if audio_file:
                        st.audio(audio_file)
                except Exception as e:
                    st.error(f"Audio generation failed: {str(e)}")
        
        with col2:
            st.subheader("Translation" if st.session_state.language == 'english' else "అనువాదం")
            
            target_lang = 'te' if st.session_state.language == 'english' else 'en'
            
            try:
                translated_name = services['translation'].translate_text(recipe.get('name', ''), target_lang)
                translated_ingredients = services['translation'].translate_text(recipe.get('ingredients', ''), target_lang)
                translated_instructions = services['translation'].translate_text(recipe.get('instructions', ''), target_lang)
                
                st.write(f"**Name:** {translated_name}")
                st.write(f"**Ingredients:** {translated_ingredients}")
                st.write(f"**Instructions:** {translated_instructions}")
                
                # TTS for translation
                if st.button("🔊 Listen (Translation)" if st.session_state.language == 'english' else "🔊 వినండి (అనువాదం)"):
                    try:
                        audio_file = services['tts'].generate_audio(translated_instructions, target_lang)
                        if audio_file:
                            st.audio(audio_file)
                    except Exception as e:
                        st.error(f"Audio generation failed: {str(e)}")
                        
            except Exception as e:
                st.error(f"Translation failed: {str(e)}")

def render_ingredient_recognition(services):
    """Render ingredient recognition module"""
    st.header(get_localized_text('menu_ingredients', services))
    
    uploaded_file = st.file_uploader(
        "Upload a food image:" if st.session_state.language == 'english' else "ఆహార చిత్రాన్ని అప్‌లోడ్ చేయండి:",
        type=['jpg', 'png', 'jpeg'],
        help="Upload an image to identify ingredients"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        # Process image
        with st.spinner("Analyzing image..." if st.session_state.language == 'english' else "చిత్రాన్ని విశ్లేషిస్తోంది..."):
            try:
                ingredients = services['image'].identify_ingredients(uploaded_file)
                
                if ingredients:
                    st.success("Ingredients identified!" if st.session_state.language == 'english' else "పదార్థాలు గుర్తించబడ్డాయి!")
                    
                    # Display identified ingredients
                    st.subheader("Identified Ingredients:" if st.session_state.language == 'english' else "గుర్తించిన పదార్థాలు:")
                    
                    for ingredient in ingredients:
                        confidence = ingredient.get('confidence', 0)
                        name = ingredient.get('name', 'Unknown')
                        
                        # Translate ingredient name if needed
                        if st.session_state.language == 'telugu':
                            try:
                                name = services['translation'].translate_text(name, 'te')
                            except:
                                pass  # Keep original if translation fails
                        
                        st.write(f"• {name} (Confidence: {confidence:.2f})")
                    
                    # Suggest recipes based on ingredients
                    if st.button("Suggest Recipes" if st.session_state.language == 'english' else "వంటకాలను సూచించండి"):
                        ingredient_names = [ing.get('name', '') for ing in ingredients]
                        suggested_recipes = services['recipe_generator'].suggest_recipes(ingredient_names)
                        
                        if suggested_recipes:
                            st.subheader("Suggested Recipes:" if st.session_state.language == 'english' else "సూచించిన వంటకాలు:")
                            for recipe in suggested_recipes:
                                st.write(f"• {recipe}")
                        else:
                            st.info("No recipes found for these ingredients." if st.session_state.language == 'english' else "ఈ పదార్థాలకు వంటకాలు కనుగొనబడలేదు.")
                else:
                    st.warning("No ingredients could be identified in the image." if st.session_state.language == 'english' else "చిత్రంలో పదార్థాలు గుర్తించబడలేదు.")
                    
            except Exception as e:
                st.error(f"Image analysis failed: {str(e)}")

def render_recipe_generator(services):
    """Render recipe generation module"""
    st.header(get_localized_text('menu_generate', services))
    
    # Input method selection
    input_method = st.radio(
        "Choose input method:" if st.session_state.language == 'english' else "ఇన్‌పుట్ పద్ధతిని ఎంచుకోండి:",
        ["Ingredients List", "Recipe Type"],
        format_func=lambda x: x if st.session_state.language == 'english' else 
                    ("పదార్థాల జాబితా" if x == "Ingredients List" else "వంటకం రకం")
    )
    
    if input_method == "Ingredients List":
        ingredients_input = st.text_area(
            "Enter available ingredients (comma-separated):" if st.session_state.language == 'english' else 
            "అందుబాటులో ఉన్న పదార్థాలను నమోదు చేయండి (కామాతో వేరు చేయబడిన):",
            placeholder="tomato, onion, rice, chicken..." if st.session_state.language == 'english' else 
                       "టమాటా, ఉల్లిపాయ, అన్నం, చికెన్..."
        )
        
        if ingredients_input and st.button("Generate Recipes" if st.session_state.language == 'english' else "వంటకాలను రూపొందించండి"):
            ingredients = [ing.strip() for ing in ingredients_input.split(',')]
            
            with st.spinner("Generating recipes..." if st.session_state.language == 'english' else "వంటకాలను రూపొందిస్తోంది..."):
                try:
                    recipes = services['recipe_generator'].generate_from_ingredients(ingredients)
                    
                    if recipes:
                        st.success(f"Generated {len(recipes)} recipes!" if st.session_state.language == 'english' else f"{len(recipes)} వంటకాలు రూపొందించబడ్డాయి!")
                        
                        for i, recipe in enumerate(recipes, 1):
                            with st.expander(f"Recipe {i}: {recipe.get('name', 'Unnamed')}" if st.session_state.language == 'english' else f"వంటకం {i}: {recipe.get('name', 'పేరులేని')}"):
                                st.write(f"**Ingredients:** {recipe.get('ingredients', 'N/A')}")
                                st.write(f"**Instructions:** {recipe.get('instructions', 'N/A')}")
                                st.write(f"**Cooking Time:** {recipe.get('cooking_time', 'N/A')}")
                    else:
                        st.info("No recipes could be generated with the provided ingredients." if st.session_state.language == 'english' else "అందించిన పదార్థాలతో వంటకాలు రూపొందించబడలేదు.")
                        
                except Exception as e:
                    st.error(f"Recipe generation failed: {str(e)}")
    
    else:  # Recipe Type
        recipe_type = st.selectbox(
            "Select recipe type:" if st.session_state.language == 'english' else "వంటకం రకాన్ని ఎంచుకోండి:",
            ["Traditional", "Modern", "Fusion", "Healthy", "Quick"],
            format_func=lambda x: {
                "Traditional": "సాంప్రదాయ" if st.session_state.language == 'telugu' else "Traditional",
                "Modern": "ఆధునిక" if st.session_state.language == 'telugu' else "Modern",
                "Fusion": "మిశ్రమ" if st.session_state.language == 'telugu' else "Fusion",
                "Healthy": "ఆరోగ్యకరమైన" if st.session_state.language == 'telugu' else "Healthy",
                "Quick": "త్వరిత" if st.session_state.language == 'telugu' else "Quick"
            }.get(x, x)
        )
        
        if st.button("Generate Recipe" if st.session_state.language == 'english' else "వంటకం రూపొందించండి"):
            with st.spinner("Generating recipe..." if st.session_state.language == 'english' else "వంటకం రూపొందిస్తోంది..."):
                try:
                    recipe = services['recipe_generator'].generate_by_type(recipe_type)
                    
                    if recipe:
                        st.success("Recipe generated!" if st.session_state.language == 'english' else "వంటకం రూపొందించబడింది!")
                        
                        st.subheader(recipe.get('name', 'Generated Recipe'))
                        st.write(f"**Type:** {recipe.get('type', 'N/A')}")
                        st.write(f"**Ingredients:** {recipe.get('ingredients', 'N/A')}")
                        st.write(f"**Instructions:** {recipe.get('instructions', 'N/A')}")
                        st.write(f"**Cooking Time:** {recipe.get('cooking_time', 'N/A')}")
                        st.write(f"**Difficulty:** {recipe.get('difficulty', 'N/A')}")
                    else:
                        st.info("Could not generate a recipe of this type." if st.session_state.language == 'english' else "ఈ రకమైన వంటకం రూపొందించబడలేదు.")
                        
                except Exception as e:
                    st.error(f"Recipe generation failed: {str(e)}")

def render_historic_newspapers(services):
    """Render historic newspapers module"""
    st.header(get_localized_text('menu_newspapers', services))
    
    # Search functionality
    search_query = st.text_input(
        "Search historic content:" if st.session_state.language == 'english' else "చారిత్రక కంటెంట్‌ను వెతకండి:",
        placeholder="Enter keywords..." if st.session_state.language == 'english' else "కీలక పదాలను నమోదు చేయండి..."
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if search_query and st.button("Search" if st.session_state.language == 'english' else "వెతకండి"):
            with st.spinner("Searching..." if st.session_state.language == 'english' else "వెతుకుతోంది..."):
                try:
                    results = services['data_handler'].search_newspapers(search_query)
                    st.session_state.search_results = results
                except Exception as e:
                    st.error(f"Search failed: {str(e)}")
    
    with col2:
        if st.button("Show All" if st.session_state.language == 'english' else "అన్నీ చూపించు"):
            try:
                st.session_state.search_results = services['data_handler'].get_newspapers()
            except Exception as e:
                st.error(f"Failed to load newspapers: {str(e)}")
    
    # Display results
    if st.session_state.search_results:
        st.subheader(f"Found {len(st.session_state.search_results)} articles" if st.session_state.language == 'english' else f"{len(st.session_state.search_results)} వ్యాసాలు కనుగొనబడ్డాయి")
        
        for article in st.session_state.search_results:
            with st.expander(f"{article.get('title', 'Untitled')} - {article.get('date', 'No date')}"):
                st.write(f"**Source:** {article.get('source', 'Unknown')}")
                st.write(f"**Date:** {article.get('date', 'Unknown')}")
                st.write(f"**Content:** {article.get('content', 'No content available')}")
                
                # Translation option
                if st.button(f"Translate", key=f"translate_{article.get('id', 'unknown')}"):
                    target_lang = 'te' if st.session_state.language == 'english' else 'en'
                    try:
                        translated_content = services['translation'].translate_text(
                            article.get('content', ''), target_lang
                        )
                        st.write(f"**Translation:** {translated_content}")
                    except Exception as e:
                        st.error(f"Translation failed: {str(e)}")
    else:
        st.info("No articles found. Try a different search term or load all articles." if st.session_state.language == 'english' else "వ్యాసాలు కనుగొనబడలేదు. వేరే వెతుకు పదం ప్రయత్నించండి లేదా అన్ని వ్యాసాలను లోడ్ చేయండి.")

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Initialize services
    services = init_services()
    
    # Render language toggle
    render_language_toggle()
    
    # Main title
    st.title(get_localized_text('app_title', services))
    
    # Accessibility notice
    services['accessibility'].render_accessibility_notice(st.session_state.language)
    
    # Menu selection
    menu_options = [
        get_localized_text('menu_recipes', services),
        get_localized_text('menu_ingredients', services),
        get_localized_text('menu_generate', services),
        get_localized_text('menu_newspapers', services)
    ]
    
    selected_menu = st.sidebar.selectbox(
        "Choose Feature:" if st.session_state.language == 'english' else "ఫీచర్ ఎంచుకోండి:",
        menu_options
    )
    
    # Render selected module
    if selected_menu == get_localized_text('menu_recipes', services):
        render_recipe_module(services)
    elif selected_menu == get_localized_text('menu_ingredients', services):
        render_ingredient_recognition(services)
    elif selected_menu == get_localized_text('menu_generate', services):
        render_recipe_generator(services)
    elif selected_menu == get_localized_text('menu_newspapers', services):
        render_historic_newspapers(services)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "🍽️ **Sahachari** - Bridging Food & Culture" if st.session_state.language == 'english' else 
        "🍽️ **సహచారి** - ఆహారం మరియు సంస్కృతిని కలుపుతోంది"
    )

if __name__ == "__main__":
    main()
