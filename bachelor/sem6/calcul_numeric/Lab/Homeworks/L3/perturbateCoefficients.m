function perturbed_coefficients = perturbateCoefficients(coefficients, mu, variance)
    perturbations = normrnd(mu, sqrt(variance), size(coefficients));
    perturbed_coefficients = coefficients + perturbations;
end