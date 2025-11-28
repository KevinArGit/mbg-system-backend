from app import db

class Menu(db.Model):
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.String(256))

    def __repr__(self):
        return f'<Menu {self.name}>'