import pandas as pd

try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    pass

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def train_data_cos_sim(dataframe):
    df = dataframe
    df = df.drop_duplicates(subset=['beer_name'])

    # Shorten the dataset for testing purposes
    df = df.head(9000)
    #df = df.head(40000)

    cols = ['brewery_name', 'beer_style', 'beer_abv']
    df['key_words'] = df[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)

    dfbag = df[['beer_name', 'key_words']].copy()

    dfbag["key_words"] = dfbag["key_words"].str.lower()
    dfbag["key_words"] = dfbag["key_words"].replace('/', '')

    dfbag = dfbag.reset_index(drop=True)

    count = CountVectorizer()
    count_matrix = count.fit_transform(dfbag['key_words'])

    # Generate the cosine similarity matrix
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    # Create a Series for the beers so they are associated to an ordered numerical list
    indices = pd.Series(dfbag['beer_name'])

    return cosine_sim, indices, dfbag


# Takes in the name of the beer and returns the top n nunber of recommended beers

def beer_recs_cbf(beer_names, n, cosine_sim, indices, dfbag):
    recommended_beers = []

    for beer_name in beer_names:
        beer_index = indices[indices == beer_name];

        if len(beer_index) > 0:
            # Get the index of the beer that matches the beer name
            idx = beer_index.index[0]

            # Creating a Series with the similarity scores in descending order
            score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)

            # Get the indices of the n most similar unique beers
            n = n + 1
            top_n_indexes = list(score_series.iloc[1:n].index)

            # Populating the list with the names of the n most similar beers
            for i in top_n_indexes:
                recommended_beers.append(dfbag.iloc[i]['beer_name'])

    return recommended_beers
