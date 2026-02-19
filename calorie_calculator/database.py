# database.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Профиль пользователя
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    gender = db.Column(db.String(10))
    activity_level = db.Column(db.String(20))
    goal = db.Column(db.String(20))

    # Статистика
    total_calculations = db.Column(db.Integer, default=0)
    achievements = db.Column(db.Text, default='[]')  # JSON с достижениями

    # Связь с историей расчетов
    calculations = db.relationship('CalculationHistory', backref='user', lazy=True)


class CalculationHistory(db.Model):
    __tablename__ = 'calculation_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # Входные данные
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    activity_level = db.Column(db.String(20))
    goal = db.Column(db.String(20))

    # Результаты
    bmr = db.Column(db.Float)
    maintenance = db.Column(db.Float)
    recommended_calories = db.Column(db.Float)
    protein = db.Column(db.Float)
    fats = db.Column(db.Float)
    carbs = db.Column(db.Float)

    # Заметки пользователя
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.strftime('%Y-%m-%d %H:%M'),
            'weight': self.weight,
            'height': self.height,
            'goal': self.goal,
            'recommended_calories': self.recommended_calories,
            'protein': self.protein,
            'fats': self.fats,
            'carbs': self.carbs,
            'notes': self.notes
        }


class Achievement(db.Model):
    __tablename__ = 'achievements'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    icon = db.Column(db.String(50))
    condition = db.Column(db.String(100))  # Условие получения
    points = db.Column(db.Integer, default=10)


class UserProgress(db.Model):
    __tablename__ = 'user_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    weight = db.Column(db.Float)
    calories_consumed = db.Column(db.Float)
    protein_consumed = db.Column(db.Float)
    fats_consumed = db.Column(db.Float)
    carbs_consumed = db.Column(db.Float)
    water_consumed = db.Column(db.Float)  # в литрах
    steps = db.Column(db.Integer)  # количество шагов
    mood = db.Column(db.Integer)  # настроение от 1 до 5
    notes = db.Column(db.Text)