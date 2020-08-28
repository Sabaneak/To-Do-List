from db import data
from flask_jwt_extended import get_jwt_identity

class TasksModel(data.Model):
    __tablename__ = "Tasks"

    id = data.Column(data.Integer, primary_key=True)
    name = data.Column(data.String(100), nullable=False, unique=True)
    category = data.Column(data.String(30), nullable=False)
    status = data.Column(data.String(30), nullable=False)

    user_id = data.Column(data.Integer, data.ForeignKey("Users.id"), nullable=False)
    user = data.relationship("UserModel")
    
    @classmethod
    def find_by_name(cls, name):
        ID = get_jwt_identity()
        return cls.query.filter_by(name=name, user_id=ID).first()

    @classmethod
    def find_by_id(cls, _id):
        ID = get_jwt_identity()
        return cls.query.filter_by(id=_id, user_id=ID).first()
    
    @classmethod
    def find_all(cls):
        ID = get_jwt_identity()
        return cls.query.filter_by(user_id=ID).all()

    def save_to_data(self) -> None:
        data.session.add(self)
        data.session.commit()

    def delete_from_data(self) -> None:
        data.session.delete(self)
        data.session.commit()