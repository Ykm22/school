import numpy as np
import pandas as pd
from numba import cuda, float32
import math
from matplotlib import pyplot as plt

def calculate_stability_score(X, eps, min_samples_range, dbscan_class):
    """Calculate clustering stability for different minPoints values"""
    stability_scores = []
    n_clusters_list = []
    noise_ratios = []
    
    def run_dbscan(min_samples):
        dbscan = dbscan_class(eps=eps, min_samples=min_samples)
        labels = dbscan.fit(X).labels_
        n_clusters = len(np.unique(labels[labels != -1]))
        noise_ratio = np.sum(labels == -1) / len(labels)
        return labels, n_clusters, noise_ratio
    
    # Run initial clustering for all min_samples values
    results = []
    for min_samples in min_samples_range:
        labels, n_clusters, noise_ratio = run_dbscan(min_samples)
        results.append((labels, n_clusters, noise_ratio))
        target = target.to_numpy()
        n_clusters_list.append(n_clusters)
        noise_ratios.append(noise_ratio)
    
    # Calculate stability scores
    for i in range(len(min_samples_range)):
        if i == 0:
            # For the first value, compare with the next one
            score = np.mean(results[i][0] == results[i+1][0])
        elif i == len(min_samples_range) - 1:
            # For the last value, compare with the previous one
            score = np.mean(results[i][0] == results[i-1][0])
        else:
            # For middle values, compare with both neighbors
            score = (np.mean(results[i][0] == results[i-1][0]) + 
                    np.mean(results[i][0] == results[i+1][0])) / 2
        stability_scores.append(score)
    
    return np.array(stability_scores), np.array(n_clusters_list), np.array(noise_ratios)

def plot_minpoints_analysis(X, eps, dbscan_class):
    """Analyze and visualize minPoints parameter selection"""
    # Calculate dimension-based recommendation
    d = X.shape[1]  # number of dimensions
    min_samples_base = 2 * d  # basic rule of thumb
    
    # Generate range of min_samples to test
    min_samples_range = np.arange(max(2, min_samples_base - 5), 
                                 min_samples_base + 15)
    
    # Calculate stability scores and cluster info
    stability_scores, n_clusters, noise_ratios = calculate_stability_score(
        X, eps, min_samples_range, dbscan_class)
    
    # Create figure with three subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
    
    # Plot 1: Stability Score
    ax1.plot(min_samples_range, stability_scores, 'b-', label='Stability')
    ax1.axvline(x=min_samples_base, color='r', linestyle='--', 
                label=f'Dimension-based ({min_samples_base})')
    ax1.set_xlabel('minPoints')
    ax1.set_ylabel('Stability Score')
    ax1.set_title('Clustering Stability vs minPoints')
    ax1.grid(True)
    ax1.legend()
    
    # Plot 2: Number of Clusters
    ax2.plot(min_samples_range, n_clusters, 'g-', label='Clusters')
    ax2.axvline(x=min_samples_base, color='r', linestyle='--',
                label=f'Dimension-based ({min_samples_base})')
    ax2.set_xlabel('minPoints')
    ax2.set_ylabel('Number of Clusters')
    ax2.set_title('Number of Clusters vs minPoints')
    ax2.grid(True)
    ax2.legend()
    
    # Plot 3: Noise Ratio
    ax3.plot(min_samples_range, noise_ratios, 'm-', label='Noise Ratio')
    ax3.axvline(x=min_samples_base, color='r', linestyle='--',
                label=f'Dimension-based ({min_samples_base})')
    ax3.set_xlabel('minPoints')
    ax3.set_ylabel('Noise Ratio')
    ax3.set_title('Noise Ratio vs minPoints')
    ax3.grid(True)
    ax3.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Find optimal minPoints
    # Combine stability and cluster count criteria
    normalized_stability = (stability_scores - stability_scores.min()) / \
                         (stability_scores.max() - stability_scores.min())
    normalized_clusters = (n_clusters - n_clusters.min()) / \
                        (n_clusters.max() - n_clusters.min())
    
    # Weight stability more heavily than number of clusters
    combined_score = 0.7 * normalized_stability - \
                    0.3 * normalized_clusters
    
    optimal_idx = np.argmax(combined_score)
    optimal_minpoints = min_samples_range[optimal_idx]
    
    return optimal_minpoints, min_samples_base
