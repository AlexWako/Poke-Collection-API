from flask import Blueprint, request
from flask.json import jsonify
from flask_restful import fields, marshal, Resource
import json
from app_resource.sets import sets
from app_resource.update_amount import update_set_card_amount, update_collection_amount
from models import CollectionModel, SetCollectionModel, CardModel, db

collection = Blueprint("collection", __name__, url_prefix = "/api/v1/collection")

# Fields (return template in JSON format)
collection_fields = {
    'id': fields.String,
    'name': fields.String,
    'generation': fields.Integer,
    'amount': fields.Integer
}

set_collection_fields = {
    'set_id': fields.String,
    'poke_id': fields.String,
    'name': fields.String,
    'number': fields.Integer,
    'amount': fields.Integer
}

card_fields = {
    'poke_id': fields.String,
    'poke_name': fields.String,
    'number': fields.Integer,
    'rarity': fields.String,
    'variant': fields.Boolean,
    'variant_name': fields.String,
    'amount': fields.Integer
}

# Get Collection
@collection.get('/')
def get_collection():
    collection = CollectionModel.query.all()
    if not collection:
        return jsonify({'error': 'Collection not found'}), 404
    return marshal(collection, collection_fields), 200

# Get Set Collection
@collection.get('/<string:set_id>')
def get_set_collection(set_id):
    set_collection = SetCollectionModel.query.filter_by(set_id = set_id).all()
    if not set_collection:
        return jsonify({'error': 'Set collection not found'}), 404
    return marshal(set_collection, set_collection_fields), 200

# Post Set
@collection.post('/')
def add_set_collection():
    set_id = request.get_json().get('set_id')

    set_exist = CollectionModel.query.get(set_id)
    if set_exist:
        return jsonify({'error': 'Set already exists'}), 409
    
    set_data = next((set for set in sets if set['id'] == set_id), None)
    if not set_data:
        return jsonify({'error': 'Set not acceptable'}), 406
        
    set_collection = CollectionModel(id = set_id, name = set_data['name'], generation = set_data['generation'], amount = 0)
    
    db.session.add(set_collection)
    db.session.commit()
    return marshal(set_collection, collection_fields), 201

# Delete Set
@collection.delete('/<string:set_id>')
def delete_set_collection(set_id):
    set = CollectionModel.query.get(set_id)
    if not set:
        return jsonify({'error': 'Set not found'}), 404
    db.session.delete(set)
    db.session.commit()
    return jsonify({}), 204

# Get Generation Collection
@collection.get('/gen/<int:generation>')
def get_generation_collection(generation):
    result = CollectionModel.query.filter_by(generation = generation).all()
    if not result:
        return jsonify({'error': 'Set from that generation not found'}), 404
    return marshal(result, collection_fields), 200

# Get Name Collection
@collection.get('/name/<string:name>')
def get_name_card(name):
    cards = SetCollectionModel.query.filter_by(name = name).all()
    if not cards:
        return jsonify({'error': 'Name not found'}), 404
    return marshal(cards, set_collection_fields), 200

# Get Set Collection Card
@collection.get('/<string:set_id>/<int:number>')
def get_set_card(set_id, number):
    result = SetCollectionModel.query.get(set_id+str(number))
    if not result:
        return jsonify({'error': 'Set not found'}), 404
    return marshal(result, set_collection_fields), 200

# Post Set Collection
@collection.post('/<string:set_id>')
def add_set_card(set_id):
    set_exist = CollectionModel.query.get(set_id)
    if not set_exist:
        return jsonify({'error': 'Set not found'}), 404

    name = request.get_json().get('name')
    number = request.get_json().get('number')
    amount = request.get_json().get('amount', 0)
    if not number:
        return jsonify({'error': 'Missing required fields: number'}), 400

    card_exist = SetCollectionModel.query.get(set_id+str(number))
    if card_exist:
        return jsonify({"error": "Card already Exist"}), 409

    set_card = SetCollectionModel(set_id = set_id, poke_id = set_id+str(number), name = name, number = number, amount = amount)
    db.session.add(set_card)
    db.session.commit()
    update_collection_amount(set_id)
    return marshal(set_card, set_collection_fields), 201

