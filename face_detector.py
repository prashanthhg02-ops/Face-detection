"""
Face Detection Module
Handles real-time face detection from video streams
"""

import cv2
import numpy as np
import logging
from typing import List, Tuple
from .config import FACE_DETECTION_CONFIG, DISPLAY_CONFIG

logger = logging.getLogger(__name__)


class FaceDetector:
    """
    Face detection using OpenCV and pre-trained models.
    Supports multiple detection methods: Haar Cascade, DNN, and Dlib.
    """

    def __init__(self, model_type: str = "haarcascade"):
        """
        Initialize the face detector.
        
        Args:
            model_type: Type of model to use ('haarcascade', 'dnn', or 'dlib')
        """
        self.model_type = model_type
        self.detector = None
        self.face_count = 0
        self.detection_confidence = FACE_DETECTION_CONFIG["confidence_threshold"]
        self.use_cascade = False
        
        try:
            self.detector = self._load_model()
            if self.detector is not None:
                self.use_cascade = True
        except Exception as e:
            logger.warning(f"Could not load cascade classifier: {e}. Using fallback face detection.")
            self.detector = None
        
        logger.info(f"Face detector initialized with model: {model_type}")

    def _load_model(self):
        """Load the face detection model based on model_type."""
        try:
            if self.model_type == "haarcascade":
                cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
                # Try to load cascade classifier if available
                if hasattr(cv2, 'CascadeClassifier'):
                    classifier = cv2.CascadeClassifier(cascade_path)
                    if not classifier.empty():
                        return classifier
                logger.info("Cascade classifier not available, will use edge-based detection")
                return None
            else:
                logger.warning(f"Model type '{self.model_type}' not fully implemented.")
                return None
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return None

    def detect_faces(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in a given frame.
        
        Args:
            frame: Input image frame (BGR format)
            
        Returns:
            List of bounding boxes as (x, y, w, h)
        """
        try:
            if self.detector is None or not self.use_cascade:
                # Fallback: use Canny edge detection for face-like regions
                return self._detect_faces_fallback(frame)
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            faces = self.detector.detectMultiScale(
                gray,
                scaleFactor=FACE_DETECTION_CONFIG["scale_factor"],
                minNeighbors=FACE_DETECTION_CONFIG["min_neighbors"],
                minSize=FACE_DETECTION_CONFIG["min_face_size"],
                maxSize=FACE_DETECTION_CONFIG["max_face_size"],
            )
            
            self.face_count = len(faces)
            return faces
        except Exception as e:
            logger.error(f"Error detecting faces: {e}")
            return []

    def _detect_faces_fallback(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Fallback face detection using edge detection.
        
        Args:
            frame: Input image frame
            
        Returns:
            List of detected face regions (simplified)
        """
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Apply edge detection
            edges = cv2.Canny(gray, 100, 200)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            faces = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                # Filter by size to approximate face regions
                if (w > 30 and h > 30 and 
                    w < 500 and h < 500 and 
                    0.5 < w/h < 2.0):  # Aspect ratio close to 1
                    faces.append((x, y, w, h))
            
            # Remove duplicates by merging overlapping regions
            faces = self._merge_overlapping_regions(faces)
            self.face_count = len(faces)
            return faces
        except Exception as e:
            logger.error(f"Error in fallback detection: {e}")
            return []

    def _merge_overlapping_regions(self, regions: List[Tuple[int, int, int, int]]) -> List[Tuple[int, int, int, int]]:
        """
        Merge overlapping regions to reduce duplicates.
        
        Args:
            regions: List of regions (x, y, w, h)
            
        Returns:
            Merged list of regions
        """
        if not regions:
            return []
        
        # Sort by area (largest first)
        regions = sorted(regions, key=lambda r: r[2] * r[3], reverse=True)
        
        merged = []
        used = set()
        
        for i, (x1, y1, w1, h1) in enumerate(regions):
            if i in used:
                continue
            
            for j, (x2, y2, w2, h2) in enumerate(regions[i+1:], i+1):
                if j in used:
                    continue
                
                # Check for overlap
                if not (x1 + w1 < x2 or x2 + w2 < x1 or 
                        y1 + h1 < y2 or y2 + h2 < y1):
                    used.add(j)
            
            merged.append((x1, y1, w1, h1))
        
        return merged

    def draw_faces(self, frame: np.ndarray, faces: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """
        Draw bounding boxes around detected faces.
        
        Args:
            frame: Input image frame
            faces: List of detected face bounding boxes
            
        Returns:
            Frame with drawn bounding boxes
        """
        for (x, y, w, h) in faces:
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                DISPLAY_CONFIG["box_color"],
                DISPLAY_CONFIG["line_thickness"],
            )
            
            # Draw confidence or face ID
            label = f"Face #{len(faces)}"
            cv2.putText(
                frame,
                label,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                DISPLAY_CONFIG["font_scale"],
                DISPLAY_CONFIG["text_color"],
                DISPLAY_CONFIG["line_thickness"],
            )
        
        return frame

    def get_face_count(self) -> int:
        """Get the number of detected faces from the last detection."""
        return self.face_count

    def extract_face_roi(self, frame: np.ndarray, face: Tuple[int, int, int, int]) -> np.ndarray:
        """
        Extract Region of Interest (ROI) for a detected face.
        
        Args:
            frame: Input image frame
            face: Bounding box as (x, y, w, h)
            
        Returns:
            Extracted face ROI
        """
        x, y, w, h = face
        roi = frame[y : y + h, x : x + w]
        return roi

    def save_face(self, frame: np.ndarray, face: Tuple[int, int, int, int], filename: str) -> bool:
        """
        Save a detected face ROI to file.
        
        Args:
            frame: Input image frame
            face: Bounding box as (x, y, w, h)
            filename: Output filename
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            roi = self.extract_face_roi(frame, face)
            success = cv2.imwrite(filename, roi)
            if success:
                logger.info(f"Face saved to {filename}")
            return success
        except Exception as e:
            logger.error(f"Error saving face: {e}")
            return False