@cuda.jit
def compute_kdistances_kernel(X, k_distances, k):
    """Modified kernel with reduced memory usage"""
    idx = cuda.grid(1)
    if idx < X.shape[0]:
        batch_size = 128
        distances = cuda.local.array(128, dtype=float32)
        current_k_distance = float32(1e9)
        
        for batch_start in range(0, X.shape[0], batch_size):
            batch_end = min(batch_start + batch_size, X.shape[0])
            
            for j in range(batch_start, batch_end):
                if j != idx:
                    dist = float32(0.0)
                    for d in range(X.shape[1]):
                        diff = X[idx, d] - X[j, d]
                        dist += diff * diff
                    distances[j - batch_start] = math.sqrt(dist)
                else:
                    distances[j - batch_start] = float32(1e9)
            
            for i in range(batch_end - batch_start):
                count_smaller = 0
                for j in range(X.shape[0]):
                    if distances[i] < current_k_distance:
                        count_smaller += 1
                        if count_smaller > k:
                            current_k_distance = distances[i]
                            break
        
        k_distances[idx] = current_k_distance

def calculate_kdistances_safe(X, k=4):
    """Safer version of k-distance calculation with proper memory management"""
    try:
        X = X.astype(np.float32)
        n_samples = X.shape[0]
        
        # Initialize device arrays
        X_device = cuda.to_device(X)
        k_distances_device = cuda.device_array(n_samples, dtype=np.float32)
        
        # Configure CUDA kernel
        threadsperblock = min(256, n_samples)
        blockspergrid = (n_samples + (threadsperblock - 1)) // threadsperblock
        
        # Execute kernel
        compute_kdistances_kernel[blockspergrid, threadsperblock](X_device, k_distances_device, k)
        
        # Synchronize and copy results
        cuda.synchronize()
        k_distances = k_distances_device.copy_to_host()
        
        # Clean up explicitly
        X_device = None
        k_distances_device = None
        
        return np.sort(k_distances)[::-1]
        
    except Exception as e:
        print(f"CUDA calculation failed: {e}")
        return calculate_kdistances_cpu(X, k)

def calculate_kdistances_cpu(X, k=4):
    """CPU fallback implementation"""
    print("Using CPU fallback for k-distance calculation...")
    n_samples = X.shape[0]
    k_distances = np.zeros(n_samples)
    
    for i in range(n_samples):
        distances = np.sqrt(np.sum((X - X[i])**2, axis=1))
        distances.sort()
        k_distances[i] = distances[k + 1]
    
    return np.sort(k_distances)[::-1]

def find_elbow_point(kdistances):
    """Find elbow point using curvature method"""
    x = np.array(range(len(kdistances)))
    y = kdistances
    
    # Normalize coordinates
    x_norm = (x - x.min()) / (x.max() - x.min())
    y_norm = (y - y.min()) / (y.max() - y.min())
    
    # Calculate curvature with smoothing
    dx_dt = np.gradient(x_norm)
    dy_dt = np.gradient(y_norm)
    d2x_dt2 = np.gradient(dx_dt)
    d2y_dt2 = np.gradient(dy_dt)
    curvature = np.abs(d2x_dt2 * dy_dt - dx_dt * d2y_dt2) / (dx_dt * dx_dt + dy_dt * dy_dt)**1.5
    
    # Find elbow point (maximum curvature)
    elbow_idx = np.argmax(curvature[10:-10]) + 10
    return elbow_idx

