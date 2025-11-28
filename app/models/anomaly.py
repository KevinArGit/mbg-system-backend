from app import db
import datetime

class Anomaly(db.Model):
    __tablename__ = 'anomalies'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    anomaly_type = db.Column(db.String(64), nullable=False)  # e.g., 'unsynchronized', 'mismatch', 'no_delivery'
    severity = db.Column(db.String(64), nullable=False)  # e.g., 'warning', 'critical'
    log_id = db.Column(db.Integer, db.ForeignKey('logs.id'))
    
    expected_quantity = db.Column(db.Integer)
    actual_quantity = db.Column(db.Integer)

    log = db.relationship('Log', backref=db.backref('anomalies', lazy=True))

    def __repr__(self):
        return f'<Anomaly {self.anomaly_type} ({self.severity}) @ {self.timestamp}>'