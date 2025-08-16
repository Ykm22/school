function perturbed_coefficients = perturbateCoefficientsUniform(coefficients, mu, variance)
    lower_bound = mu - sqrt(3)*sqrt(variance);
    upper_bound = mu + sqrt(3)*sqrt(variance);
    
    perturbations = unifrnd(lower_bound, upper_bound, size(coefficients));
    perturbed_coefficients = coefficients + perturbations;
end