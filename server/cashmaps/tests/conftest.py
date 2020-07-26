from cashmaps import create_app
import pytest

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        return app
