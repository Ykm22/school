from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, adjusted_rand_score
import numpy as np
import pandas as pd
from sklearn.metrics import davies_bouldin_score, calinski_harabasz_score
from sklearn.metrics import homogeneity_score, completeness_score, v_measure_score
from scipy.spatial.distance import cdist

def preprocess(df, target_column):
    # Discretisize string values
    df["ocean_proximity"] = df["ocean_proximity"].map({
       x: i for i, x in enumerate(df["ocean_proximity"].unique())
    })

    df.dropna(inplace=True)
    # Separate train inputs to target values
    target = df[target_column]
    df = df.drop(target_column, axis=1)
    df.drop(["population", "total_bedrooms", "households", "longitude", "housing_median_age"], axis=1, inplace=True)
    print(df.columns.to_numpy())
    

    return df, target

def scale(X):
    # Compute mean and std for each feature
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    
    # Standardize by subtracting mean and dividing by std
    X = (X - mean) / std

    return X

def dbscan():
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
   print(f"Number of clusters: {n_clusters}")
   
   # Basic metrics
   sil_score = silhouette_score(X, labels) if len(np.unique(labels)) > 1 else 0
   print(f"Silhouette Score: {sil_score}")
   
   target_bins = pd.qcut(target, q=n_clusters, labels=False)
   ari_score = adjusted_rand_score(target_bins, labels)
   print(f"Adjusted Rand Index: {ari_score}")
   
   # Additional metrics
   db_score = davies_bouldin_score(X, labels)
   ch_score = calinski_harabasz_score(X, labels)
   print(f"Davies-Bouldin Score: {db_score}")
   print(f"Calinski-Harabasz Score: {ch_score}")
   
   homogeneity = homogeneity_score(target_bins, labels)
   completeness = completeness_score(target_bins, labels)
   v_measure = v_measure_score(target_bins, labels)
   print(f"Homogeneity: {homogeneity}")
   print(f"Completeness: {completeness}")
   print(f"V-measure: {v_measure}")
   
   noise_ratio = np.sum(labels == -1) / len(labels)
   core_samples_mask = np.zeros_like(labels, dtype=bool)
   core_samples_mask[clustering.core_sample_indices_] = True
   print(f"Noise ratio: {noise_ratio}")

def calculate_inertia(X, labels):
   unique_labels = np.unique(labels[labels != -1])
   inertia = 0
   for label in unique_labels:
       cluster_points = X[labels == label]
       centroid = np.mean(cluster_points, axis=0)
       inertia += np.sum(cdist([centroid], cluster_points) ** 2)
   return inertia

if __name__ == "__main__":
    dbscan()
