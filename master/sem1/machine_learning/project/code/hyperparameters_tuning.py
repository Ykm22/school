import numpy as np
import matplotlib.pyplot as plt

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

def calculate_kdistances(X, k=4):
    n_samples = X.shape[0]
    k_distances = np.zeros(n_samples)
    
    for i in range(n_samples):
        distances = np.sqrt(np.sum((X - X[i])**2, axis=1))
        distances.sort()
        k_distances[i] = distances[k + 1]  # k+1 because the first one is distance to self (0)
    
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
    """Generate k-distance plot"""
    kdistances = calculate_kdistances(X, k)
    
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

