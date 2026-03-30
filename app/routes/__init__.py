import pkgutil
import importlib

def register_blueprints(app):
    package = __name__

    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"{package}.{module_name}")

        # Procura por variáveis que terminam com _bp
        for attr in dir(module):
            if attr.endswith("_bp"):
                app.register_blueprint(getattr(module, attr))