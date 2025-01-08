import numpy as np
from performance_measures import calculate_silhouette, calculate_mutual_information, calculate_stability_score, calculate_inertia, calculate_calinski_harabasz, calculate_adjusted_rand_index
import matplotlib.pyplot as plt

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
