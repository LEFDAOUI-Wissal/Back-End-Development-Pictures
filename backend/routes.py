from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if 1 <= id <= len(data):
        return jsonify(data[id - 1])
    else:
        abort(404, description="Picture not found")



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    # Extract picture data from the request body
    new_picture = request.json

    # Check if a picture with the given id already exists
    for picture in data:
        if picture['id'] == new_picture['id']:
            return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302

    # Append the new picture to the data list
    data.append(new_picture)

    # Return the created picture with a 201 status code
    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # Extract picture data from the request body
    updated_picture = request.json

    # Find the picture in the data list
    for index, picture in enumerate(data):
        if picture['id'] == id:
            # Update the picture with the incoming request data
            data[index] = {**picture, **updated_picture}
            # Ensure the id remains unchanged
            data[index]['id'] = id
            return jsonify(data[index]), 200

    # If the picture is not found, return a 404 error
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Find the picture in the data list by id
    picture = next((pic for pic in data if pic['id'] == id), None)
    
    # If the picture is not found, return a 404 error
    if picture is None:
        return make_response(
            jsonify({"message": "picture not found"}), 404
        )

    # If the picture is found, remove it from the data list
    data.remove(picture)
    
    # Return a 204 No Content response on successful deletion
    return '', 204