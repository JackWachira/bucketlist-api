from flask import request
from flask_restful import Resource, Api
from models.bucket_models import app, BucketLists, BucketListsSchema


api = Api(app)

schema = BucketListsSchema()


class BucketList(Resource):

    def get(self):

        bucket_list_query = BucketLists.query.all()
        # Serialize the query results in the JSON API format
        results = schema.dump(bucket_list_query, many=True).data
        return results

    def post(self):
        raw_dict = request.get_json(force=True)

        return raw_dict


api.add_resource(BucketList, '/v1/bucketlists/')
