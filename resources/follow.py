from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request
import mysql.connector
from mysql.connector import Error

from resources.mysql_connection import get_connection



class FollowResource(Resource):

    # 친구 맺기
    @jwt_required()
    def post(self, followee_id):

        user_id = get_jwt_identity()

        try:
            connection = get_connection()
            query = '''insert into follow
                    (followerId, followeeId)
                    values
                    (%s,%s);'''
            record = (user_id,followee_id)
            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()
            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            return {'result' : 'fail', 'error' : str(e)}, 500


        return {'result' : 'success'}
    
    # 친구 끊기
    @jwt_required()
    def delete(self, followee_id):

        user_id = get_jwt_identity()

        try:
            connection = get_connection()
            query = '''delete from follow
                        where followerId = %s and followeeId = %s;'''
            record = (user_id,followee_id)
            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()
            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            return {'result' : 'fail', 'error' : str(e)}, 500
            
        return {'result' : 'success'}
    



    







