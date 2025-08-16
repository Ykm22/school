using System;
using System.Collections.Generic;
using model;

namespace services
{
    public interface IMedicineServices
    {
        IEnumerable<Medicine> GetAllMedicines();
        void AddMedicine(Medicine medicine);
        void UpdateMedicine(Medicine medicine, bool substract);
        void DeleteMedicine(int id);
        IEnumerable<Medicine> FilterMedicines(Purpose purpose);
        Medicine FindMedicine(int id);
    }
}