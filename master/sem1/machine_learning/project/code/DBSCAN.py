import numpy as np
from collections import deque

class StandardDBSCAN:
    def __init__(self, eps=0.5, min_samples=5):
        self.eps = eps
        self.min_samples = min_samples
        
    def fit(self, X):
        X = np.array(X, dtype=np.float64)
        n_samples = X.shape[0]
        
        # Calculate distance matrix
        distances = np.zeros((n_samples, n_samples))
        for i in range(n_samples):
            diff = X - X[i]
            distances[i] = np.sqrt(np.sum(diff * diff, axis=1)) <= self.eps
        
        # Identify core points
        n_neighbors = np.sum(distances, axis=1)
        core_samples = n_neighbors >= self.min_samples
        
        # Initialize labels
        labels = np.full(n_samples, -1)
        current_cluster = 0
        
        # Expand clusters
        for i in range(n_samples):
            if labels[i] != -1 or not core_samples[i]:
                continue
            
            # Start new cluster
            cluster = self._expand_cluster(i, distances, core_samples, labels)
            labels[cluster] = current_cluster
            current_cluster += 1
        
        self.labels_ = labels
        self.core_sample_indices_ = np.where(core_samples)[0]
        return self
    
    def _expand_cluster(self, point_idx, distances, core_samples, labels):
        """Expand cluster using breadth-first search"""
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
