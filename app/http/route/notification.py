from flask import Blueprint

from core.decorators import *
from app.http.controllers.notification import NotificationController

notification_bp = Blueprint('notification', __name__, url_prefix='/api/v1/notifications')
controller = NotificationController()

notification_bp.add_url_rule(
    '/', 'create_notification',
    view_func=timed(handle_exceptions(sync_transactional(controller.create_notification))),
    methods=['POST']
)