# Sahachari - Bilingual Food & Culture Bridge

## Overview

Sahachari is a bilingual (Telugu-English) web application built with Streamlit that bridges food, language, and culture. The application provides recipe translation with text-to-speech capabilities, ingredient recognition from images, recipe generation, and exploration of historic newspapers. It emphasizes accessibility and inclusivity as core design principles.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit for rapid Python-based web UI development
- **Layout**: Wide layout with expandable sidebar for navigation and accessibility controls
- **Responsiveness**: Built-in Streamlit responsiveness with custom accessibility enhancements
- **State Management**: Streamlit session state for maintaining user preferences and application state

### Backend Architecture
- **Language**: Python-based modular architecture
- **Service Pattern**: Each major feature is implemented as a separate service module
- **Configuration Management**: Centralized configuration system with environment variable support
- **Caching**: Streamlit's `@st.cache_resource` decorator for service initialization

### Data Storage Solutions
- **Current**: File-based storage using JSON/CSV for temporary data
- **Future**: Designed to migrate to database solutions (SQLite/PostgreSQL)
- **Data Handler**: Abstracted data access layer that can switch between data sources

## Key Components

### Core Services
1. **Translation Service** (`modules/translation.py`)
   - Primary: Google Translate API
   - Fallback: googletrans library
   - Supports Telugu-English bidirectional translation

2. **Text-to-Speech Service** (`modules/text_to_speech.py`)
   - Primary: Google Cloud TTS API
   - Fallback: gTTS (Google Text-to-Speech)
   - Supports both English and Telugu audio generation

3. **Image Recognition Service** (`modules/image_recognition.py`)
   - Primary: Google Vision API
   - Secondary: Azure Computer Vision
   - Fallback: Basic image analysis with food keyword filtering

4. **Recipe Generator** (`modules/recipe_generator.py`)
   - External APIs: Spoonacular API, OpenAI API
   - Fallback: Template-based local generation
   - Supports traditional and modern dish generation

5. **Data Handler** (`modules/data_handler.py`)
   - Abstracted data access layer
   - Currently handles JSON/CSV files
   - Designed for easy migration to database systems

6. **Accessibility Helper** (`modules/accessibility.py`)
   - High contrast mode support
   - Large text options
   - Screen reader optimization
   - Keyboard navigation support

### Configuration System
- **Config Manager** (`utils/config.py`): Centralized configuration with JSON file storage
- **Constants** (`utils/constants.py`): Language mappings, menu items, and UI text translations

## Data Flow

1. **User Input**: Users interact through Streamlit UI components
2. **Service Layer**: Requests are processed by appropriate service modules
3. **External APIs**: Services make calls to external APIs with fallback mechanisms
4. **Data Processing**: Results are processed and cached for performance
5. **Response**: Translated/processed content is displayed to users

### Language Flow
- User selects language preference
- All UI elements update based on language constants
- Content translation happens through Translation Service
- Text-to-speech generates audio in selected language

## External Dependencies

### Required APIs (with fallbacks)
- **Google Translate API** (fallback: googletrans library)
- **Google Cloud TTS API** (fallback: gTTS)
- **Google Vision API** (fallback: Azure Computer Vision, then basic analysis)
- **Spoonacular API** (fallback: OpenAI API, then template-based generation)

### Python Libraries
- `streamlit`: Web application framework
- `googletrans`: Translation fallback
- `gtts`: Text-to-speech fallback
- `PIL`: Image processing
- `pandas`: Data manipulation
- `requests`: HTTP client for API calls

### Environment Variables
- `GOOGLE_TRANSLATE_API_KEY`
- `GOOGLE_CLOUD_TTS_API_KEY`
- `GOOGLE_VISION_API_KEY`
- `AZURE_COMPUTER_VISION_KEY`
- `AZURE_COMPUTER_VISION_ENDPOINT`
- `OPENAI_API_KEY`
- `SPOONACULAR_API_KEY`

## Deployment Strategy

### Platform Options
- **Primary**: Streamlit Cloud (recommended for Streamlit apps)
- **Alternatives**: Heroku, custom server deployment
- **Configuration**: Environment variables for API keys and settings

### Performance Considerations
- Service initialization caching with `@st.cache_resource`
- Configurable cache duration for API responses
- File size limits for image uploads (configurable)
- Maximum text length limits for processing

### Data Migration Strategy
- Current: File-based temporary data system
- Future: Database integration (SQLite for development, PostgreSQL for production)
- Data Handler abstraction enables seamless migration
- Configuration-driven data source switching

### Accessibility Compliance
- WCAG guidelines implementation
- Screen reader compatibility
- Keyboard navigation support
- High contrast and large text options
- Alt text for images and UI elements

The architecture prioritizes modularity, accessibility, and scalability while maintaining simplicity for rapid development and deployment.