def plot_kdistance(X, k=4):
    """Generate k-distance plot with improved error handling"""
    try:
        # Calculate k-distances
        kdistances = calculate_kdistances_safe(X, k)
        
        # Create plot
        plt.figure(figsize=(10, 6))
        plt.plot(range(len(kdistances)), kdistances, 'b-')
        plt.xlabel('Points sorted by distance')
        plt.ylabel(f'{k}-distance')
        plt.title(f'{k}-distance Plot for DBSCAN Parameter Selection')
        plt.grid(True)
        
        # Find and mark elbow point
        elbow_idx = find_elbow_point(kdistances)
        suggested_eps = kdistances[elbow_idx]
        
        plt.plot(elbow_idx, kdistances[elbow_idx], 'ro', 
                label=f'Suggested eps ≈ {suggested_eps:.3f}')
        plt.legend()
        
        plt.show()
        return suggested_eps
        
    except Exception as e:
        print(f"Error in plot_kdistance: {e}")
        print("Falling back to default eps value...")
        return 1.15

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

def calculate_calinski_harabasz(X, labels):
    """Calculate Calinski-Harabasz Index without sklearn"""
    n_samples = X.shape[0]
    unique_labels = np.unique(labels[labels != -1])
    n_clusters = len(unique_labels)
    
    if n_clusters <= 1:
        return 0.0
        
    # Calculate overall mean
    overall_mean = np.mean(X, axis=0)
    
    # Calculate between-cluster sum of squares (BCSS)
    bcss = 0.0
    wcss = 0.0
    
    for label in unique_labels:
        cluster_points = X[labels == label]
        n_points = len(cluster_points)
        if n_points == 0:
            continue
            
        # Cluster center
        cluster_mean = np.mean(cluster_points, axis=0)
        
        # Update BCSS
        diff = cluster_mean - overall_mean
        bcss += n_points * np.sum(diff * diff)
        
        # Update WCSS (within-cluster sum of squares)
        diffs = cluster_points - cluster_mean
        wcss += np.sum(diffs * diffs)
    
    # Avoid division by zero
    if wcss == 0:
        return 0.0
        
    # Calculate CH score
    ch_score = (bcss / (n_clusters - 1)) / (wcss / (n_samples - n_clusters))
    return ch_score

def calculate_adjusted_rand_index(labels_true, labels_pred):
    """Calculate Adjusted Rand Index without sklearn"""
    # Convert target to cluster labels using binning
    unique_labels = np.unique(labels_pred[labels_pred != -1])
    n_clusters = len(unique_labels)
    
    if n_clusters <= 1:
        return 0.0
    
    # Create bins based on target values
    sorted_vals = np.sort(labels_true)
    bin_edges = np.linspace(sorted_vals[0], sorted_vals[-1], n_clusters + 1)
    labels_binned = np.digitize(labels_true, bin_edges[:-1]) - 1
    
    # Create contingency matrix
    contingency = np.zeros((n_clusters, n_clusters), dtype=int)
    mask = labels_pred != -1  # Exclude noise points
    
    for i in range(len(labels_pred)):
        if mask[i]:
            contingency[labels_binned[i], labels_pred[i]] += 1
    
    # Calculate RI components
    n_samples = np.sum(contingency)
    a = np.sum(contingency * (contingency - 1)) / 2
    
    row_sums = np.sum(contingency, axis=1)
    col_sums = np.sum(contingency, axis=0)
    
    b = np.sum(row_sums * (row_sums - 1)) / 2
    c = np.sum(col_sums * (col_sums - 1)) / 2
    d = n_samples * (n_samples - 1) / 2
    
    # Expected index
    expected_index = (b * c) / d
    max_index = (b + c) / 2
    
    if max_index == expected_index:
        return 0.0
    
    # Calculate ARI
    ari = (a - expected_index) / (max_index - expected_index)
    return ari

