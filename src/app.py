"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

jackson_family.add_member({
    'name': 'John',
    'age': 33,
    'lucky_numbers': [7,14,22]
})

jackson_family.add_member({
    'name': 'Jane',
    'age': 35,
    'lucky_numbers': [10, 14, 3]
})

jackson_family.add_member({
    'name': 'Jimmy',
    'age': 5,
    'lucky_numbers': [ 1 ]
})

print(jackson_family.serialize())



# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods

    members = jackson_family.get_all_members()
    
    response_body = {
        "members": members
    }

    return jsonify(response_body), 200

@app.route('/members', methods= ['POST'])
def handle_add_member():

    member = request.get_json()

    if member is None: 
        return 'Error body not empty', 400
    if member['name'] is None:
        return 'Error name not empty', 400

    new_member = jackson_family.add_member(member)   
    return jsonify(new_member), 200         

@app.route('/members/<int:member_id>', methods=['GET'])
def handle_get_member(member_id):

    member = jackson_family.get_member(member_id)
    
    if member is None:
        return 'Miembro no encontrado', 404
    else:
     return jsonify({
        "id": member['id'],
        "first_name": member['name'],
        "age": member['age'],
        "lucky_numbers": member['lucky_numbers']

    }), 200

@app.route('/members/<int:id>', methods=['DELETE'])
def handle_delete_member(id):
    success = jackson_family.delete_member(id)
    
    if success:
        return jsonify({}), 204
    else:
        return jsonify({'msg': 'Miembro no encontrado'}), 404



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
