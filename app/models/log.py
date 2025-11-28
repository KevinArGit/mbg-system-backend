from app import db
import datetime

class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    log_type = db.Column(db.String(64), nullable=False)  # e.g., 'inventory_change', 'delivery', 'waste'
    details = db.Column(db.String(256))
    
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    kitchen_id = db.Column(db.Integer, db.ForeignKey('kitchens.id'))
    
    previous_quantity = db.Column(db.Integer)
    current_quantity = db.Column(db.Integer)

    item = db.relationship('Item', backref=db.backref('logs', lazy=True))
    warehouse = db.relationship('Warehouse', backref=db.backref('logs', lazy=True))
    kitchen = db.relationship('Kitchen', backref=db.backref('logs', lazy=True))

    def __repr__(self):
        return f'<Log {self.log_type} for item {self.item_id} @ {self.timestamp}>'