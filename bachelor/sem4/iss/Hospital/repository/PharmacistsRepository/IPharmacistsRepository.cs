using model;

namespace repository.PharmacistsRepository
{
    public interface IPharmacistsRepository<in TId, TE> : IRepository<TId, TE> where TE : Identifiable
    {
        Pharmacist FindByCredentials(string pharmacistName, string pharmacistPassword);
    }
}