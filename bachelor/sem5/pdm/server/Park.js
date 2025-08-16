class Park {
    constructor({id, description, squared_kms, last_review, reaches_eco_target}){
        this.id = id;
        this.description = description;
        this.squared_kms = squared_kms;
        this.last_review = last_review;
        this.reaches_eco_target = reaches_eco_target;
    }
};

module.exports = Park;
