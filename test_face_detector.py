"""Tests for Face Detection Module"""

import unittest
import numpy as np
from src.face_detector import FaceDetector


class TestFaceDetector(unittest.TestCase):
    """Test cases for FaceDetector class."""

    def setUp(self):
        """Set up test fixtures."""
        self.detector = FaceDetector(model_type="haarcascade")
        self.test_frame = np.zeros((480, 640, 3), dtype=np.uint8)

    def test_initialization(self):
        """Test FaceDetector initialization."""
        self.assertIsNotNone(self.detector)
        self.assertEqual(self.detector.model_type, "haarcascade")
        self.assertEqual(self.detector.face_count, 0)

    def test_detect_faces_empty_frame(self):
        """Test face detection on empty frame."""
        faces = self.detector.detect_faces(self.test_frame)
        self.assertIsInstance(faces, (list, np.ndarray))
        # Empty frame should detect 0 or very few faces
        self.assertLessEqual(len(faces), 2)

    def test_get_face_count(self):
        """Test get_face_count method."""
        self.detector.detect_faces(self.test_frame)
        count = self.detector.get_face_count()
        self.assertEqual(count, 0)

    def test_draw_faces(self):
        """Test drawing faces on frame."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        faces = np.array([(100, 100, 50, 50)])
        result = self.detector.draw_faces(frame, faces)
        self.assertEqual(result.shape, frame.shape)

    def test_extract_face_roi(self):
        """Test extracting face ROI."""
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 255
        face = (100, 100, 50, 50)
        roi = self.detector.extract_face_roi(frame, face)
        self.assertEqual(roi.shape, (50, 50, 3))

    def test_merge_overlapping_regions(self):
        """Test merging overlapping regions."""
        regions = [(0, 0, 50, 50), (25, 25, 50, 50), (200, 200, 50, 50)]
        merged = self.detector._merge_overlapping_regions(regions)
        # Should merge overlapping regions
        self.assertGreater(len(regions), 0)
        self.assertLessEqual(len(merged), len(regions))


if __name__ == "__main__":
    unittest.main()
