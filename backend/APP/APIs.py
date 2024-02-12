from flask import jsonify
from flask_restful import Resource

class Data(Resource):

    def get(self):
        return {'message': 'test from Flask'}

    # def get(self,user_id):
    #     if user_id is None:
    #         return jsonify({"users": ["user1", "user2"]})
    #     else:
    #         return jsonify({"user": "user1"})

    # def post(self):
    #     user_data = request.json
    #     return jsonify(user_data), 201

    # def put(self, user_id):
    #     user_data = request.json
    #     return jsonify(user_data)

    # def delete(self, user_id):
    #     return jsonify({"message": "User deleted"}), 204
