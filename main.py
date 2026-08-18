"""
Main Application for Face Detection with AIML
Real-time face detection with conversational AI chatbot integration
"""

import cv2
import logging
import os
from datetime import datetime
from .face_detector import FaceDetector
from .aiml_chatbot import AIMLChatbot
from .config import (
    WEBCAM_CONFIG,
    DISPLAY_CONFIG,
    LOGGING_CONFIG,
    FACES_DIR,
    AIML_DIR,
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG["level"]),
    format=LOGGING_CONFIG["format"],
    handlers=[
        logging.FileHandler(LOGGING_CONFIG["log_file"]),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class FaceDetectionApp:
    """
    Main application for face detection with AIML integration.
    Manages webcam input, face detection, and chatbot interactions.
    """

    def __init__(self):
        """Initialize the application."""
        logger.info("Initializing Face Detection Application...")
        
        self.face_detector = FaceDetector(model_type="haarcascade")
        self.chatbot = AIMLChatbot(AIML_DIR)
        self.cap = None
        self.running = False
        self.frame_count = 0
        self.total_faces_detected = 0
        
        logger.info("Application initialized successfully")

    def initialize_webcam(self) -> bool:
        """
        Initialize the webcam.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.cap = cv2.VideoCapture(WEBCAM_CONFIG["camera_id"])
            
            if not self.cap.isOpened():
                logger.error("Failed to open webcam")
                return False
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WEBCAM_CONFIG["frame_width"])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WEBCAM_CONFIG["frame_height"])
            self.cap.set(cv2.CAP_PROP_FPS, WEBCAM_CONFIG["fps"])
            
            logger.info("Webcam initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing webcam: {e}")
            return False

    def process_frame(self, frame):
        """
        Process a single frame for face detection.
        
        Args:
            frame: Input frame from webcam
            
        Returns:
            Processed frame with face detection results
        """
        # Flip frame if configured
        if WEBCAM_CONFIG["flip_horizontal"]:
            frame = cv2.flip(frame, 1)
        
        # Detect faces
        faces = self.face_detector.detect_faces(frame)
        self.total_faces_detected += len(faces)
        
        # Draw faces on frame
        frame = self.face_detector.draw_faces(frame, faces)
        
        # Update chatbot with detection info
        self.chatbot.update_face_info(len(faces))
        
        # Add FPS and info display
        frame = self._add_info_display(frame, len(faces))
        
        return frame, faces

    def _add_info_display(self, frame, face_count):
        """
        Add information display on the frame.
        
        Args:
            frame: Input frame
            face_count: Number of detected faces
            
        Returns:
            Frame with information display
        """
        info_text = [
            f"Faces Detected: {face_count}",
            f"Frames: {self.frame_count}",
            f"Total Faces: {self.total_faces_detected}",
            "Press 'q' to quit | 's' to save | 'c' to chat",
        ]
        
        y_offset = 30
        for text in info_text:
            cv2.putText(
                frame,
                text,
                (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1,
            )
            y_offset += 25
        
        return frame

    def handle_keyboard_input(self, key, frame, faces):
        """
        Handle keyboard input.
        
        Args:
            key: Key pressed (ord value)
            frame: Current frame
            faces: Detected faces in current frame
            
        Returns:
            True to continue, False to exit
        """
        if key == ord("q"):
            logger.info("Quit command received")
            return False
        elif key == ord("s"):
            self._save_faces(frame, faces)
        elif key == ord("c"):
            self._start_chat_session()
        
        return True

    def _save_faces(self, frame, faces):
        """
        Save detected faces to files.
        
        Args:
            frame: Current frame
            faces: Detected faces
        """
        if len(faces) == 0:
            print("No faces to save")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for idx, face in enumerate(faces):
            filename = os.path.join(FACES_DIR, f"face_{timestamp}_{idx}.jpg")
            success = self.face_detector.save_face(frame, face, filename)
            if success:
                print(f"Face {idx + 1} saved to {filename}")

    def _start_chat_session(self):
        """Start an interactive chat session with the AIML chatbot."""
        print("\n" + "=" * 50)
        print("Chat Session Started (Press Ctrl+C to exit)")
        print("=" * 50)
        
        try:
            while True:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                
                response = self.chatbot.respond(user_input)
                print(f"Bot: {response}\n")
        except KeyboardInterrupt:
            print("\nChat session ended")

    def run(self):
        """Run the main application loop."""
        if not self.initialize_webcam():
            logger.error("Failed to initialize webcam. Exiting.")
            return
        
        self.running = True
        logger.info("Starting main application loop")
        print("\nFace Detection Application Started")
        print("Controls:")
        print("  'q' - Quit")
        print("  's' - Save detected faces")
        print("  'c' - Chat with AIML bot")
        print("=" * 50)
        
        try:
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    logger.warning("Failed to read frame from webcam")
                    break
                
                self.frame_count += 1
                frame, faces = self.process_frame(frame)
                
                # Display frame
                cv2.imshow("Face Detection with AIML", frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key != 255:
                    self.running = self.handle_keyboard_input(key, frame, faces)
        
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up resources...")
        
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        
        logger.info(f"Application closed. Total frames: {self.frame_count}, Total faces: {self.total_faces_detected}")
        print("\nApplication closed successfully")


def main():
    """Entry point for the application."""
    app = FaceDetectionApp()
    app.run()


if __name__ == "__main__":
    main()
