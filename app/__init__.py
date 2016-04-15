from flask import Flask, Response
from models.models import db


class MyResponse(Response):
    default_mimetype = 'application/xml'


def create_app(configuration):
    app = Flask(__name__)
    app.config.from_object(configuration)
    app.response_class = MyResponse

    db.init_app(app)

    # Blueprints
    from app.resources.resources import bucket_list
    app.register_blueprint(bucket_list, url_prefix='/api/v1')

    return app
