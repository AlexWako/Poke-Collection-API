from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CollectionModel(db.Model):
    __tablename__ = "collection"
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String, unique = True, nullable = False)
    generation = db.Column(db.Integer, nullable = False)
    amount = db.Column(db.Integer, nullable = False)

    sets = db.relationship('SetCollectionModel', back_populates = 'collection', cascade = "all, delete-orphan")

    def __repr__(self):
        return f"Collection(id = {self.id}, name = {self.name}, amount = {self.amount})"

class SetCollectionModel(db.Model):
    __tablename__ = "setcollection"
    set_id = db.Column(db.String, db.ForeignKey("collection.id"), nullable = False)
    poke_id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String, nullable = True)
    number = db.Column(db.Integer, nullable = False)
    amount = db.Column(db.Integer, nullable = False)

    collection = db.relationship('CollectionModel', back_populates = 'sets')
    card = db.relationship('CardModel', back_populates = 'set_collection', cascade = "all, delete-orphan")


    def __repr__(self):
        return f"SetCollection(set_id = {self.set_id}, poke_id = {self.poke_id}, number = {self.number}, amount = {self.amount})"

class CardModel(db.Model):
    __tablename__ = "card"
    poke_id_variant = db.Column(db.String, primary_key = True)
    poke_id = db.Column(db.String, db.ForeignKey("setcollection.poke_id"), nullable = False)
    poke_name = db.Column(db.String, nullable = True)
    number = db.Column(db.Integer, nullable = False)
    rarity = db.Column(db.String, nullable = True)
    variant = db.Column(db.Boolean, nullable = False)
    variant_name = db.Column(db.String, nullable = False)
    amount = db.Column(db.Integer, nullable = False)

    set_collection = db.relationship("SetCollectionModel", back_populates = "card")

    def __repr__(self):
       return f"Card(poke_id_variant = {self.poke_id_variant}, poke_id = {self.poke_id}, poke_name = {self.poke_name}, number = {self.number}, rarity = {self.rarity}, variant = {self.variant}, variant_name = {self.variant_name}, amount = {self.amount})"
