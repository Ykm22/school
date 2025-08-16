using System.Threading.Tasks;
using model;

namespace services
{
    public interface IObserver
    {
        // todo
        void Update_AddedMedicine(Medicine medicine);
        void Update_UpdatedMedicine(Medicine medicine);
        void Update_DeletedMedicine(Medicine medicine);
        void Update_AddedOrder(Order order);
        void Update_UpdatedOrder(Order order);
    }
}