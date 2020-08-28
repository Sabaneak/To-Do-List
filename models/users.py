from flask import request, url_for
from requests import Response

from libs.mailgun import MailGun
from db import data

class UserModel(data.Model):
    __tablename__ = "Users"

    id = data.Column(data.Integer, primary_key=True)
    username = data.Column(data.String(50), nullable=False, unique=True)
    password = data.Column(data.String(50), nullable=False)
    email = data.Column(data.String(80), nullable=False, unique=True)
    activated = data.Column(data.Boolean, default=False)

    tasks = data.relationship("TasksModel", lazy="dynamic")

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @classmethod
    def find_by_id(cls, ID):
        return cls.query.filter_by(id = ID).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email = email).first()
    
    def send_confirmation_email(self) -> Response:
        link = request.url_root[:-1] + url_for("userconfirm", user_id=self.id)
        subject = "Registration complete"
        text = "Click on the link to confirm your registration: {link}"
        html = f'<html>Click the link to confirm your registration: <a href="{link}">{link}</a></html>'
        return MailGun.send_email([self.email], subject, text, html)
    
    def save_to_data(self):
        data.session.add(self)
        data.session.commit()

    def delete_from_data(self):
        data.session.delete(self)
        data.session.commit()