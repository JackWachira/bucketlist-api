class BaseConfig(object):
    """Holds default configuration options."""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bucketlist.db'


class DevelopmentConfig(BaseConfig):
    """Development configuration options."""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bucketlist.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BaseConfig):
    """Test configuration options."""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///memory'


class ProductionConfig(BaseConfig):
    """Production configuration options."""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bucketlist.db'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
