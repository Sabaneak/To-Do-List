from mallow import ma
from models.users import UserModel
from models.tasks import TasksModel
from schemas.tasks import TaskSchema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

class UserSchema(ma.SQLAlchemyAutoSchema):
    tasks = ma.Nested(TaskSchema, many=True)
    
    class Meta:
        model = UserModel
        load_instance = True
        load_only = ("password",)
        dump_only = ("id",)
