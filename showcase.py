import requests

url = "http://127.0.0.1:5000/api/v1/collection"

# Test collection
set_payload = [
    {"set_id": None},
    {"set_id": "s12a"},
    {"set_id": "sv2a"},
    {"set_id": "sv8a"}
]

number_sv2a = [68, 68, 168, 170, 173]
card_payload_sv2a = [
    {"name": "Machamp", "rarity": "R", "variant": "0", "variant_name": "OG", "amount": 1},
    {"name": "Machamp", "rarity": "R", "variant": "1", "variant_name": "MBRH", "amount": 2},
    {"name": "Charmander", "rarity": "AR", "variant": "0", "variant_name": "OG", "amount": 1},
    {"name": "Squirtle", "rarity": "AR", "variant": "0", "variant_name": "OG", "amount": 1},
    {"name": "Pikachu", "rarity": "AR", "variant": "0", "variant_name": "OG", "amount": 1}
]

number_sv8a = [110, 111, 113]
card_payload_sv8a = [
    {"name": "Feebas", "rarity": "AR", "variant": "0", "variant_name": "OG", "amount": 1},
    {"name": "Spheal", "rarity": "AR", "variant": "0", "variant_name": "OG", "amount": 1},
    {"name": "Stunfisk", "rarity": "AR", "variant": "0", "variant_name": "OG", "amount": 1}
]

patch_payload_sv2a = {"name": "Pika", "amount": 5}

patch_payload_sv8a = [
    {"name": "Feebas", "rarity": "SR", "variant": "0", "variant_name": "OG", "amount": 0},
    {"name": "Spheal", "rarity": "AR", "variant": "0", "variant_name": "OG", "amount": 5},
    {"name": "Stunfisk", "rarity": "R", "variant": "0", "variant_name": "OG", "amount": 10}
] 

# python src/showcase.py

# Collection Methods

'''# Get empty collection
print(requests.get(url+"/").json())

# Add and delete sets from collection
for payload in set_payload:
    print(requests.post(url+"/", json = payload).json())
print(requests.delete(url+"/s12a"))
print(requests.get(url+"/").json())

# Get collection by generation
print(requests.get(url+"/9").json())   ''' 


# Card Methods

'''# Add and delete cards from collection
for number, payload in zip(number_sv2a, card_payload_sv2a):
    print(requests.post(url+f"/sv2a/{number}", json = payload).json())
for number, payload in zip(number_sv8a, card_payload_sv8a):
    print(requests.post(url+f"/sv8a/{number}", json = payload).json())
print(requests.delete(url+"/sv2a/168/0/OG")) # Delete Charmander
print(requests.get(url+"/sv2a/168/0/OG").json()) # Check Charmander deleted
print(requests.get(url+"/sv2a/68/1/MBRH").json()) # Get Machamp variant

# Patch cards from collection
for number, payload in zip(number_sv8a, patch_payload_sv8a):
    print(requests.get(url+f"/sv8a/{number}/0/OG").json())
    print(requests.patch(url+f"/sv8a/{number}/0/OG", json = payload).json())
    print(requests.get(url+f"/sv8a/{number}/0/OG").json())'''

# Set Collection Methods

# Get Machamp
print(requests.get(url+"/name/Machamp").json())
print(requests.get(url+"/sv2a/68").json())

# Delete Machamp
print(requests.delete(url+"/sv2a/68"))
print(requests.get(url+"/name/Machamp/1/MBRH").json())

# Patch Pikachu
print(requests.get(url+f"/sv2a/173").json())
print(requests.patch(url+f"/sv2a/173", json = patch_payload_sv2a).json())
print(requests.get(url+f"/sv2a/173").json())