def calculate_mutual_information(labels_true, labels_pred):
    """Calculate Mutual Information without sklearn"""
    # Convert target to cluster labels using binning
    unique_labels = np.unique(labels_pred[labels_pred != -1])
    n_clusters = len(unique_labels)
    
    if n_clusters <= 1:
        return 0.0
    
    # Create bins based on target values
    sorted_vals = np.sort(labels_true)
    bin_edges = np.linspace(sorted_vals[0], sorted_vals[-1], n_clusters + 1)
    labels_binned = np.digitize(labels_true, bin_edges[:-1]) - 1
    
    # Calculate contingency matrix
    contingency = np.zeros((n_clusters, n_clusters))
    mask = labels_pred != -1
    
    for i in range(len(labels_pred)):
        if mask[i]:
            contingency[labels_binned[i], labels_pred[i]] += 1
    
    # Calculate mutual information
    n_samples = np.sum(contingency)
    mi = 0.0
    
    for i in range(contingency.shape[0]):
        for j in range(contingency.shape[1]):
            if contingency[i, j] > 0:
                p_ij = contingency[i, j] / n_samples
                p_i = np.sum(contingency[i, :]) / n_samples
                p_j = np.sum(contingency[:, j]) / n_samples
                mi += p_ij * np.log2(p_ij / (p_i * p_j))
    
    return mi

def calculate_inertia(X, labels):
    """Calculate the sum of squared distances of samples to their closest cluster center"""
    unique_labels = np.unique(labels[labels != -1])
    inertia = 0.0
    
    for label in unique_labels:
        cluster_points = X[labels == label]
        if len(cluster_points) > 0:
            centroid = np.mean(cluster_points, axis=0)
            inertia += np.sum((cluster_points - centroid) ** 2)
    
    return inertia

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

def calculate_bootstrap_statistics(X, target, dbscan, n_bootstrap=100, confidence_level=0.95):
    """
    Perform bootstrap analysis of DBSCAN clustering results.
    
    Parameters:
    -----------
    X : array-like
        Input data matrix
    target : array-like
        Target values for external validation
    dbscan : CudaDBSCAN instance
        Configured DBSCAN clusterer
    n_bootstrap : int
        Number of bootstrap samples
    confidence_level : float
        Confidence level for intervals (default: 0.95)
    
    Returns:
    --------
    dict
        Dictionary containing statistical measures for each metric
    """
    n_samples = X.shape[0]
    alpha = 1 - confidence_level
    
    # Initialize arrays to store bootstrap results
    bootstrap_results = {
        'silhouette': [],
        'calinski_harabasz': [],
        'inertia': [],
        'ari': [],
        'mi': [],
        'n_clusters': [],
        'noise_ratio': []
    }
    
    # Perform bootstrap resampling
    for _ in range(n_bootstrap):
        # Generate bootstrap sample
        indices = np.random.choice(n_samples, size=n_samples, replace=True)
        X_bootstrap = X[indices]
        target_bootstrap = target[indices]
        
        # Fit DBSCAN and calculate metrics
        dbscan.fit(X_bootstrap)
        labels = dbscan.labels_
        
        # Store results
        bootstrap_results['silhouette'].append(
            calculate_silhouette_cuda(X_bootstrap, labels))
        bootstrap_results['calinski_harabasz'].append(
            calculate_calinski_harabasz(X_bootstrap, labels))
        bootstrap_results['inertia'].append(
            calculate_inertia(X_bootstrap, labels))
        bootstrap_results['ari'].append(
            calculate_adjusted_rand_index(target_bootstrap, labels))
        bootstrap_results['mi'].append(
            calculate_mutual_information(target_bootstrap, labels))
        bootstrap_results['n_clusters'].append(
            len(np.unique(labels[labels != -1])))
        bootstrap_results['noise_ratio'].append(
            np.sum(labels == -1) / len(labels))
    
    # Calculate statistics
    stats = {}
    for metric, values in bootstrap_results.items():
        values = np.array(values)
        
        # Calculate basic statistics
        mean = np.mean(values)
        std = np.std(values)
        
        # Calculate confidence intervals
        sorted_values = np.sort(values)
        lower_idx = int(np.floor(n_bootstrap * (alpha/2)))
        upper_idx = int(np.ceil(n_bootstrap * (1 - alpha/2))) - 1
        ci_lower = sorted_values[lower_idx]
        ci_upper = sorted_values[upper_idx]
        
        stats[metric] = {
            'mean': mean,
            'std': std,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'bootstrap_values': values  # Store the bootstrap values for plotting
        }
    
    return stats

