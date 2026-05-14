from flask import Blueprint

notification_bp = Blueprint('notification', __name__, url_prefix='/notifications')

@notification_bp.route('/', methods=['GET'])
def get_notifications():
    return {"message": "Notifications list"}, 200

@notification_bp.route('/<int:notification_id>', methods=['GET'])
def get_notification(notification_id):
    return {"message": f"Notification {notification_id}"}, 200