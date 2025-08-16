using model;

namespace repository.MedicalStaffRepository
{
    public interface IMedicalStaffRepository<in TId, TE> : IRepository<TId, TE> where TE : Identifiable
    {
        MedicalStaff FindByCredentials(string medicalStaffName, string medicalStaffPassword);
    }
}