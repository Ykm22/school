import numpy as np
import matplotlib.pyplot as plt

def calculate_silhouette(X, labels):
    """Calculate Silhouette Score"""
    n_samples = X.shape[0]
    unique_labels = np.unique(labels[labels != -1])
    
    silhouette_scores = []
    for i in range(n_samples):
        if labels[i] == -1:
            silhouette_scores.append(0)
            continue
        
        # Calculate a (mean intra-cluster distance)
        same_cluster = X[labels == labels[i]]
        if len(same_cluster) <= 1:
            silhouette_scores.append(0)
            continue
        
        a = np.mean([np.sqrt(np.sum((X[i] - point) ** 2)) 
                    for point in same_cluster if not np.array_equal(point, X[i])])
        
        # Calculate b (mean nearest-cluster distance)
        b = float('inf')
        for label in unique_labels:
            if label != labels[i]:
                other_cluster = X[labels == label]
                if len(other_cluster) > 0:
                    mean_dist = np.mean([np.sqrt(np.sum((X[i] - point) ** 2)) 
                                       for point in other_cluster])
                    b = min(b, mean_dist)
        
        if a == 0 and b == float('inf'):
            silhouette_scores.append(0)
        else:
            silhouette_scores.append((b - a) / max(a, b))
    
    return np.mean(silhouette_scores)

def calculate_stability_score(X, eps, min_samples_range):
    """Calculate clustering stability for different minPoints values"""
    stability_scores = []
    n_clusters_list = []
    noise_ratios = []
    
    def run_dbscan(min_samples):
        dbscan = StandardDBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit(X).labels_
        n_clusters = len(np.unique(labels[labels != -1]))
        noise_ratio = np.sum(labels == -1) / len(labels)
        return labels, n_clusters, noise_ratio
    
    # Calculate all results first
    results = []
    for min_samples in min_samples_range:
        labels, n_clusters, noise_ratio = run_dbscan(min_samples)
        results.append((labels, n_clusters, noise_ratio))
        n_clusters_list.append(n_clusters)
        noise_ratios.append(noise_ratio)
    
    # Calculate stability scores
    for i in range(len(min_samples_range)):
        if i == 0:
            score = np.mean(results[i][0] == results[i+1][0])
        elif i == len(min_samples_range) - 1:
            score = np.mean(results[i][0] == results[i-1][0])
        else:
            score = (np.mean(results[i][0] == results[i-1][0]) + 
                    np.mean(results[i][0] == results[i+1][0])) / 2
        stability_scores.append(score)
    
    return np.array(stability_scores), np.array(n_clusters_list), np.array(noise_ratios)

def plot_minpoints_analysis(X, eps):
    """Analyze and visualize minPoints parameter selection"""
    d = X.shape[1]
    min_samples_base = 2 * d
    
    min_samples_range = np.arange(max(2, min_samples_base - 5), 
                                 min_samples_base + 15)
    
    stability_scores, n_clusters, noise_ratios = calculate_stability_score(
        X, eps, min_samples_range)
    
    # Create visualization
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
    
    # Plot stability scores
    ax1.plot(min_samples_range, stability_scores, 'b-', label='Stability')
    ax1.axvline(x=min_samples_base, color='r', linestyle='--', 
                label=f'Dimension-based ({min_samples_base})')
    ax1.set_xlabel('minPoints')
    ax1.set_ylabel('Stability Score')
    ax1.set_title('Clustering Stability vs minPoints')
    ax1.grid(True)
    ax1.legend()
    
    # Plot number of clusters
    ax2.plot(min_samples_range, n_clusters, 'g-', label='Clusters')
    ax2.axvline(x=min_samples_base, color='r', linestyle='--',
                label=f'Dimension-based ({min_samples_base})')
    ax2.set_xlabel('minPoints')
    ax2.set_ylabel('Number of Clusters')
    ax2.set_title('Number of Clusters vs minPoints')
    ax2.grid(True)
    ax2.legend()
    
    # Plot noise ratio
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
    normalized_stability = (stability_scores - stability_scores.min()) / \
                         (stability_scores.max() - stability_scores.min())
    normalized_clusters = (n_clusters - n_clusters.min()) / \
                        (n_clusters.max() - n_clusters.min())
    
    combined_score = 0.7 * normalized_stability - 0.3 * normalized_clusters
    optimal_idx = np.argmax(combined_score)
    optimal_minpoints = min_samples_range[optimal_idx]
    
    return optimal_minpoints, min_samples_base

def calculate_calinski_harabasz(X, labels):
    """Calculate Calinski-Harabasz Index"""
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
        
        # Update WCSS
        diffs = cluster_points - cluster_mean
        wcss += np.sum(diffs * diffs)
    
    if wcss == 0:
        return 0.0
    
    ch_score = (bcss / (n_clusters - 1)) / (wcss / (n_samples - n_clusters))
    return ch_score

def calculate_adjusted_rand_index(labels_true, labels_pred):
    """Calculate Adjusted Rand Index"""
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
    mask = labels_pred != -1
    
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
    
    expected_index = (b * c) / d
    max_index = (b + c) / 2
    
    if max_index == expected_index:
        return 0.0
    
    ari = (a - expected_index) / (max_index - expected_index)
    return ari

def calculate_mutual_information(labels_true, labels_pred):
    """Calculate Mutual Information"""
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
