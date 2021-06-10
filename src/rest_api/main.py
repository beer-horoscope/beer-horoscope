import threading

from flask import Flask, request, jsonify

from src.rest_api.services.beer_rec_service import get_beer_recs, get_beer_names, get_beer_names_tag, post_beer_ratings
from src.training.beer_recs import load_inmemory, train_models

app = Flask(__name__)

load_inmemory()

lock = threading.Lock()

"""
POST /api/recommendation Request Body Format Samples

sample #1

{
    "beer_names": ["Cauldron DIPA"],
    "n": 5
}

sample #2

{
    "beer_names": ["Swannanoa Sunset", "Hefeweizen"],
    "n": 10
}
"""

@app.route('/api/recommendation', methods=['POST'])
def recommendation():
    response = ''
    params = request.get_json()
    if request.method == 'POST':
        response = jsonify(get_beer_recs(
            params["beer_names"],
            params["n"]
        ))
    return response


"""
POST /api/rating Request Body Format Samples

sample #1

{
    "beer_name" : "Swannanoa Sunset",
    "review_overall" : 3
}

"""


@app.route('/api/rating', methods=['POST'])
def rating():
    params = request.get_json()
    if request.method == 'POST':
        response = jsonify(result=post_beer_ratings(
            beer_name=params["beer_name"],
            review_overall=params["review_overall"]
        ))
    return response


@app.route('/api/beer', methods=['GET'])
def beer_names():
    if request.method == 'GET':
        response = jsonify(get_beer_names())
        return response


@app.route('/api/beer/<tag>', methods=['GET'])
def beer_names_tag(tag):
    if request.method == 'GET':
        response = jsonify(get_beer_names_tag(tag))
        return response


@app.route('/api/cache', methods=['GET'])
def cache_refresh():
    if request.method == 'GET':
        thread = threading.Thread(target=mutual_cache_refresh, args=(lock,))
        thread.daemon = True
        thread.start()
        return "cache refreshing"


@app.route('/api/train', methods=['GET'])
def trigger_train_models():
    if request.method == 'GET':
        thread = threading.Thread(target=mutual_train_models, args=(lock,))
        thread.daemon = True
        thread.start()
        return "training data. this will take a while"


@app.route('/api/test', methods=['GET', 'POST', 'PUT'])
def test():
    return "api test results"


def mutual_train_models(local_lock):
    local_lock.acquire()

    try:
        train_models()
    finally:
        local_lock.release()

    return


def mutual_cache_refresh(local_lock):
    local_lock.acquire()

    try:
        load_inmemory()
    finally:
        local_lock.release()

    return


if __name__ == '__main__':
    app.run()
