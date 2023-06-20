from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request
import mysql.connector
from mysql.connector import Error

from resources.mysql_connection import get_connection


class MemoResource(Resource):

    @jwt_required()
    def put(self, memo_id):

        data = request.get_json()

        userId = get_jwt_identity()

        try:
            connection = get_connection()
            query = '''update memo
                    set title = %s, date = %s, content =%s
                    where userId = %s and id = %s;'''
            record = (data['title'], data['date'], data['content'],
                      userId, memo_id)
            
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            return {'result' : 'fail', 'error' : str(e)}, 500

        return {'result' : 'success'}
    

    @jwt_required()
    def delete(self, memo_id):

        user_id = get_jwt_identity()

        try:
            connection = get_connection()
            query = '''delete from memo
                    where id = %s and userId = %s;'''
            record = (memo_id, user_id)
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            return {'result' : 'fail', 'error' : str(e)}, 500

        return {'result' : 'success'}


class MemoListResource(Resource):
    
    @jwt_required()
    def post(self) :

        data = request.get_json()

        user_id = get_jwt_identity()

        try:
            connection = get_connection()
            query = '''insert into memo
                    (title, date,content, userId)
                    values
                    (%s,%s,%s,%s);'''
            record = (data['title'],data['date'], data['content'], user_id)

            cousor = connection.cursor()
            cousor.execute(query, record)
            connection.commit()

            cousor.close()
            connection.close()

        except Error as e:
            print(e)
            return {'result' : 'fail', 'error' : str(e)}, 500

        return {'result' : 'success'}

    @jwt_required()
    def get(self) :
        
        user_id = get_jwt_identity()

        try:
            connection = get_connection()
            query = '''select*
                    from memo
                    where userId = %s
                    order by date desc;'''
            record = (user_id,)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query,record)
            
            result_list = cursor.fetchall()

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            return {'result' : 'fail', 'error':str(e)}, 500
        
        i = 0
        for row in result_list :
            result_list[i]['createdAt'] = row['createdAt'].isoformat()
            result_list[i]['updatedAt'] = row['updatedAt'].isoformat()
            result_list[i]['date'] = row['date'].isoformat()
            i = i + 1

        return {'result' : 'success',
                'count' : len(result_list),
                'items' : result_list}







