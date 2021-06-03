import logging

import numpy as np

try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    pass

from sklearn.decomposition import TruncatedSVD


def train_data_svd(dataframe):
    # Shorten the dataset for testing purposes
    df = dataframe.head(10000)
    #df = dataframe

    # create a sparse pivot table
    df_pivot = df.pivot_table(index='review_profilename', columns='beer_name', values='review_overall').fillna(0)
    T = df_pivot.values.T
    SVD = TruncatedSVD(n_components=600, random_state=600)
    matrix = SVD.fit_transform(T)

    # Create the correlation matrix
    corr = np.corrcoef(matrix)

    # Put all the beer names in a list
    beer_names = df_pivot.columns
    beer_names_list = list(beer_names)

    return corr, beer_names_list


# Takes in the name of the beer and returns the top n number of recommended beers

def beer_recs_cf(beer_names, n, corr, beer_names_list):

    def build_dict(seq, key):
        return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

    info_by_name = build_dict(beer_names_list, key="beer_name")

    for beer_name in beer_names:
        beer_idx = info_by_name.get(beer_name)["index"]

        out = []

        try:
            sim_idx = corr[beer_idx]  # Get the similarity index of the input beer

            # Create a list of tuples (beer name, correlation coefficient)
            similar = []
            for idx, coeff in enumerate(sim_idx):
                similar.append((beer_names_list[idx]["beer_name"], coeff))

            similar.sort(key=lambda x: x[1], reverse=True)

            for i in range(1, n + 1):
                out.append(similar[i][0])
        except:
            pass

    return out
