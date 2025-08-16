using System;
using model;

namespace services
{
    public interface IServices : IMedicineServices, IPharmacistServices, IMedicalStaffServices, IOrderServices
    {
        Pharmacist Login(Pharmacist pharmacist, IObserver client);
        void Logout(Pharmacist pharmacist, IObserver client);
        MedicalStaff LoginMedicalStaff(MedicalStaff medicalStaff, IObserver client);
        void LogoutMedicalStaff(MedicalStaff medicalStaff, IObserver client);
    }
}