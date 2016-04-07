"""Import statements."""
from models.bucket_models import migrate_manager

if __name__ == '__main__':
    # run the flask app
    migrate_manager.run()
