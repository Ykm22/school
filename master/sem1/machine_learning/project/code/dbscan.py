import numpy as np
import pandas as pd
from collections import deque
from multiprocessing import Pool, cpu_count
from functools import partial

class KDTree:
   def __init__(self, points, depth=0):
       if len(points) == 0:
           self.point = None
           self.left = self.right = None
           return
           
       k = points.shape[1]
       axis = depth % k
       points = points[points[:, axis].argsort()]
       median = len(points) // 2
       
       self.point = points[median]
       self.left = KDTree(points[:median], depth + 1)
       self.right = KDTree(points[median + 1:], depth + 1)

   def get_points_in_range(self, target, radius):
       if self.point is None:
           return []
           
       points = []
       if np.sqrt(np.sum((target - self.point) ** 2)) <= radius:
           points.append(self.point)
           
       k = len(target)
       axis = 0 if not hasattr(self, 'depth') else self.depth % k
       
       if target[axis] - radius <= self.point[axis]:
           points.extend(self.left.get_points_in_range(target, radius))
       if target[axis] + radius >= self.point[axis]:
           points.extend(self.right.get_points_in_range(target, radius))
           
       return points

def find_neighbors_chunk(args):
   chunk_start, chunk_size, X, kdtree, eps = args
   chunk_end = min(chunk_start + chunk_size, len(X))
   neighbors = []
   
   for i in range(chunk_start, chunk_end):
       nearby_points = kdtree.get_points_in_range(X[i], eps)
       neighbors.append([j for j in range(len(X)) 
                       if j != i and np.any(np.all(X[j] == nearby_points, axis=1))])
   return neighbors

class ParallelDBSCAN:
   def __init__(self, eps=0.5, min_samples=5, n_jobs=None):
       self.eps = eps
       self.min_samples = min_samples
       self.n_jobs = n_jobs if n_jobs else cpu_count()
       
   def fit(self, X):
       n_samples = len(X)
       self.labels_ = np.full(n_samples, -1)
       visited = np.zeros(n_samples, dtype=bool)
       core_samples = np.zeros(n_samples, dtype=bool)
       
       # Build KD-Tree
       kdtree = KDTree(X)
       
       # Parallel neighbor finding
       chunk_size = n_samples // self.n_jobs
       chunks = [(i, chunk_size, X, kdtree, self.eps) 
                for i in range(0, n_samples, chunk_size)]
       
       print("starting cpus...") 
       with Pool(self.n_jobs) as pool:
           neighbor_chunks = pool.map(find_neighbors_chunk, chunks)
           
       neighbors = [n for chunk in neighbor_chunks for n in chunk]
       
       # Parallel core point identification
       def find_core_points(chunk):
           return [len(n) >= self.min_samples for n in chunk]
       with Pool(self.n_jobs) as pool:
           core_chunks = pool.map(find_core_points, 
                                [neighbors[i:i+chunk_size] 
                                 for i in range(0, len(neighbors), chunk_size)])
       
       core_samples = np.concatenate(core_chunks)
       
       # Cluster expansion (cannot be easily parallelized due to dependencies)
       current_cluster = 0
       for i in range(n_samples):
           if i % 100 == 0:
              print(f"{i}/{n_samples-1}")
           if visited[i] or not core_samples[i]:
               continue
               
           cluster = self._expand_cluster(i, neighbors, visited, core_samples)
           self.labels_[cluster] = current_cluster
           current_cluster += 1
           
       self.core_sample_indices_ = np.where(core_samples)[0]
       return self
       
   def _expand_cluster(self, point_idx, neighbors, visited, core_samples):
       cluster = {point_idx}
       queue = deque([point_idx])
       visited[point_idx] = True
       
       while queue:
           current = queue.popleft()
           if not core_samples[current]:
               continue
               
           for neighbor in neighbors[current]:
               if not visited[neighbor]:
                   visited[neighbor] = True
                   cluster.add(neighbor)
                   if core_samples[neighbor]:
                       queue.append(neighbor)
                       
       return list(cluster)

