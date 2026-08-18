"""Tests for AIML Chatbot Module"""

import unittest
from src.aiml_chatbot import AIMLChatbot


class TestAIMLChatbot(unittest.TestCase):
    """Test cases for AIMLChatbot class."""

    def setUp(self):
        """Set up test fixtures."""
        self.chatbot = AIMLChatbot("./data/aiml")

    def test_initialization(self):
        """Test AIMLChatbot initialization."""
        self.assertIsNotNone(self.chatbot)
        self.assertEqual(self.chatbot.face_count, 0)

    def test_respond(self):
        """Test chatbot response generation."""
        response = self.chatbot.respond("hello")
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_update_face_info(self):
        """Test updating face information."""
        self.chatbot.update_face_info(3, "test detection")
        self.assertEqual(self.chatbot.face_count, 3)
        self.assertEqual(self.chatbot.last_detection_info, "test detection")

    def test_get_detection_status_no_faces(self):
        """Test detection status with no faces."""
        self.chatbot.update_face_info(0)
        status = self.chatbot.get_detection_status()
        self.assertIn("No faces", status)

    def test_get_detection_status_one_face(self):
        """Test detection status with one face."""
        self.chatbot.update_face_info(1)
        status = self.chatbot.get_detection_status()
        self.assertIn("1 face", status)

    def test_get_detection_status_multiple_faces(self):
        """Test detection status with multiple faces."""
        self.chatbot.update_face_info(5)
        status = self.chatbot.get_detection_status()
        self.assertIn("5 faces", status)


if __name__ == "__main__":
    unittest.main()
