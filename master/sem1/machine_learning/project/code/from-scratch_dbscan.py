import numpy as np
import pandas as pd
from LimeExplainer import LimeExplainer, explain_clustering
from DBSCAN import StandardDBSCAN
from performance_measures import calculate_silhouette, calculate_mutual_information, calculate_stability_score, calculate_inertia, calculate_calinski_harabasz, calculate_adjusted_rand_index
from hyperparameters_tuning import plot_minpoints_analysis, plot_kdistance
from preprocessing import preprocess, scale
from statistics import calculate_bootstrap_statistics, print_statistical_analysis, plot_bootstrap_distributions

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
    optimal_minpoints, dimension_based = plot_minpoints_analysis(X, suggested_eps)
    print(f"\nResults:")
    print(f"Dimension-based recommendation: {dimension_based}")
    print(f"Optimal minPoints from stability analysis: {optimal_minpoints}")
    
    # Run clustering
    print("\nRunning DBSCAN with suggested parameters...")
    dbscan = StandardDBSCAN(eps=suggested_eps, min_samples=optimal_minpoints)
    dbscan.fit(X)
    labels = dbscan.labels_
    
    # Calculate metrics
    n_clusters = len(np.unique(labels[labels != -1]))
    silhouette = calculate_silhouette(X, labels)
    ch_score = calculate_calinski_harabasz(X, labels)
    inertia = calculate_inertia(X, labels)
    ari = calculate_adjusted_rand_index(target, labels)
    mi = calculate_mutual_information(target, labels)
    noise_ratio = np.sum(labels == -1) / len(labels)
    
    # Print results
    print("\nClustering Results:")
    print("-" * 40)
    print(f"Number of clusters: {n_clusters}")
    print(f"Silhouette Score: {silhouette:.3f}")
    print(f"Calinski-Harabasz Score: {ch_score:.3f}")
    print(f"Inertia: {inertia:.3f}")
    print(f"Adjusted Rand Index: {ari:.3f}")
    print(f"Mutual Information: {mi:.3f}")
    print(f"Noise ratio: {noise_ratio:.3f}")
    
    # Generate LIME explanations
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
