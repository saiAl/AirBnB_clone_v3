#!/usr/bin/python3
""" view for Review objects that handles all RESTFul API actions """

from models.review import Review
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_Review(place_id):
    """ Retrieves the list of all Review objects of a Place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    all_reviews = []
    for review in storage.all("Review").values():
        if review.place_id == place_id:
            all_reviews.append(review.to_dict())
    return jsonify(all_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review(review_id):
    """ Retrieves a review object"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a review object"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def new_review(place_id):
    """ Creates a review  """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    review = request.get_json(silent=True)
    if review is None:
        return jsonify({"error": "Not a JSON"}), 400

    if "user_id" not in review:
        abort(400, "Missing user_id")
    user = storage.get("User", review["user_id"])

    if user is None:
        abort(404)
    if "text" not in review:
        return jsonify({"error": "Missing text"}), 400
    review["place_id"] = place.id
    review = Review(**review)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a review object """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    update_review = request.get_json(silent=True)
    if update_review is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in update_review.items():
        if key not in ["id", "user_id", "place_id", "created_at",
                       "updated_at"]:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
