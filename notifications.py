def get_notifications(user_id):
    # Simulated fake notification data
    notifications = [
        {"id": 1, "message": "Welcome!", "read": True},
        {"id": 2, "message": "Your order shipped", "read": False},
        {"id": 3, "message": "Package delivered", "read": False},
    ]
    return notifications

def count_unread(notifications):
    return sum(1 for n in notifications if not n["read"])
