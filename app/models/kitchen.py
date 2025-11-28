from app import db

class Kitchen(db.Model):
    __tablename__ = 'kitchens'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.String(256))
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    schools = db.relationship('School', backref='kitchen', lazy=True)

    def __repr__(self):
        return f'<Kitchen {self.name}>'