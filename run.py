"""Import statements."""
from app import create_app
from config.config import DevelopmentConfig

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    # run the flask app
    app.run()
