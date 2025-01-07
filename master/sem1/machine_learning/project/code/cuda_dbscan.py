import numpy as np
import pandas as pd
from numba import cuda, float32
import math

@cuda.jit
def compute_distances_kernel(X, distances, eps_squared):
    idx = cuda.grid(1)
    if idx < X.shape[0]:
        for j in range(X.shape[0]):
            dist = 0.0
            for k in range(X.shape[1]):
                diff = X[idx, k] - X[j, k]
                dist += diff * diff
            distances[idx, j] = 1 if dist <= eps_squared else 0

@cuda.jit
def compute_silhouette_distances(X, point_idx, distances):
    idx = cuda.grid(1)
    if idx < X.shape[0] and idx != point_idx:
        dist = 0.0
        for k in range(X.shape[1]):
            diff = X[idx, k] - X[point_idx, k]
            dist += diff * diff
        distances[idx] = math.sqrt(dist)
    elif idx == point_idx:
        distances[idx] = 0.0

class CudaDBSCAN:
    def __init__(self, eps=0.5, min_samples=5):
        self.eps = eps
        self.min_samples = min_samples
        
    def fit(self, X):
        X = X.astype(np.float32)
        n_samples = X.shape[0]
        
        X_global_mem = cuda.to_device(X)
        distances = cuda.device_array((n_samples, n_samples), dtype=np.int32)
        
        threadsperblock = 256
        blockspergrid = (n_samples + (threadsperblock - 1)) // threadsperblock
        
        eps_squared = float32(self.eps * self.eps)
        compute_distances_kernel[blockspergrid, threadsperblock](X_global_mem, distances, eps_squared)
        
        distances_cpu = distances.copy_to_host()
        
        n_neighbors = np.sum(distances_cpu, axis=1)
        core_samples = n_neighbors >= self.min_samples
        
        labels = np.full(n_samples, -1)
        current_cluster = 0
        
        for i in range(n_samples):
            if labels[i] != -1 or not core_samples[i]:
                continue
            cluster = self._expand_cluster(i, distances_cpu, core_samples, labels)
            labels[cluster] = current_cluster
            current_cluster += 1
            
        self.labels_ = labels
        self.core_sample_indices_ = np.where(core_samples)[0]
        return self
        
    def _expand_cluster(self, point_idx, distances, core_samples, labels):
        from collections import deque
        cluster = {point_idx}
        queue = deque([point_idx])
        labels[point_idx] = 0
        
        while queue:
            current = queue.popleft()
            if not core_samples[current]:
                continue
            neighbors = np.where(distances[current] == 1)[0]
            for neighbor in neighbors:
                if labels[neighbor] == -1:
                    labels[neighbor] = 0
                    cluster.add(neighbor)
                    if core_samples[neighbor]:
                        queue.append(neighbor)
        return list(cluster)

def calculate_silhouette_cuda(X, labels):
    X = X.astype(np.float32)
    n_samples = X.shape[0]
    unique_labels = np.unique(labels[labels != -1])
    
    # CUDA setup
    threadsperblock = 256
    blockspergrid = (n_samples + (threadsperblock - 1)) // threadsperblock
    
    # Move data to GPU
    X_gpu = cuda.to_device(X)
    distances_gpu = cuda.device_array(n_samples, dtype=np.float32)
    
    scores = []
    for i in range(n_samples):
        if labels[i] == -1:
            scores.append(0)
            continue
            
        # Compute all distances from point i to all other points
        compute_silhouette_distances[blockspergrid, threadsperblock](X_gpu, i, distances_gpu)
        distances = distances_gpu.copy_to_host()
        
        # Calculate a (mean distance to same cluster)
        same_cluster_mask = labels == labels[i]
        same_cluster_mask[i] = False
        same_cluster_distances = distances[same_cluster_mask]
        
        if len(same_cluster_distances) == 0:
            scores.append(0)
            continue
            
        a = np.mean(same_cluster_distances)
        
        # Calculate b (mean distance to nearest cluster)
        b = float('inf')
        for label in unique_labels:
            if label != labels[i]:
                other_cluster_distances = distances[labels == label]
                if len(other_cluster_distances) > 0:
                    mean_dist = np.mean(other_cluster_distances)
                    b = min(b, mean_dist)
                    
        scores.append((b - a) / max(a, b) if max(a, b) > 0 else 0)
    
    return np.mean(scores)

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

def main():
    df = pd.read_csv("./housing.csv")
    df, target = preprocess(df, "median_house_value")
    X = df.to_numpy()
    X = scale(X)
    
    print("Starting CUDA DBSCAN clustering...")
    dbscan = CudaDBSCAN(eps=1.15, min_samples=25)
    dbscan.fit(X)
    
    labels = dbscan.labels_
    n_clusters = len(np.unique(labels)) - (1 if -1 in labels else 0)
    print(f"Number of clusters: {n_clusters}")
    
    silhouette = calculate_silhouette_cuda(X, labels)
    print(f"Silhouette Score: {silhouette}")
    
    noise_ratio = np.sum(labels == -1) / len(labels)
    print(f"Noise ratio: {noise_ratio}")

if __name__ == "__main__":
    main()
