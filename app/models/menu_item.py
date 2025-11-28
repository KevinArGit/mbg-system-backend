from app import db

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    menu = db.relationship('Menu', backref=db.backref('menu_items', lazy=True, cascade="all, delete-orphan"))
    item = db.relationship('Item', backref=db.backref('menu_items', lazy=True))

    def __repr__(self):
        return f'<MenuItem {self.item.name} in {self.menu.name}>'