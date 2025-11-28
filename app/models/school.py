from app import db

class School(db.Model):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.String(256))
    address = db.Column(db.String(256))
    kitchen_id = db.Column(db.Integer, db.ForeignKey('kitchens.id'))

    def __repr__(self):
        return f'<School {self.name}>'