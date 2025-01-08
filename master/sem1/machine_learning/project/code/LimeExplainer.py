import numpy as np
import matplotlib.pyplot as plt

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
                    perturbed_samples[i, j] = instance[j]
                else:
                    perturbed_samples[i, j] = np.random.uniform(
                        lower_bound[j], upper_bound[j]
                    )
        
        return perturbed_samples, perturbation_matrix
    
    def _compute_distances(self, perturbed_samples, instance):
        """Compute distances with normalized features"""
        diff = perturbed_samples - instance
        std = np.std(diff, axis=0) + 1e-8
        normalized_diff = diff / std
        
        distances = np.sqrt(np.sum(normalized_diff ** 2, axis=1))
        
        median_dist = np.median(distances)
        kernel_width = self.kernel_width * median_dist if median_dist > 0 else self.kernel_width
        weights = np.sqrt(np.exp(-(distances ** 2) / kernel_width ** 2))
        
        return weights
    
    def _fit_local_linear_model(self, perturbation_matrix, predictions, weights):
        """Fit weighted linear model with ridge regression"""
        X_mean = np.mean(perturbation_matrix, axis=0)
        X_std = np.std(perturbation_matrix, axis=0) + 1e-8
        X_scaled = (perturbation_matrix - X_mean) / X_std
        
        y_mean = np.mean(predictions)
        y_centered = predictions - y_mean
        
        alpha = 0.01  # Ridge regularization strength
        sample_weight = weights / np.sum(weights)
        
        weighted_cov = np.dot(X_scaled.T * sample_weight, X_scaled)
        weighted_corr = np.dot(X_scaled.T * sample_weight, y_centered)
        
        n_features = perturbation_matrix.shape[1]
        identity = np.eye(n_features)
        coefficients = np.linalg.solve(weighted_cov + alpha * identity, weighted_corr)
        
        coefficients = coefficients / X_std
        intercept = y_mean - np.dot(X_mean, coefficients)
        
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
        temp_dbscan = StandardDBSCAN(eps=dbscan.eps, min_samples=dbscan.min_samples)
        perturbed_labels = temp_dbscan.fit(perturbed_samples).labels_
        
        # Find nearest neighbors for robust cluster assignment
        k = min(5, len(X) - 1)
        distances = np.sqrt(np.sum((X - instance) ** 2, axis=1))
        nearest_indices = np.argsort(distances)[:k]
        instance_label = int(np.median(dbscan.labels_[nearest_indices]))
        
        # Calculate similarity-based predictions
        predictions = np.zeros(len(perturbed_labels))
        for i, label in enumerate(perturbed_labels):
            if label == instance_label:
                predictions[i] = 1.0
            elif label == -1 or instance_label == -1:
                predictions[i] = 0.0
            else:
                cluster_points = X[dbscan.labels_ == instance_label]
                perturbed_point = perturbed_samples[i]
                dist_to_cluster = np.min(np.sqrt(np.sum((cluster_points - perturbed_point) ** 2, axis=1)))
                predictions[i] = np.exp(-dist_to_cluster / dbscan.eps)
        
        # Compute distances and fit local model
        weights = self._compute_distances(perturbed_samples, instance)
        coefficients, intercept = self._fit_local_linear_model(
            perturbation_matrix, predictions, weights)
        
        # Create explanation dictionary
        explanation = {
            'feature_importance': dict(zip(feature_names, coefficients)),
            'intercept': intercept,
            'predicted_cluster': instance_label,
            'local_reliability': np.mean(weights),
            'prediction_confidence': np.mean(predictions)
        }
        
        if instance_label != -1:
            cluster_points = X[dbscan.labels_ == instance_label]
            if len(cluster_points) > 0:
                cluster_center = np.median(cluster_points, axis=0)
                explanation.update({
                    'cluster_size': len(cluster_points),
                    'cluster_center': cluster_center,
                    'cluster_std': np.std(cluster_points, axis=0),
                    'distance_to_center': np.sqrt(np.sum((instance - cluster_center) ** 2))
                })
        
        return explanation

def plot_lime_explanation(explanation, max_features=10):
    """Visualize LIME explanation"""
    feature_importance = explanation['feature_importance']
    sorted_features = sorted(feature_importance.items(), 
                           key=lambda x: abs(x[1]), 
                           reverse=True)[:max_features]
    
    features, importance = zip(*sorted_features)
    
    plt.figure(figsize=(12, 6))
    y_pos = np.arange(len(features))
    colors = ['red' if imp < 0 else 'blue' for imp in importance]
    bars = plt.barh(y_pos, importance, color=colors, alpha=0.6)
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        label_x = width + 0.001 if width >= 0 else width - 0.001
        plt.text(label_x, bar.get_y() + bar.get_height()/2, 
                f'{importance[i]:.3f}',
                va='center', ha='left' if width >= 0 else 'right')
    
    plt.yticks(y_pos, features)
    plt.xlabel('Feature Importance')
    
    cluster_label = "Noise" if explanation["predicted_cluster"] == -1 else f'Cluster {explanation["predicted_cluster"]}'
    plt.title(f'LIME Explanation for {cluster_label}')
    
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
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def explain_clustering(X, dbscan, feature_names=None, n_explanations=5):
    """Generate explanations for multiple instances"""
    explainer = LimeExplainer(n_samples=5000)
    unique_labels = np.unique(dbscan.labels_)
    
    for label in unique_labels:
        mask = dbscan.labels_ == label
        cluster_points = X[mask]
        
        if len(cluster_points) == 0:
            continue
        
        if label != -1:
            center = np.median(cluster_points, axis=0)
            distances = np.sqrt(np.sum((cluster_points - center) ** 2, axis=1))
            idx = np.argmin(distances)
        else:
            idx = np.random.randint(len(cluster_points))
        
        instance = cluster_points[idx]
        explanation = explainer.explain_instance(instance, dbscan, X, feature_names)
        plot_lime_explanation(explanation)
        
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

