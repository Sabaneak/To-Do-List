from flask_restful import Resource
from flask import request
from models.tasks import TasksModel
from schemas.tasks import TaskSchema
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity

task_schema = TaskSchema()
task_list_schema = TaskSchema(many=True)

class Input_Tasks(Resource):

    @classmethod
    @jwt_required
    def post(cls):
        task = task_schema.load(request.get_json())
        ID = get_jwt_identity()
        task.user_id = ID
        
        if TasksModel.find_by_name(task.name):
            return {'msg': "Task already exists"}
        
        try:
            task.save_to_data()
        except:
            return {'msg': "Task was not saved"}, 500

        return {'msg': "Task was added to database"}

class Tasks(Resource):

    @classmethod
    @jwt_required
    def get(cls, name):
        task = TasksModel.find_by_name(name)
        
        if task:
            return task_schema.dump(task), 200

        return {'msg': "No such task exists"}, 404

    @classmethod
    @jwt_required
    def put(cls, name):
        task = TasksModel.find_by_name(name)
        given_task = request.get_json()
        
        if not task:
            return {'msg': "No such task exists"}
        
        task.category = given_task["category"]
        task.status = given_task["status"]

        try:
            task.save_to_data()
        except:
            return {'msg': "Task was not saved"}, 500

        return {'msg': "Task has been modified"}, 200

    @classmethod
    @fresh_jwt_required
    def delete(cls, name):
        task = TasksModel.find_by_name(name)
        
        if task:
            task.delete_from_data()
            return {'msg': "Task has been deleted"}, 200

        return {'msg': "No such task exists"}, 404

class TasksList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        return {'Tasks': task_list_schema.dump(TasksModel.find_all())}, 200

        