def print_statistical_analysis(stats):
    """
    Print formatted statistical analysis results.
    
    Parameters:
    -----------
    stats : dict
        Dictionary containing statistical measures for each metric
    """
    print("\nStatistical Analysis Results:")
    print("-" * 80)
    
    metrics_names = {
        'silhouette': 'Silhouette Score',
        'calinski_harabasz': 'Calinski-Harabasz Score',
        'inertia': 'Inertia',
        'ari': 'Adjusted Rand Index',
        'mi': 'Mutual Information',
        'n_clusters': 'Number of Clusters',
        'noise_ratio': 'Noise Ratio'
    }
    
    for metric, name in metrics_names.items():
        metric_stats = stats[metric]
        print(f"\n{name}:")
        print(f"  Mean ± Std: {metric_stats['mean']:.3f} ± {metric_stats['std']:.3f}")
        print(f"  95% CI: [{metric_stats['ci_lower']:.3f}, {metric_stats['ci_upper']:.3f}]")

def plot_bootstrap_distributions(stats):
    """
    Create visualization of bootstrap distributions for each metric.
    
    Parameters:
    -----------
    stats : dict
        Dictionary containing statistical measures for each metric
    """
    metrics = list(stats.keys())
    n_metrics = len(metrics)
    
    # Create subplot grid
    n_rows = (n_metrics + 1) // 2
    fig, axes = plt.subplots(n_rows, 2, figsize=(15, 4*n_rows))
    if n_rows == 1:
        axes = np.array([axes])  # Ensure axes is always 2D
    axes = axes.flatten()
    
    metric_names = {
        'silhouette': 'Silhouette Score',
        'calinski_harabasz': 'Calinski-Harabasz Score',
        'inertia': 'Inertia',
        'ari': 'Adjusted Rand Index',
        'mi': 'Mutual Information',
        'n_clusters': 'Number of Clusters',
        'noise_ratio': 'Noise Ratio'
    }
    
    for i, metric in enumerate(metrics):
        metric_stats = stats[metric]
        
        # Create histogram
        values = metric_stats['bootstrap_values']
        axes[i].hist(values, bins=30, density=True, alpha=0.6, color='blue')
        
        # Add mean and CI lines
        axes[i].axvline(metric_stats['mean'], color='red', linestyle='--',
                       label=f"Mean: {metric_stats['mean']:.3f}")
        axes[i].axvline(metric_stats['ci_lower'], color='green', linestyle=':',
                       label=f"95% CI: [{metric_stats['ci_lower']:.3f}, {metric_stats['ci_upper']:.3f}]")
        axes[i].axvline(metric_stats['ci_upper'], color='green', linestyle=':')
        
        # Customize plot
        metric_name = metric_names.get(metric, metric)
        axes[i].set_title(f"Bootstrap Distribution: {metric_name}")
        axes[i].set_xlabel("Value")
        axes[i].set_ylabel("Density")
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)
    
    # Remove empty subplots if any
    for i in range(len(metrics), len(axes)):
        fig.delaxes(axes[i])
    
    plt.tight_layout()
    plt.show()


