from sklearn.cluster import DBSCAN
from sklearn.metrics import (
    silhouette_score,
    adjusted_rand_score,
    calinski_harabasz_score,
    mutual_info_score
)
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

def preprocess(df, target_column):
    # Discretize string values
    df["ocean_proximity"] = df["ocean_proximity"].map({
        x: i for i, x in enumerate(df["ocean_proximity"].unique())
    })
    df.dropna(inplace=True)
    # Separate train inputs from target values
    target = df[target_column]
    df = df.drop(target_column, axis=1)
    df.drop(["population", "total_bedrooms", "households", "longitude", "housing_median_age"], axis=1, inplace=True)
    return df, target

def scale(X):
    # Compute mean and std for each feature
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    
    # Standardize by subtracting mean and dividing by std
    X = (X - mean) / std
    return X

def calculate_inertia(X, labels):
    # Filter out noise points (label -1)
    unique_labels = np.unique(labels[labels != -1])
    inertia = 0
    
    for label in unique_labels:
        cluster_points = X[labels == label]
        if len(cluster_points) > 0:  # Ensure cluster has points
            centroid = np.mean(cluster_points, axis=0)
            inertia += np.sum(cdist([centroid], cluster_points) ** 2)
    
    return inertia

def dbscan():
    # Load and preprocess data
    df = pd.read_csv("./housing.csv")
    df, target = preprocess(df, "median_house_value")
    df.dropna(inplace=True)
    X = df.to_numpy()
    X = scale(X)
    
    print("Clustering start")
    clustering = DBSCAN(eps=1.15, min_samples=25).fit(X)
    print("Clustering finish")
    
    labels = clustering.labels_
    n_clusters = len(np.unique(labels)) - (1 if -1 in labels else 0)
    
    # Calculate metrics matching the table
    metrics = {
        "Number of Clusters": n_clusters,
        "Silhouette Score": silhouette_score(X, labels) if len(np.unique(labels)) > 1 else 0,
        "Calinski-Harabasz Score": calinski_harabasz_score(X, labels),
        "Inertia": calculate_inertia(X, labels),
        "Adjusted Rand Index": adjusted_rand_score(
            pd.qcut(target, q=max(n_clusters, 2), labels=False),
            labels
        ),
        "Mutual Information": mutual_info_score(
            pd.qcut(target, q=max(n_clusters, 2), labels=False),
            labels
        ),
        "Noise Ratio": np.sum(labels == -1) / len(labels)
    }
    
    # Print results in a formatted table
    print("\nClustering Metrics:")
    print("-" * 50)
    for metric, value in metrics.items():
        print(f"{metric:<25} {value:.4f}")

if __name__ == "__main__":
    dbscan()
