<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Face Detection with AIML Project Instructions

## Project Overview
This is a real-time face detection application integrated with an AIML (Artificial Intelligence Markup Language) chatbot. The project demonstrates computer vision capabilities combined with conversational AI.

## Key Features
- Real-time face detection from webcam
- Multiple face tracking
- AIML-powered conversational chatbot
- Face recognition and ROI extraction
- Performance-optimized detection

## Development Guidelines

### Code Structure
- `src/face_detector.py` - Core face detection logic
- `src/aiml_chatbot.py` - AIML chatbot integration
- `src/main.py` - Main application entry point
- `src/config.py` - Configuration settings
- `tests/` - Unit tests

### Required Dependencies
- OpenCV (cv2)
- TensorFlow
- NumPy
- AIML

### Running the Application
```bash
python -m src.main
```

### Testing
```bash
python -m pytest tests/
```

### Controls During Execution
- **q** - Quit application
- **s** - Save detected faces
- **c** - Chat with AIML chatbot

## AIML Integration
Custom AIML patterns can be added in `data/aiml/` directory. The chatbot provides:
- Face detection status queries
- General conversation
- Application help and information

## Project Structure
```
.
├── src/
│   ├── __init__.py
│   ├── face_detector.py
│   ├── aiml_chatbot.py
│   ├── main.py
│   └── config.py
├── data/
│   ├── aiml/
│   ├── models/
│   └── faces/
├── tests/
├── requirements.txt
├── setup.py
└── README.md
```

## Customization Tips
- Adjust detection parameters in `src/config.py`
- Add custom AIML patterns in `data/aiml/`
- Modify display settings for different screen resolutions
- Switch between detection models (haarcascade, dnn, dlib)

## Performance Considerations
- Frame rate and resolution affect CPU usage
- Face detection scale factor impacts accuracy vs speed
- AIML response times depend on knowledge base size

## Troubleshooting
- Ensure webcam permissions are granted
- Check AIML directory structure for proper file loading
- Verify all dependencies are installed via `pip install -r requirements.txt`

## Future Enhancements
- GPU acceleration for faster detection
- Face recognition and identification
- Emotion detection
- Multiple language support for chatbot
- Cloud-based processing option
