# 🌐 Sahachari – A Bilingual Cultural & Culinary Companion

### **Bridging Food, Language & Culture Through Inclusive AI**

---

## 📖 Overview

**Sahachari** is a bilingual (Telugu–English) web platform designed to celebrate and preserve regional culinary heritage through accessible AI. Built with **Streamlit**, it offers seamless **recipe translation**, **text-to-speech narration**, **ingredient detection from images**, and **custom recipe generation**. The platform places a strong emphasis on **accessibility**, **language inclusivity**, and **cultural preservation**.

---

## 👤 Target Audience

* Native Telugu speakers and non-Telugu speakers exploring Telugu cuisine
* Elderly users with accessibility needs
* Students and researchers of food, language, or regional history
* Anyone curious about cultural dishes with language support

---

## 💡 Key Features

| Feature                     | Description                                                                |
| --------------------------- | -------------------------------------------------------------------------- |
| 🔄 **Translation Service**  | Telugu–English recipe translation with API and offline fallback            |
| 🔊 **Text-to-Speech (TTS)** | Converts translated recipes to audio in Telugu or English                  |
| 🖼 **Image Recognition**    | Recognizes ingredients from uploaded photos using Google/Azure APIs        |
| 🍲 **Recipe Generator**     | Creates traditional or modern recipes using OpenAI/Spoonacular APIs        |
| 📰 **Historic Archives**    | Explores vintage newspaper snippets related to food and culture (optional) |
| ♿ **Accessibility Tools**   | High-contrast mode, large fonts, and keyboard/screen reader support        |

---

## 🧱 System Architecture

### 🖥 Frontend

* **Framework**: [Streamlit](https://streamlit.io/) – lightweight and Pythonic
* **Layout**: Wide layout with sidebar for navigation and settings
* **State Management**: Handled via `st.session_state` for language and mode persistence
* **Accessibility**: Built-in support for high contrast, large text, and keyboard navigation

---

### 🧠 Backend (Modular Services)

| Module                    | Path                           | Description                                                      |
| ------------------------- | ------------------------------ | ---------------------------------------------------------------- |
| `TranslationService`      | `modules/translation.py`       | Uses Google Translate API and `googletrans` fallback             |
| `TextToSpeechService`     | `modules/text_to_speech.py`    | Supports Google Cloud TTS and gTTS fallback                      |
| `ImageRecognitionService` | `modules/image_recognition.py` | Uses Google Vision / Azure Vision or keyword-based fallback      |
| `RecipeGenerator`         | `modules/recipe_generator.py`  | Supports dynamic and template-based recipe creation              |
| `DataHandler`             | `modules/data_handler.py`      | Abstracted data layer for JSON, CSV, and future database support |
| `AccessibilityHelper`     | `modules/accessibility.py`     | Manages contrast mode, font size, and accessibility UI options   |

---

## 📦 Data Management

* **Current**: JSON/CSV-based storage for temporary and static content
* **Planned**: Migration to relational DB (SQLite → PostgreSQL)
* **Data Access Layer**: Abstracted with support for switching data backends easily

---

## 🔁 Workflow / Data Flow

1. **User Input**: Via Streamlit widgets (text, audio, image)
2. **Service Routing**: Handled via modular service handlers
3. **API Communication**: External APIs called conditionally with fallbacks
4. **Processing**: Translations, audio, recognition, or generation as needed
5. **Display**: Output shown in user-preferred language with optional audio

---

## 🌐 Language Flow

* Users choose **English** or **Telugu** in the UI.
* UI elements update via `constants.py` mapping.
* Text content is translated and converted to audio if needed.

---

## 🔐 Environment Configuration

Set via `.env` or server dashboard:

```env
GOOGLE_TRANSLATE_API_KEY=
GOOGLE_CLOUD_TTS_API_KEY=
GOOGLE_VISION_API_KEY=
AZURE_COMPUTER_VISION_KEY=
AZURE_COMPUTER_VISION_ENDPOINT=
OPENAI_API_KEY=
SPOONACULAR_API_KEY=
```

---

## 🧰 External Dependencies

### 🔑 APIs

* Google Translate API
* Google Cloud Text-to-Speech
* Google Vision / Azure Vision API
* Spoonacular / OpenAI for recipe generation

### 📦 Python Libraries

```txt
streamlit
googletrans==4.0.0rc1
gtts
Pillow
pandas
requests
```

---

## 🚀 Deployment Strategy

### 🎯 Preferred: [Streamlit Cloud](https://streamlit.io/cloud)

* Easy environment variable setup
* Built-in support for GitHub integration

### 🧩 Alternatives:

* **Heroku** (with Dockerfile or buildpacks)
* **Bare-metal/VM** with gunicorn or `streamlit run`

### 🧠 Performance

* Service initialization is cached using `@st.cache_resource`
* API responses can be memoized for speed
* File and text input sizes configurable in settings

---

## 🔄 Data Migration Path

| Phase       | Storage Type | Description                                    |
| ----------- | ------------ | ---------------------------------------------- |
| Current     | JSON / CSV   | Quick development & prototyping                |
| Development | SQLite       | Lightweight, local DB with relational features |
| Production  | PostgreSQL   | Scalable, cloud-compatible DB with migrations  |

---

## ♿ Accessibility Compliance

Following WCAG and inclusive design:

* High-contrast toggle
* Font size scaling
* Screen reader support
* Keyboard-only navigation
* Alt text for all visuals

---

## 📌 Summary

**Sahachari** is a thoughtfully built, culturally anchored application that:

* Connects people to heritage through language and food
* Prioritizes accessibility and inclusivity
* Supports modular expansion for new services (e.g., voice search, video recipes)
* Enables easy deployment and community participation

