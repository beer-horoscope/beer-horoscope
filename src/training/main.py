from flask import Flask

try:
    import src.training.beer_recs
except ImportError:
    import beer_recs
    pass

app = Flask(__name__)

if __name__ == '__main__':
    beer_recs.train_models()
    print(beer_recs.generate_beer_recs(["Cauldron DIPA"], 5))
    print(beer_recs.generate_beer_recs(["Swannanoa Sunset"], 10))
