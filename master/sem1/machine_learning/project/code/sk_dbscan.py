from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd
from performance_measures import calculate_silhouette, calculate_mutual_information, calculate_stability_score, calculate_inertia, calculate_calinski_harabasz, calculate_adjusted_rand_index
from preprocessing import preprocess, scale

def dbscan_analysis():
    # Load and preprocess data
    df = pd.read_csv("./housing.csv")
    df, target = preprocess(df, "median_house_value")
    X = df.to_numpy()
    X = scale(X)
    
    print("Clustering start")
    clustering = DBSCAN(eps=0.782, min_samples=15).fit(X)
    print("Clustering finish")
    
    labels = clustering.labels_
    n_clusters = len(np.unique(labels[labels != -1]))
    print(f"Number of clusters: {n_clusters}")
    
    # Calculate custom metrics
    sil_score = calculate_silhouette(X, labels)
    ch_score = calculate_calinski_harabasz(X, labels)
    inertia = calculate_inertia(X, labels)
    
    # Create bins for target values to match cluster count
    target_bins = pd.qcut(target, q=max(n_clusters, 1), labels=False)
    ari_score = calculate_adjusted_rand_index(target_bins, labels)
    homogeneity = calculate_homogeneity(target_bins, labels)
    
    # Calculate noise ratio
    noise_ratio = np.sum(labels == -1) / len(labels)
    
    # Print results
    print("\nClustering Results:")
    print("-" * 40)
    print(f"Number of clusters: {n_clusters}")
    print(f"Silhouette Score: {sil_score:.3f}")
    print(f"Calinski-Harabasz Score: {ch_score:.3f}")
    print(f"Inertia: {inertia:.3f}")
    print(f"Adjusted Rand Index: {ari_score:.3f}")
    print(f"Homogeneity Score: {homogeneity:.3f}")
    print(f"Noise ratio: {noise_ratio:.3f}")

if __name__ == "__main__":
    dbscan_analysis()
