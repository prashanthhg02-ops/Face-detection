"""
Configuration settings for Face Detection with AIML project
"""

import os

# Project directories
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
AIML_DIR = os.path.join(DATA_DIR, "aiml")
MODELS_DIR = os.path.join(DATA_DIR, "models")
FACES_DIR = os.path.join(DATA_DIR, "faces")

# Create directories if they don't exist
for directory in [DATA_DIR, AIML_DIR, MODELS_DIR, FACES_DIR]:
    os.makedirs(directory, exist_ok=True)

# Face Detection Configuration
FACE_DETECTION_CONFIG = {
    "confidence_threshold": 0.5,
    "model_type": "haarcascade",  # Options: "haarcascade", "dnn", "dlib"
    "scale_factor": 1.1,
    "min_neighbors": 5,
    "min_face_size": (30, 30),
    "max_face_size": (500, 500),
}

# Webcam Configuration
WEBCAM_CONFIG = {
    "camera_id": 0,
    "frame_width": 1280,
    "frame_height": 720,
    "fps": 30,
    "flip_horizontal": True,
}

# AIML Configuration
AIML_CONFIG = {
    "engine": "aiml",
    "brain_file": os.path.join(AIML_DIR, "startup.xml"),
    "learning_file": os.path.join(AIML_DIR, "learned.xml"),
    "enable_learning": True,
}

# Display Configuration
DISPLAY_CONFIG = {
    "show_fps": True,
    "show_confidence": True,
    "box_color": (0, 255, 0),  # BGR format - Green
    "text_color": (255, 255, 255),  # White
    "line_thickness": 2,
    "font_scale": 0.6,
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "log_file": os.path.join(PROJECT_ROOT, "app.log"),
}