class LimeExplainer:
    def __init__(self, kernel_width=0.75, n_samples=5000):
        self.kernel_width = kernel_width
        self.n_samples = n_samples
    
    def _generate_perturbed_samples(self, instance, X, n_features):
        """Generate perturbed samples with improved stability"""
        # Calculate robust statistics
        q1 = np.percentile(X, 25, axis=0)
        q3 = np.percentile(X, 75, axis=0)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        # Initialize arrays
        perturbed_samples = np.zeros((self.n_samples, n_features))
        perturbation_matrix = np.random.binomial(1, 0.5, (self.n_samples, n_features))
        
        for i in range(self.n_samples):
            for j in range(n_features):
                if perturbation_matrix[i, j]:
                    # Keep original value
                    perturbed_samples[i, j] = instance[j]
                else:
                    # Sample uniformly within bounds
                    perturbed_samples[i, j] = np.random.uniform(
                        lower_bound[j], upper_bound[j]
                    )
        
        return perturbed_samples, perturbation_matrix
    
    def _compute_distances(self, perturbed_samples, instance):
        """Compute distances with normalized features"""
        # Normalize the differences
        diff = perturbed_samples - instance
        std = np.std(diff, axis=0) + 1e-8  # Add small constant for stability
        normalized_diff = diff / std
        
        # Compute Euclidean distances
        distances = np.sqrt(np.sum(normalized_diff ** 2, axis=1))
        
        # Apply kernel with adaptive width
        median_dist = np.median(distances)
        kernel_width = self.kernel_width * median_dist if median_dist > 0 else self.kernel_width
        weights = np.sqrt(np.exp(-(distances ** 2) / kernel_width ** 2))
        
        return weights
    
    def _fit_local_linear_model(self, perturbation_matrix, predictions, weights):
        """Fit weighted linear model with ridge regression"""
        # Center and scale the features
        X_mean = np.mean(perturbation_matrix, axis=0)
        X_std = np.std(perturbation_matrix, axis=0) + 1e-8
        X_scaled = (perturbation_matrix - X_mean) / X_std
        
        # Center the predictions
        y_mean = np.mean(predictions)
        y_centered = predictions - y_mean
        
        # Set up the weighted ridge regression
        alpha = 0.01  # Ridge regularization strength
        sample_weight = weights / np.sum(weights)
        
        # Compute the weighted covariance matrix
        weighted_cov = np.dot(X_scaled.T * sample_weight, X_scaled)
        weighted_corr = np.dot(X_scaled.T * sample_weight, y_centered)
        
        # Add ridge penalty and solve
        n_features = perturbation_matrix.shape[1]
        identity = np.eye(n_features)
        coefficients = np.linalg.solve(weighted_cov + alpha * identity, weighted_corr)
        
        # Transform coefficients back to original scale
        coefficients = coefficients / X_std
        intercept = y_mean - np.dot(X_mean, coefficients)
        
        # Standardize coefficient magnitudes
        coef_norm = np.linalg.norm(coefficients)
        if coef_norm > 0:
            coefficients = coefficients / coef_norm
        
        return coefficients, intercept
    
    def explain_instance(self, instance, dbscan, X, feature_names=None):
        """Generate explanation with improved stability and interpretability"""
        n_features = len(instance)
        if feature_names is None:
            feature_names = [f'feature_{i}' for i in range(n_features)]
        
        # Generate perturbed samples
        perturbed_samples, perturbation_matrix = self._generate_perturbed_samples(
            instance, X, n_features)
        
        # Create temporary DBSCAN with same parameters
        temp_dbscan = CudaDBSCAN(eps=dbscan.eps, min_samples=dbscan.min_samples)
        perturbed_labels = temp_dbscan.fit(perturbed_samples).labels_
        
        # Find nearest neighbors for robust cluster assignment
        k = min(5, len(X) - 1)  # Use up to 5 nearest neighbors
        distances = np.sqrt(np.sum((X - instance) ** 2, axis=1))
        nearest_indices = np.argsort(distances)[:k]
        instance_label = np.median(dbscan.labels_[nearest_indices])  # Use median label
        
        # Calculate similarity-based predictions instead of binary
        predictions = np.zeros(len(perturbed_labels))
        for i, label in enumerate(perturbed_labels):
            if label == instance_label:
                predictions[i] = 1.0
            elif label == -1 or instance_label == -1:
                predictions[i] = 0.0
            else:
                # Calculate similarity between clusters
                cluster_points = X[dbscan.labels_ == instance_label]
                perturbed_point = perturbed_samples[i]
                dist_to_cluster = np.min(np.sqrt(np.sum((cluster_points - perturbed_point) ** 2, axis=1)))
                predictions[i] = np.exp(-dist_to_cluster / dbscan.eps)
        
        # Compute distances and fit local model
        weights = self._compute_distances(perturbed_samples, instance)
        coefficients, intercept = self._fit_local_linear_model(
            perturbation_matrix, predictions, weights)
        
        # Scale coefficients for interpretability
        coef_scale = np.abs(coefficients).max()
        if coef_scale > 0:
            coefficients = coefficients / coef_scale
        
        # Create explanation dictionary
        explanation = {
            'feature_importance': dict(zip(feature_names, coefficients)),
            'intercept': intercept,
            'predicted_cluster': int(instance_label),
            'local_reliability': np.mean(weights),
            'prediction_confidence': np.mean(predictions)
        }
        
        # Add cluster-specific information
        if instance_label != -1:
            cluster_points = X[dbscan.labels_ == instance_label]
            if len(cluster_points) > 0:
                cluster_center = np.median(cluster_points, axis=0)  # Use median for robustness
                explanation.update({
                    'cluster_size': len(cluster_points),
                    'cluster_center': cluster_center,
                    'cluster_std': np.std(cluster_points, axis=0),
                    'distance_to_center': np.sqrt(np.sum((instance - cluster_center) ** 2))
                })
        
        return explanation

