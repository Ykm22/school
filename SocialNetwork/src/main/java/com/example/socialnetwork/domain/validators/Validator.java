package com.example.socialnetwork.domain.validators;

public interface Validator<E> {
    /**
     * Validates an entity
     * @param entity to validate
     * @throws ValidationException if entity is invalid
     */
    public void validate(E entity) throws ValidationException;
}
