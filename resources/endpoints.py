from flask import request, jsonify
from flask_restful import Resource, Api, abort
from models.bucket_models import app, BucketLists, BucketListsSchema, db
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

api = Api(app, prefix="/api/v1/")

schema = BucketListsSchema()


class BucketList(Resource):

    def get(self):

        bucket_list_query = BucketLists.query.all()
        # Serialize the query results in the JSON API format
        results = schema.dump(bucket_list_query, many=True).data
        return results

    def post(self):
        raw_dict = request.get_json(force=True)
        try:
           # Validate the data or raise a Validation error if
           # incorrect
            schema.validate(raw_dict)
            # Create a User object with the API data recieved
            bucketlist = BucketLists(
                raw_dict['name'], raw_dict['created_by'])
            # Commit data
            bucketlist.add(bucketlist)
            query = BucketLists.query.get(bucketlist.id)
            results = schema.dump(query).data
            return results, 201

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp

    def put(self, bucket_id=0):
        if bucket_id != 0:
            bucketlist = BucketLists.query.get_or_404(bucket_id)
            raw_dict = request.get_json(force=True)
            try:
                schema.validate(raw_dict)
                for key, value in raw_dict.items():
                    setattr(bucketlist, key, value)
                bucketlist.update()
                return schema.dump(bucketlist).data, 201
            except ValidationError as err:
                resp = jsonify({"error": err.messages})
                resp.status_code = 401
                return resp
            except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp
        else:
            resp = jsonify({"error": "Bucket id missing"})
            resp.status_code = 401
            return resp


api.add_resource(BucketList, 'bucketlists/', 'bucketlists/<bucket_id>')
