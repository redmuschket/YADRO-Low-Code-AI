from .database import register_database_middleware
from .dependencies import register_dependencies_middleware

def register_all_middleware(app):
    register_database_middleware(app)
    register_dependencies_middleware(app)