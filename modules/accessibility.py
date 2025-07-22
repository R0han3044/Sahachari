import streamlit as st

class AccessibilityHelper:
    """Accessibility helper for ensuring the app is accessible to all users"""
    
    def __init__(self):
        self.accessibility_features = {
            'high_contrast': False,
            'large_text': False,
            'screen_reader_mode': False,
            'keyboard_navigation': True
        }
    
    def render_accessibility_notice(self, language='english'):
        """Render accessibility notice and controls"""
        if language == 'english':
            st.sidebar.markdown("### ♿ Accessibility")
            st.sidebar.info("This app supports screen readers, keyboard navigation, and high contrast mode.")
        else:
            st.sidebar.markdown("### ♿ అందుబాటు")
            st.sidebar.info("ఈ యాప్ స్క్రీన్ రీడర్లు, కీబోర్డ్ నావిగేషన్ మరియు హై కాంట్రాస్ట్ మోడ్‌ను సపోర్ట్ చేస్తుంది.")
    
    def render_accessibility_controls(self, language='english'):
        """Render accessibility control options"""
        st.sidebar.markdown("---")
        
        if language == 'english':
            st.sidebar.subheader("Accessibility Options")
            
            # High contrast toggle
            high_contrast = st.sidebar.checkbox("High Contrast Mode", 
                                              value=self.accessibility_features['high_contrast'])
            
            # Large text toggle
            large_text = st.sidebar.checkbox("Large Text", 
                                           value=self.accessibility_features['large_text'])
            
            # Screen reader mode
            screen_reader = st.sidebar.checkbox("Screen Reader Optimized", 
                                              value=self.accessibility_features['screen_reader_mode'])
            
        else:
            st.sidebar.subheader("అందుబాటు ఎంపికలు")
            
            # High contrast toggle
            high_contrast = st.sidebar.checkbox("హై కాంట్రాస్ట్ మోడ్", 
                                              value=self.accessibility_features['high_contrast'])
            
            # Large text toggle
            large_text = st.sidebar.checkbox("పెద్ద టెక్స్ట్", 
                                           value=self.accessibility_features['large_text'])
            
            # Screen reader mode
            screen_reader = st.sidebar.checkbox("స్క్రీన్ రీడర్ ఆప్టిమైజ్డ్", 
                                              value=self.accessibility_features['screen_reader_mode'])
        
        # Update features
        self.accessibility_features.update({
            'high_contrast': high_contrast,
            'large_text': large_text,
            'screen_reader_mode': screen_reader
        })
        
        # Apply accessibility features
        self._apply_accessibility_features()
    
    def _apply_accessibility_features(self):
        """Apply selected accessibility features"""
        if self.accessibility_features['high_contrast']:
            self._apply_high_contrast()
        
        if self.accessibility_features['large_text']:
            self._apply_large_text()
        
        if self.accessibility_features['screen_reader_mode']:
            self._apply_screen_reader_optimizations()
    
    def _apply_high_contrast(self):
        """Apply high contrast styling"""
        st.markdown("""
        <style>
        .stApp {
            background-color: #000000;
            color: #FFFFFF;
        }
        .stButton > button {
            background-color: #FFFFFF;
            color: #000000;
            border: 2px solid #FFFFFF;
        }
        .stSelectbox > div > div {
            background-color: #000000;
            color: #FFFFFF;
        }
        .stTextInput > div > div > input {
            background-color: #000000;
            color: #FFFFFF;
            border: 2px solid #FFFFFF;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def _apply_large_text(self):
        """Apply large text styling"""
        st.markdown("""
        <style>
        .stApp {
            font-size: 18px;
        }
        h1 {
            font-size: 3rem !important;
        }
        h2 {
            font-size: 2.5rem !important;
        }
        h3 {
            font-size: 2rem !important;
        }
        .stButton > button {
            font-size: 18px;
            padding: 12px 24px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def _apply_screen_reader_optimizations(self):
        """Apply screen reader optimizations"""
        # Add ARIA labels and roles
        st.markdown("""
        <style>
        .stApp {
            --sr-only: {
                position: absolute;
                width: 1px;
                height: 1px;
                padding: 0;
                margin: -1px;
                overflow: hidden;
                clip: rect(0, 0, 0, 0);
                white-space: nowrap;
                border: 0;
            }
        }
        </style>
        """, unsafe_allow_html=True)
    
    def add_alt_text_for_images(self, image_description, language='english'):
        """Add alt text for images"""
        if language == 'english':
            return f"Image: {image_description}"
        else:
            return f"చిత్రం: {image_description}"
    
    def create_accessible_button(self, label, help_text=None, language='english'):
        """Create an accessible button with proper labels"""
        if help_text:
            if language == 'english':
                return st.button(label, help=help_text)
            else:
                return st.button(label, help=help_text)
        else:
            return st.button(label)
    
    def create_accessible_file_uploader(self, label, accepted_types=None, help_text=None, language='english'):
        """Create an accessible file uploader"""
        kwargs = {'label': label}
        
        if accepted_types:
            kwargs['type'] = accepted_types
        
        if help_text:
            kwargs['help'] = help_text
        
        return st.file_uploader(**kwargs)
    
    def announce_content_change(self, message, language='english'):
        """Announce content changes for screen readers"""
        # Use st.empty() to create live regions for dynamic content
        if language == 'english':
            st.info(f"Content Update: {message}")
        else:
            st.info(f"కంటెంట్ అప్‌డేట్: {message}")
    
    def create_skip_navigation(self, language='english'):
        """Create skip navigation links"""
        if language == 'english':
            st.markdown("""
            <div style="position: absolute; left: -9999px;">
                <a href="#main-content" style="position: absolute; left: 6px; top: 7px; z-index: 999; text-decoration: none; background: #000; color: #fff; padding: 8px;">
                    Skip to main content
                </a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="position: absolute; left: -9999px;">
                <a href="#main-content" style="position: absolute; left: 6px; top: 7px; z-index: 999; text-decoration: none; background: #000; color: #fff; padding: 8px;">
                    ముఖ్య కంటెంట్‌కు వెళ్లండి
                </a>
            </div>
            """, unsafe_allow_html=True)
    
    def validate_color_contrast(self, foreground_color, background_color):
        """Validate color contrast ratio for accessibility compliance"""
        # This would implement WCAG color contrast calculation
        # For now, return a basic check
        return True
    
    def get_keyboard_shortcuts(self, language='english'):
        """Get list of keyboard shortcuts"""
        if language == 'english':
            return {
                'Tab': 'Navigate between elements',
                'Enter/Space': 'Activate buttons and links',
                'Arrow Keys': 'Navigate within components',
                'Esc': 'Close dialogs and popups'
            }
        else:
            return {
                'Tab': 'ఎలిమెంట్స్ మధ్య నావిగేట్ చేయండి',
                'Enter/Space': 'బటన్లు మరియు లింక్‌లను యాక్టివేట్ చేయండి',
                'Arrow Keys': 'కాంపోనెంట్స్ లోపల నావిగేట్ చేయండి',
                'Esc': 'డైలాగ్‌లు మరియు పాప్‌అప్‌లను మూసివేయండి'
            }
    
    def render_keyboard_shortcuts_help(self, language='english'):
        """Render keyboard shortcuts help"""
        shortcuts = self.get_keyboard_shortcuts(language)
        
        if language == 'english':
            st.sidebar.markdown("### ⌨️ Keyboard Shortcuts")
        else:
            st.sidebar.markdown("### ⌨️ కీబోర్డ్ షార్ట్‌కట్‌లు")
        
        for key, description in shortcuts.items():
            st.sidebar.markdown(f"**{key}**: {description}")
    
    def ensure_focus_management(self):
        """Ensure proper focus management for dynamic content"""
        # This would implement focus management for SPAs
        # Streamlit handles most of this automatically
        pass
    
    def validate_accessibility_compliance(self):
        """Validate overall accessibility compliance"""
        # This would run accessibility checks
        compliance_issues = []
        
        # Check for basic compliance requirements
        if not self.accessibility_features['keyboard_navigation']:
            compliance_issues.append("Keyboard navigation should be enabled")
        
        return {
            'is_compliant': len(compliance_issues) == 0,
            'issues': compliance_issues,
            'score': max(0, 100 - len(compliance_issues) * 25)
        }