class ManualDBSCAN:
   def __init__(self, eps=0.5, min_samples=5):
       self.eps = eps
       self.min_samples = min_samples
       self.labels_ = None
       self.core_sample_indices_ = None
       
   def fit(self, X):
       n_samples = len(X)
       self.labels_ = np.full(n_samples, -1)
       visited = np.zeros(n_samples, dtype=bool)
       core_samples = np.zeros(n_samples, dtype=bool)
       
       # Build KD-Tree
       kdtree = KDTree(X)
       
       # Find neighbors using KD-Tree
       neighbors = [[] for _ in range(n_samples)]
       for i in range(n_samples):
           if i % 10 == 0:
              print(f"{i}/{n_samples}")
           nearby_points = kdtree.get_points_in_range(X[i], self.eps)
           neighbors[i] = [j for j in range(n_samples) 
                         if j != i and np.any(np.all(X[j] == nearby_points, axis=1))]
       
       # Find core points
       for i in range(n_samples):
           if len(neighbors[i]) >= self.min_samples:
               core_samples[i] = True
               
       # Assign clusters
       current_cluster = 0
       for i in range(n_samples):
           if visited[i] or not core_samples[i]:
               continue
               
           cluster = self._expand_cluster(i, neighbors, visited, core_samples)
           self.labels_[cluster] = current_cluster
           current_cluster += 1
           
       self.core_sample_indices_ = np.where(core_samples)[0]
       return self

   def _expand_cluster(self, point_idx, neighbors, visited, core_samples):
       cluster = {point_idx}
       queue = deque([point_idx])
       visited[point_idx] = True
       
       while queue:
           current = queue.popleft()
           if not core_samples[current]:
               continue
               
           for neighbor in neighbors[current]:
               if not visited[neighbor]:
                   visited[neighbor] = True
                   cluster.add(neighbor)
                   if core_samples[neighbor]:
                       queue.append(neighbor)
                       
       return list(cluster)

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

def calculate_silhouette(X, labels):
    scores = []
    unique_labels = np.unique(labels[labels != -1])
    
    for i in range(len(X)):
        if labels[i] == -1:
            scores.append(0)
            continue
            
        # Calculate a (mean distance to points in same cluster)
        same_cluster = X[labels == labels[i]]
        if len(same_cluster) <= 1:
            scores.append(0)
            continue
        a = np.mean([np.sqrt(np.sum((X[i] - p) ** 2)) for p in same_cluster if not np.array_equal(p, X[i])])
        
        # Calculate b (mean distance to points in nearest different cluster)
        b = float('inf')
        for label in unique_labels:
            if label != labels[i]:
                other_cluster = X[labels == label]
                mean_dist = np.mean([np.sqrt(np.sum((X[i] - p) ** 2)) for p in other_cluster])
                b = min(b, mean_dist)
                
        scores.append((b - a) / max(a, b) if max(a, b) > 0 else 0)
    
    return np.mean(scores)



# def main():
#    df = pd.read_csv("./housing.csv")
#    df, target = preprocess(df, "median_house_value")
#    X = df.to_numpy()
#    X = scale(X)
#    
#    dbscan = ParallelDBSCAN(eps=1.15, min_samples=25)
#    dbscan.fit(X[:1000])
#    
#    labels = dbscan.labels_
#    n_clusters = len(np.unique(labels)) - (1 if -1 in labels else 0)
#    print(f"Clusters: {n_clusters}")
#    print(f"Noise ratio: {np.sum(labels == -1) / len(labels)}")

def main():
    df = pd.read_csv("./housing.csv")
    df, target = preprocess(df, "median_house_value")
    X = df.to_numpy()
    X = scale(X)
    
    print("Starting clustering...")
    dbscan = ManualDBSCAN(eps=1.15, min_samples=25)
    dbscan.fit(X)
    
    labels = dbscan.labels_
    n_clusters = len(np.unique(labels)) - (1 if -1 in labels else 0)
    print(f"Number of clusters: {n_clusters}")
    
    silhouette = calculate_silhouette(X, labels)
    print(f"Silhouette Score: {silhouette}")
    
    noise_ratio = np.sum(labels == -1) / len(labels)
    print(f"Noise ratio: {noise_ratio}")

if __name__ == "__main__":
    main()
