from app import db
import datetime

class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    log_type = db.Column(db.String(64), nullable=False, index=True)  # e.g., 'dispatch_from_warehouse', 'receipt_at_kitchen'
    
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), index=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=True)
    kitchen_id = db.Column(db.Integer, db.ForeignKey('kitchens.id'), nullable=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=True)
    
    previous_quantity = db.Column(db.Integer)
    current_quantity = db.Column(db.Integer)

    # --- New Fields ---
    # status: Tracks the verification state of the log entry.
    # 'pending': The default state. Needs to be checked.
    # 'verified': The log has been successfully matched and is considered correct.
    # 'mismatch': The log is part of a transaction that has a discrepancy.
    status = db.Column(db.String(64), nullable=False, default='pending', index=True)

    # parent_log_id: Links a receipt log back to its original dispatch log.
    # This creates a clear, auditable chain of custody.
    parent_log_id = db.Column(db.Integer, db.ForeignKey('logs.id'), nullable=True)
    # --------------------

    def __repr__(self):
        return f'<Log {self.log_type} for item {self.item_id} @ {self.timestamp}>'
