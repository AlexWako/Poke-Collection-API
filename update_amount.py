from models import CollectionModel, SetCollectionModel, CardModel, db

def update_set_card_amount(poke_id):
    total_amount = db.session.query(db.func.sum(CardModel.amount)).filter_by(poke_id=poke_id).scalar() or 0
    set_card = SetCollectionModel.query.get(poke_id)
    if set_card:
        set_card.amount = total_amount
    db.session.commit()

def update_collection_amount(set_id):
    total_amount = db.session.query(db.func.sum(SetCollectionModel.amount)).filter_by(set_id=set_id).scalar() or 0
    collection = CollectionModel.query.get(set_id)
    if collection:
        collection.amount = total_amount
    db.session.commit()
