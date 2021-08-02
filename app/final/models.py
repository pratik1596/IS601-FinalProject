from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Team(db.Model):

    __tablename__ = 'mlb_teams'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    Team = db.Column(
        db.String(12),
        index=False,
        unique=False,
        nullable=False
    )
    Payroll_millions = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=False
    )
    Wins = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return '<Team {}>'.format(self.Team)



class User(UserMixin, db.Model):

    __tablename__ = 'users-login'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    email = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
	)
    website = db.Column(
        db.String(60),
        index=False,
        unique=False,
        nullable=True
	)
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    def set_password(self, password):
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)