from .user_routes import user_bp
from .category_routes import category_bp
from .location_routes import location_bp

def register_blueprints(app):

    blueprints = [
        user_bp,
        category_bp,
        location_bp
    ]

    for bp in blueprints:
        app.register_blueprint(bp)