"""
AIML Chatbot Integration Module
Handles conversational AI using AIML (Artificial Intelligence Markup Language)
"""

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


class AIMLChatbot:
    """
    AIML-based chatbot for face detection application.
    Provides conversational responses about detected faces and general queries.
    """

    def __init__(self, aiml_dir: str):
        """
        Initialize the AIML chatbot.
        
        Args:
            aiml_dir: Directory containing AIML files
        """
        self.aiml_dir = aiml_dir
        self.kernel = None
        self.face_count = 0
        self.last_detection_info = ""
        
        try:
            import aiml
            self.aiml_available = True
            self.kernel = aiml.Kernel()
            self._load_aiml_files()
            logger.info("AIML Chatbot initialized successfully")
        except ImportError:
            self.aiml_available = False
            logger.warning("AIML library not available. Using fallback responses.")
            self._create_fallback_responses()

    def _load_aiml_files(self):
        """Load AIML files from the data directory."""
        try:
            if not os.path.exists(self.aiml_dir):
                logger.warning(f"AIML directory not found: {self.aiml_dir}. Creating default AIML.")
                os.makedirs(self.aiml_dir, exist_ok=True)
                self._create_default_aiml()
            
            aiml_files = [f for f in os.listdir(self.aiml_dir) if f.endswith(".xml")]
            if aiml_files:
                for aiml_file in aiml_files:
                    file_path = os.path.join(self.aiml_dir, aiml_file)
                    self.kernel.learn(file_path)
                    logger.info(f"Loaded AIML file: {aiml_file}")
            else:
                logger.info("No AIML files found. Creating default AIML.")
                self._create_default_aiml()
                self._load_aiml_files()
        except Exception as e:
            logger.error(f"Error loading AIML files: {e}")

    def _create_default_aiml(self):
        """Create default AIML files for basic responses."""
        default_aiml = """<?xml version="1.0" encoding="UTF-8"?>
<aiml version="2.0">
    <!-- Greeting patterns -->
    <category>
        <pattern>HELLO</pattern>
        <template>Hello! I'm a face detection chatbot. Ask me about detected faces or anything else!</template>
    </category>
    
    <category>
        <pattern>HI</pattern>
        <template>Hi there! How can I help you today?</template>
    </category>
    
    <!-- Face detection queries -->
    <category>
        <pattern>HOW MANY FACES</pattern>
        <template>I can see <star/> faces in the current frame.</template>
    </category>
    
    <category>
        <pattern>DETECT FACE*</pattern>
        <template>Face detection is active. I'm scanning the video stream for faces.</template>
    </category>
    
    <!-- Help -->
    <category>
        <pattern>HELP</pattern>
        <template>I can help you with:
- Face detection information
- General conversation
- Application status
Type your question to get started!</template>
    </category>
    
    <!-- Fallback -->
    <category>
        <pattern>*</pattern>
        <template>That's interesting! Could you tell me more?</template>
    </category>
</aiml>"""
        
        default_file = os.path.join(self.aiml_dir, "startup.xml")
        with open(default_file, "w", encoding="utf-8") as f:
            f.write(default_aiml)
        logger.info(f"Created default AIML file: {default_file}")

    def _create_fallback_responses(self):
        """Create fallback response templates when AIML is not available."""
        self.fallback_responses = {
            "hello": "Hello! I'm a face detection chatbot.",
            "how are you": "I'm working well! Detecting faces in real-time.",
            "faces": "I can detect and track multiple faces in the video stream.",
            "help": "I can help with face detection info and general questions.",
            "status": "Face detection system is running normally.",
            "default": "That's interesting! Tell me more about that.",
        }

    def respond(self, user_input: str) -> str:
        """
        Generate a response to user input.
        
        Args:
            user_input: User's input message
            
        Returns:
            Chatbot response
        """
        try:
            if self.aiml_available and self.kernel:
                response = self.kernel.respond(user_input)
                return response if response else self.fallback_responses["default"]
            else:
                return self._get_fallback_response(user_input)
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Sorry, I encountered an error processing your request."

    def _get_fallback_response(self, user_input: str) -> str:
        """Get a fallback response based on keywords in user input."""
        user_input_lower = user_input.lower()
        
        for keyword, response in self.fallback_responses.items():
            if keyword in user_input_lower:
                return response
        
        return self.fallback_responses["default"]

    def update_face_info(self, face_count: int, detection_info: str = ""):
        """
        Update chatbot with current face detection information.
        
        Args:
            face_count: Number of detected faces
            detection_info: Additional detection information
        """
        self.face_count = face_count
        self.last_detection_info = detection_info

    def get_detection_status(self) -> str:
        """Get a status message about detected faces."""
        if self.face_count == 0:
            return "No faces detected in the current frame."
        elif self.face_count == 1:
            return "Detected 1 face in the current frame."
        else:
            return f"Detected {self.face_count} faces in the current frame."

    def set_context(self, context_key: str, context_value: str):
        """
        Set context information for the chatbot.
        
        Args:
            context_key: Context variable name
            context_value: Context variable value
        """
        if self.aiml_available and self.kernel:
            try:
                self.kernel.setPredicate(context_key, context_value)
                logger.debug(f"Set context: {context_key} = {context_value}")
            except Exception as e:
                logger.error(f"Error setting context: {e}")

    def get_context(self, context_key: str) -> Optional[str]:
        """
        Get context information from the chatbot.
        
        Args:
            context_key: Context variable name
            
        Returns:
            Context value or None
        """
        if self.aiml_available and self.kernel:
            try:
                value = self.kernel.getPredicate(context_key)
                return value if value else None
            except Exception as e:
                logger.error(f"Error getting context: {e}")
        return None
