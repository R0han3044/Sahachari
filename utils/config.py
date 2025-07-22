import os
import json
import streamlit as st

class Config:
    """Configuration management for the Sahachari application"""
    
    def __init__(self):
        self.config_file = 'config.json'
        self.default_config = {
            'data_source': 'temporary',
            'api_settings': {
                'google_translate_enabled': True,
                'google_vision_enabled': True,
                'azure_vision_enabled': False,
                'openai_enabled': False,
                'spoonacular_enabled': False
            },
            'app_settings': {
                'default_language': 'english',
                'max_file_size_mb': 10,
                'supported_image_formats': ['jpg', 'jpeg', 'png'],
                'max_text_length': 5000,
                'cache_duration': 3600
            },
            'accessibility_settings': {
                'high_contrast_mode': False,
                'large_text_mode': False,
                'screen_reader_mode': False,
                'keyboard_navigation': True
            },
            'ui_settings': {
                'theme': 'light',
                'sidebar_expanded': True,
                'show_accessibility_controls': True,
                'show_statistics': False
            }
        }
        
        # Load configuration
        self.config = self._load_config()
        
        # Set up API keys from environment
        self._setup_api_keys()
    
    def _load_config(self):
        """Load configuration from file or create default"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Merge with default config to ensure all keys exist
                return self._merge_configs(self.default_config, config)
            else:
                # Create default config file
                self._save_config(self.default_config)
                return self.default_config.copy()
                
        except Exception as e:
            st.warning(f"Failed to load configuration: {str(e)}. Using defaults.")
            return self.default_config.copy()
    
    def _merge_configs(self, default, loaded):
        """Merge loaded config with default config"""
        merged = default.copy()
        
        for key, value in loaded.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value
        
        return merged
    
    def _setup_api_keys(self):
        """Setup API keys from environment variables"""
        self.api_keys = {
            'google_translate': os.getenv('GOOGLE_TRANSLATE_API_KEY'),
            'google_vision': os.getenv('GOOGLE_VISION_API_KEY'),
            'google_cloud_tts': os.getenv('GOOGLE_CLOUD_TTS_API_KEY'),
            'azure_computer_vision': os.getenv('AZURE_COMPUTER_VISION_KEY'),
            'azure_endpoint': os.getenv('AZURE_COMPUTER_VISION_ENDPOINT'),
            'openai': os.getenv('OPENAI_API_KEY'),
            'spoonacular': os.getenv('SPOONACULAR_API_KEY')
        }
        
        # Update API settings based on available keys
        self.config['api_settings']['google_translate_enabled'] = bool(self.api_keys['google_translate'])
        self.config['api_settings']['google_vision_enabled'] = bool(self.api_keys['google_vision'])
        self.config['api_settings']['azure_vision_enabled'] = bool(self.api_keys['azure_computer_vision'])
        self.config['api_settings']['openai_enabled'] = bool(self.api_keys['openai'])
        self.config['api_settings']['spoonacular_enabled'] = bool(self.api_keys['spoonacular'])
    
    def _save_config(self, config):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"Failed to save configuration: {str(e)}")
    
    def get(self, key, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key, value):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        
        # Save to file
        self._save_config(self.config)
    
    @property
    def data_source(self):
        """Get current data source"""
        return self.config['data_source']
    
    @data_source.setter
    def data_source(self, value):
        """Set data source"""
        self.config['data_source'] = value
        self._save_config(self.config)
    
    @property
    def default_language(self):
        """Get default language"""
        return self.config['app_settings']['default_language']
    
    @property
    def max_file_size_mb(self):
        """Get maximum file size in MB"""
        return self.config['app_settings']['max_file_size_mb']
    
    @property
    def supported_image_formats(self):
        """Get supported image formats"""
        return self.config['app_settings']['supported_image_formats']
    
    def is_api_enabled(self, api_name):
        """Check if a specific API is enabled"""
        return self.config['api_settings'].get(f'{api_name}_enabled', False)
    
    def get_api_key(self, api_name):
        """Get API key for a specific service"""
        return self.api_keys.get(api_name)
    
    def update_accessibility_settings(self, settings):
        """Update accessibility settings"""
        self.config['accessibility_settings'].update(settings)
        self._save_config(self.config)
    
    def get_accessibility_settings(self):
        """Get accessibility settings"""
        return self.config['accessibility_settings']
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self.default_config.copy()
        self._save_config(self.config)
        st.success("Configuration reset to defaults")
    
    def export_config(self, filename=None):
        """Export configuration to file"""
        if not filename:
            filename = f"sahachari_config_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return filename
        except Exception as e:
            st.error(f"Failed to export configuration: {str(e)}")
            return None
    
    def import_config(self, config_file):
        """Import configuration from file"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # Validate imported config
            if self._validate_config(imported_config):
                self.config = self._merge_configs(self.default_config, imported_config)
                self._save_config(self.config)
                st.success("Configuration imported successfully")
                return True
            else:
                st.error("Invalid configuration file")
                return False
                
        except Exception as e:
            st.error(f"Failed to import configuration: {str(e)}")
            return False
    
    def _validate_config(self, config):
        """Validate configuration structure"""
        required_sections = ['data_source', 'api_settings', 'app_settings']
        
        try:
            for section in required_sections:
                if section not in config:
                    return False
            return True
        except:
            return False
    
    def get_environment_info(self):
        """Get environment information for debugging"""
        return {
            'data_source': self.data_source,
            'api_keys_available': {
                name: bool(key) for name, key in self.api_keys.items()
            },
            'config_file_exists': os.path.exists(self.config_file),
            'app_settings': self.config['app_settings']
        }
    
    def render_admin_panel(self):
        """Render admin configuration panel"""
        st.subheader("⚙️ Configuration")
        
        # Data source selection
        data_sources = ['temporary', 'production']
        current_source = st.selectbox(
            "Data Source",
            data_sources,
            index=data_sources.index(self.data_source)
        )
        
        if current_source != self.data_source:
            self.data_source = current_source
            st.rerun()
        
        # API settings
        st.markdown("### API Settings")
        for api_name, enabled in self.config['api_settings'].items():
            if api_name.endswith('_enabled'):
                service_name = api_name.replace('_enabled', '')
                has_key = bool(self.get_api_key(service_name))
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{service_name.title()}**: {'✅' if has_key else '❌'}")
                with col2:
                    st.write("Available" if has_key else "No API Key")
        
        # App settings
        st.markdown("### App Settings")
        max_file_size = st.number_input(
            "Max File Size (MB)",
            min_value=1,
            max_value=100,
            value=self.max_file_size_mb
        )
        
        if max_file_size != self.max_file_size_mb:
            self.set('app_settings.max_file_size_mb', max_file_size)
        
        # Export/Import
        st.markdown("### Configuration Management")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Export Config"):
                filename = self.export_config()
                if filename:
                    st.success(f"Exported to {filename}")
        
        with col2:
            uploaded_config = st.file_uploader("Import Config", type=['json'])
            if uploaded_config:
                if self.import_config(uploaded_config):
                    st.rerun()
        
        with col3:
            if st.button("Reset to Defaults"):
                self.reset_to_defaults()
                st.rerun()