def plot_lime_explanation(explanation, max_features=10):
    """Enhanced visualization of LIME explanation"""
    import matplotlib.pyplot as plt
    
    # Sort features by absolute importance
    feature_importance = explanation['feature_importance']
    sorted_features = sorted(feature_importance.items(), 
                           key=lambda x: abs(x[1]), 
                           reverse=True)[:max_features]
    
    features, importance = zip(*sorted_features)
    
    # Create figure with appropriate size
    plt.figure(figsize=(12, 6))
    
    # Create horizontal bar plot
    y_pos = np.arange(len(features))
    colors = ['red' if imp < 0 else 'blue' for imp in importance]
    
    # Plot bars with enhanced style
    bars = plt.barh(y_pos, importance, color=colors, alpha=0.6)
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        label_x = width + 0.001 if width >= 0 else width - 0.001
        plt.text(label_x, bar.get_y() + bar.get_height()/2, 
                f'{importance[i]:.3f}',
                va='center', ha='left' if width >= 0 else 'right')
    
    # Customize plot
    plt.yticks(y_pos, features)
    plt.xlabel('Feature Importance')
    
    # Set title based on cluster
    cluster_label = "Noise" if explanation["predicted_cluster"] == -1 else f'Cluster {explanation["predicted_cluster"]}'
    plt.title(f'LIME Explanation for {cluster_label}')
    
    # Add information box
    info_text = []
    if 'cluster_size' in explanation:
        info_text.extend([
            f'Cluster Size: {explanation["cluster_size"]}',
            f'Distance to Center: {explanation["distance_to_center"]:.3f}'
        ])
    info_text.extend([
        f'Local Reliability: {explanation["local_reliability"]:.3f}',
        f'Prediction Confidence: {explanation["prediction_confidence"]:.3f}'
    ])
    
    plt.text(0.95, 0.05, '\n'.join(info_text),
            transform=plt.gca().transAxes,
            verticalalignment='bottom',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    # Add grid for better readability
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def explain_clustering(X, dbscan, feature_names=None, n_explanations=5):
    """Generate explanations for multiple instances"""
    explainer = LimeExplainer(n_samples=5000)  # Increased number of samples
    
    # Get unique labels including noise
    unique_labels = np.unique(dbscan.labels_)
    
    for label in unique_labels:
        # Get points for this cluster/noise
        mask = dbscan.labels_ == label
        cluster_points = X[mask]
        
        if len(cluster_points) == 0:
            continue
        
        # Select instance closest to cluster center for more representative explanation
        if label != -1:
            center = np.median(cluster_points, axis=0)
            distances = np.sqrt(np.sum((cluster_points - center) ** 2, axis=1))
            idx = np.argmin(distances)
        else:
            # For noise points, select random instance
            idx = np.random.randint(len(cluster_points))
        
        instance = cluster_points[idx]
        
        # Generate and plot explanation
        explanation = explainer.explain_instance(instance, dbscan, X, feature_names)
        plot_lime_explanation(explanation)
        
        # Print detailed explanation
        cluster_type = 'Noise' if label == -1 else f'Cluster {label}'
        print(f"\nDetailed Explanation for Instance in {cluster_type}:")
        print("-" * 50)
        
        if 'cluster_size' in explanation:
            print(f"Cluster Size: {explanation['cluster_size']}")
            print(f"Distance to Cluster Center: {explanation['distance_to_center']:.3f}")
        
        print(f"Local Reliability Score: {explanation['local_reliability']:.3f}")
        print(f"Prediction Confidence: {explanation['prediction_confidence']:.3f}")
        print("\nFeature Contributions:")
        
        for feature, importance in sorted(
            explanation['feature_importance'].items(),
            key=lambda x: abs(x[1]),
            reverse=True
        ):
            print(f"{feature}: {importance:.3f}")
        print("-" * 50)

def main():
    # Load and preprocess data
    df = pd.read_csv("./housing.csv")
    df, target = preprocess(df, "median_house_value")
    target = target.to_numpy()
    X = df.to_numpy()
    X = scale(X)

    # Parameter analysis
    print("Analyzing optimal eps parameter...")
    suggested_eps = plot_kdistance(X, k=4)
    print(f"Suggested eps value: {suggested_eps:.3f}")

    print("\nAnalyzing optimal minPoints parameter...")
    optimal_minpoints, dimension_based = plot_minpoints_analysis(X, suggested_eps, CudaDBSCAN)
    print(f"\nResults:")
    print(f"Dimension-based recommendation: {dimension_based}")
    print(f"Optimal minPoints from stability analysis: {optimal_minpoints}")
    
    # Initial DBSCAN clustering
    print("\nRunning CUDA DBSCAN with suggested parameters...")
    dbscan = CudaDBSCAN(eps=suggested_eps, min_samples=optimal_minpoints)
    dbscan.fit(X)
    labels = dbscan.labels_
    
    # Calculate initial metrics
    n_clusters = len(np.unique(labels[labels != -1]))
    silhouette = calculate_silhouette_cuda(X, labels)
    ch_score = calculate_calinski_harabasz(X, labels)
    inertia = calculate_inertia(X, labels)
    ari = calculate_adjusted_rand_index(target, labels)
    mi = calculate_mutual_information(target, labels)
    noise_ratio = np.sum(labels == -1) / len(labels)
    
    # Print initial results
    print("\nInitial Clustering Results:")
    print("-" * 40)
    print(f"Number of clusters: {n_clusters}")
    print(f"Silhouette Score: {silhouette:.3f}")
    print(f"Calinski-Harabasz Score: {ch_score:.3f}")
    print(f"Inertia: {inertia:.3f}")
    print(f"Adjusted Rand Index: {ari:.3f}")
    print(f"Mutual Information: {mi:.3f}")
    print(f"Noise ratio: {noise_ratio:.3f}")
    print("\nGenerating LIME explanations...")
    feature_names = ['latitude', 'median_income', 'total_rooms', 'ocean_proximity']
    explain_clustering(X, dbscan, feature_names=feature_names, n_explanations=3)

    # Perform statistical analysis
    print("\nPerforming bootstrap analysis...")
    stats = calculate_bootstrap_statistics(
        X=X,
        target=target,
        dbscan=dbscan,
        n_bootstrap=10,
        confidence_level=0.95
    )
    
    # Print statistical analysis results
    print_statistical_analysis(stats)
    
    # Create visualization of bootstrap distributions
    plot_bootstrap_distributions(stats)
    
    plt.show()  # Make sure all plots are displayed

if __name__ == "__main__":
    main()