@collection.put('/<string:set_id>/<int:number>')
@collection.patch('/<string:set_id>/<int:number>')
def patch_set_card(set_id, number):
    set_card = SetCollectionModel.query.get(set_id+str(number))
    if set_card is None:
        return jsonify({'error': 'Card not found'}), 404

    name = request.get_json().get('name')
    amount = request.get_json().get('amount', 0)

    set_card.name = name
    set_card.amount = amount

    db.session.commit()
    update_collection_amount(set_id)
    return marshal(SetCollectionModel.query.get(set_id+str(number)), set_collection_fields), 200

@collection.delete('/<string:set_id>/<int:number>')
def delete_set_card(set_id, number):
    set_card = SetCollectionModel.query.get(set_id+str(number))
    if not set_card:
        return jsonify({'error': 'Card not found'}), 404
    db.session.delete(set_card)
    db.session.commit()
    update_collection_amount(set_id)
    return jsonify({}), 204

# Get Card
@collection.get('/<string:set_id>/<int:number>/<int:variant>/<string:variant_name>')
def get_card(set_id, number, variant, variant_name):
    result = CardModel.query.get(set_id+str(number)+str(variant)+variant_name)
    if not result:
        print(result)
        return jsonify({'error': 'Card not found'}), 404
    return marshal(result, card_fields), 200

# Post Card
@collection.post('/<string:set_id>/<int:number>')
def add_card(set_id, number):
    set_exist = CollectionModel.query.get(set_id)
    if not set_exist:
        return jsonify({'error': 'Set not found'}), 404

    name = request.get_json().get('name')
    rarity = request.get_json().get('rarity')
    variant = request.get_json().get('variant')
    variant_name = request.get_json().get('variant_name')
    amount = request.get_json().get('amount', 0)
    if not variant or not variant_name:
        return jsonify({'error': 'Missing required fields: variant, variant_name'}), 400
    card_exist = CardModel.query.get(set_id+str(number)+str(variant)+variant_name)
    if card_exist:
        return jsonify({"error": "Card already exist"}), 409
    card = CardModel(poke_id_variant = set_id+str(number)+str(variant)+variant_name, poke_id = set_id+str(number), poke_name = name, number = str(number), rarity = rarity, variant = bool(variant), variant_name = variant_name, amount = amount)
    
    set_card_exist = SetCollectionModel.query.get(set_id+str(number))
    if not set_card_exist:
        set_card = SetCollectionModel(set_id = set_id, poke_id = set_id+str(number), name = name, number = str(number), amount = amount)
        db.session.add(set_card)

    db.session.add(card)
    db.session.commit()
    update_set_card_amount(set_id+str(number))
    update_collection_amount(set_id)
    return marshal(card, card_fields), 201

@collection.put('/<string:set_id>/<int:number>/<int:variant>/<string:variant_name>')
@collection.patch('/<string:set_id>/<int:number>/<int:variant>/<string:variant_name>')
def patch_card(set_id, number, variant, variant_name):
    card = CardModel.query.get(set_id+str(number)+str(variant)+variant_name)
    if not card:
        return jsonify({'error': 'Card version not found'}), 404

    name = request.get_json().get('name')
    rarity = request.get_json().get('rarity')
    amount = request.get_json().get('amount', 0)

    card.poke_name = name
    card.rarity = rarity
    card.amount = amount

    db.session.commit()
    update_set_card_amount(set_id+str(number))
    update_collection_amount(set_id)
    return marshal(CardModel.query.get(set_id+str(number)+str(variant)+variant_name), card_fields), 200

    
@collection.delete('/<string:set_id>/<int:number>/<int:variant>/<string:variant_name>')
def delete_card(set_id, number, variant, variant_name):
    card = CardModel.query.get(set_id+str(number)+str(variant)+variant_name)
    if not card:
        return jsonify({'error': 'Card version not found'}), 404

    db.session.delete(card)
    db.session.commit()
    update_set_card_amount(set_id+str(number))
    update_collection_amount(set_id)
    return jsonify({}), 204