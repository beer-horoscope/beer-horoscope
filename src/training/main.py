from flask import Flask

try:
    import src.training.beer_recs
except ImportError:
    import beer_recs
    pass

app = Flask(__name__)

# @app.route('/<beer_name>/<brewery_name>/<beer_type>/<abv>/<other>/', methods=['GET'])
# def rec(beer_name, brewery_name, beer_type, abv, other):
#     return json.dumps(beer_recs.generate_beer_recs(beer_name, brewery_name, beer_type, abv, other, 5))

if __name__ == '__main__':
    # app.run(debug=True)
    beer_recs.train_models()
    print(beer_recs.generate_beer_recs("Cauldron DIPA", "Lagunitas", "", 5.0, ["dark"], 5))
    print(beer_recs.generate_beer_recs("Swannanoa Sunset", "Destihl", "sour", 5.0, [""], 10))
