from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    sensitive_data = db.Column(db.Text, nullable=False)
    scan_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Scan {self.filename}>"
