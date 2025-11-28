from app import db

class Inventory(db.Model):
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)

    warehouse = db.relationship('Warehouse', backref=db.backref('inventory_items', lazy=True))
    item = db.relationship('Item', backref=db.backref('inventories', lazy=True))

    def __repr__(self):
        return f'<Inventory {self.item.name} in {self.warehouse.name}: {self.quantity}>'