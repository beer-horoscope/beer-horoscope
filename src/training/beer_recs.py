import os
import pickle

import pandas as pd
import sqlalchemy as sql

try:
    import src.training.model_cbf_cos_sim as model_cbf_cos_sim
    import src.training.model_cf_svd as model_cf_svd
except ImportError:
    import model_cbf_cos_sim
    import model_cf_svd
    pass

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

corr = None
beer_names_list = None
cosine_sim = None
indices = None
dfbag = None

TRAINED_MODELS_DIR = None
HOST=None
PORT=None
DATABASE=None
USER=None
PASSWD=None


def get_beer_recs_dataframe():
    populate_env_variables()

    # Database call
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    # server = 'mysql://user:password@payday.thekeunster.local:3306/beer_horoscope'
    # server = 'mysql://user:password@localhost:3306/beer_horoscope'
    server = 'mysql://{}:{}@{}:{}/{}'.format(USER, PASSWD, HOST, PORT, DATABASE)
    engine = sql.create_engine('{}'.format(server))
    query = '''select `review_profilename`, `brewery_name`, `beer_name`, `beer_style`, `beer_abv`, `review_overall` from `beer_reviews`'''
    df = pd.read_sql_query(query, engine)

    return df


def train_svd_model(dataframe):
    TRAINED_MODELS_DIR = os.getenv('TRAINED_MODELS_DIR')
    if TRAINED_MODELS_DIR is None:
        TRAINED_MODELS_DIR = ''

    corr, beer_names_list = model_cf_svd.train_data_svd(dataframe)

    pickle_out_svd_corr = open('{}corr.pickle'.format(TRAINED_MODELS_DIR), 'wb')
    pickle_out_svd_beer_names_list = open('{}beer_names_list.pickle'.format(TRAINED_MODELS_DIR), 'wb')
    pickle.dump(corr, pickle_out_svd_corr)
    pickle.dump(beer_names_list, pickle_out_svd_beer_names_list)
    pickle_out_svd_corr.close()
    pickle_out_svd_beer_names_list.close()


def train_cos_sim_model(dataframe):
    TRAINED_MODELS_DIR = os.getenv('TRAINED_MODELS_DIR')
    if TRAINED_MODELS_DIR is None:
        TRAINED_MODELS_DIR = ''

    cosine_sim, indices, dfbag = model_cbf_cos_sim.train_data_cos_sim(dataframe)

    pickle_out_cos_sim_cosine_sim = open('{}cosine_sim.pickle'.format(TRAINED_MODELS_DIR), 'wb')
    pickle_out_cos_sim_indices = open('{}indices.pickle'.format(TRAINED_MODELS_DIR), 'wb')
    pickle_out_cos_sim_dfbag = open('{}dfbag.pickle'.format(TRAINED_MODELS_DIR), 'wb')
    pickle.dump(cosine_sim, pickle_out_cos_sim_cosine_sim)
    pickle.dump(indices, pickle_out_cos_sim_indices)
    pickle.dump(dfbag, pickle_out_cos_sim_dfbag)
    pickle_out_cos_sim_cosine_sim.close()
    pickle_out_cos_sim_indices.close()
    pickle_out_cos_sim_dfbag.close()


def train_models():
    dataframe = get_beer_recs_dataframe()
    train_svd_model(dataframe)
    train_cos_sim_model(dataframe)
    load_inmemory()


def load_inmemory():
    global corr
    global beer_names_list
    global cosine_sim
    global indices
    global dfbag

    try:
        TRAINED_MODELS_DIR = os.getenv('TRAINED_MODELS_DIR')
        if TRAINED_MODELS_DIR is None:
            TRAINED_MODELS_DIR = ''

        populate_env_variables()
        # Database call
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        # server = 'mysql://user:password@payday.thekeunster.local:3306/beer_horoscope'
        # server = 'mysql://user:password@localhost:3306/beer_horoscope'
        server = 'mysql://{}:{}@{}:{}/{}'.format(USER, PASSWD, HOST, PORT, DATABASE)
        engine = sql.create_engine('{}'.format(server))
        query = '''
        SELECT DISTINCT
            beer_beerid,
            beer_name,
            brewery_id, 
            brewery_name,
            beer_style,
            beer_abv
        from beer_reviews
        '''

        print('populating beer list')
        df = pd.read_sql_query(query, engine)
        beer_names_list_from_df = df.values.tolist()

        beer_names_list = []
        for beer in beer_names_list_from_df:
            beer_map = {}
            beer_map['beer_beerid'] = beer[0]
            beer_map['beer_name'] = beer[1]
            beer_map['brewery_id'] = beer[2]
            beer_map['brewery_name'] = beer[3]
            beer_map['beer_style'] = beer[4]
            beer_map['beer_abv'] = beer[5]
            beer_names_list.append(beer_map)

        print('loading corr')
        f1 = open("{}corr.pickle".format(TRAINED_MODELS_DIR), "rb")
        corr = pickle.load(f1)

        # f2 = open("{}beer_names_list.pickle".format(TRAINED_MODELS_DIR), "rb")
        # beer_names_list_from_pickle = pickle.load(f2)

        print('loading cosine sim')
        f3 = open("{}cosine_sim.pickle".format(TRAINED_MODELS_DIR), "rb")
        cosine_sim = pickle.load(f3)

        print('loading indices')
        f4 = open("{}indices.pickle".format(TRAINED_MODELS_DIR), "rb")
        indices = pickle.load(f4)

        print('loading dfbag')
        f5 = open("{}dfbag.pickle".format(TRAINED_MODELS_DIR), "rb")
        dfbag = pickle.load(f5)
    except:
        print("Error loading in-memory models")

def generate_cos_sim_beer_recs(beer_names, n):
    if cosine_sim is None or indices is None or dfbag is None:
        load_inmemory()

    cbf_recs = model_cbf_cos_sim.beer_recs_cbf(beer_names, int(n / 2), cosine_sim, indices, dfbag)
    return cbf_recs


def generate_svd_beer_recs(beer_names, n):
    if corr is None or beer_names_list is None:
        load_inmemory()

    cf_recs = model_cf_svd.beer_recs_cf(beer_names, int(n / 2), corr, beer_names_list)

    return cf_recs


def generate_beer_recs(beer_names, n):
    cbf_recs = generate_cos_sim_beer_recs(beer_names, n)
    cf_recs = generate_svd_beer_recs(beer_names, n)

    return cbf_recs + list(set(cf_recs) - set(cbf_recs))


def generate_beer_names():
    if beer_names_list is None:
        load_inmemory()

    return beer_names_list

def generate_beer_names_tag(tag):
    if beer_names_list is None:
        load_inmemory()

    return list(filter(lambda k: tag.lower() in k['beer_name'].lower(), beer_names_list))

def populate_env_variables():
    global HOST
    global PORT
    global DATABASE
    global USER
    global PASSWD

    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    DATABASE = os.getenv('DATABASE')
    USER = os.getenv('USER')
    PASSWD = os.getenv('PASSWORD')