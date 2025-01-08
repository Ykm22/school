import numpy as np

def preprocess(df, target_column):
    df["ocean_proximity"] = df["ocean_proximity"].map({
        x: i for i, x in enumerate(df["ocean_proximity"].unique())
    })
    df.dropna(inplace=True)
    target = df[target_column]
    df = df.drop(target_column, axis=1)
    df.drop(["population", "total_bedrooms", "households", "longitude", "housing_median_age"], axis=1, inplace=True)
    return df, target

def scale(X):
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    return (X - mean) / std
