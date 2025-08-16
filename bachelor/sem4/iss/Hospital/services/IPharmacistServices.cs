using model;

namespace services
{
    public interface IPharmacistServices
    {
        Pharmacist FindPharmacistByCredentials(string pharmacistName, string pharmacistPassword);
    }
}