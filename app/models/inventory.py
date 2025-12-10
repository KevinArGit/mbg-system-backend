from app import db

class Inventory(db.Model):
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True)
    
    # Polymorphic location fields
    location_type = db.Column(db.String(50), nullable=False)  # e.g., 'warehouse', 'kitchen', 'school'
    location_id = db.Column(db.Integer, nullable=False)

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)

    item = db.relationship('Item', backref=db.backref('inventories', lazy=True))

    __table_args__ = (
        db.Index('ix_inventory_location', 'location_type', 'location_id'),
    )

    def __repr__(self):
        return f'<Inventory for item {self.item_id} in {self.location_type}:{self.location_id}: {self.quantity}>'