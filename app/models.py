from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from app import db
class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_type = db.Column(db.String(100))
    card_number = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # UTC timestamp

    def __repr__(self):
        return f'<ScanResult {self.card_type} - {self.card_number}>'
