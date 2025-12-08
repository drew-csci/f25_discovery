import unittest
from notifications import get_notifications, count_unread

class TestNotifications(unittest.TestCase):

    def test_get_notifications_returns_list(self):
        result = get_notifications(user_id=1)
        self.assertIsInstance(result, list)

    def test_notifications_items_are_dicts(self):
        notifications = get_notifications(user_id=1)
        self.assertTrue(all(isinstance(n, dict) for n in notifications))

    def test_count_unread_returns_correct_number(self):
        notifications = [
            {"message": "A", "read": True},
            {"message": "B", "read": False},
            {"message": "C", "read": False},
        ]
        result = count_unread(notifications)
        self.assertEqual(result, 2)

if __name__ == "__main__":
    unittest.main()

