from mallow import ma
from models.tasks import TasksModel
from models.users import UserModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TasksModel
        load_instance = True
        load_only = ("user","id")
        dump_only = ("user_id",)
        include_fk = True