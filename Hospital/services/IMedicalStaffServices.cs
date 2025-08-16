using model;

namespace services
{
    public interface IMedicalStaffServices
    {
        MedicalStaff FindMedicalStaffByCredentials(string medicalStaffName, string medicalStaffPassword);
    }
}