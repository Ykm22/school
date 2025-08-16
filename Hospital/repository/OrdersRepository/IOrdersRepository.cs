using System.Collections.Generic;
using model;

namespace repository.OrdersRepository
{
    public interface IOrdersRepository<in TId, TE> : IRepository<TId, TE> where TE : Identifiable
    {
        IEnumerable<Order> FilterByStatus(OrderStatus orderStatus);
        void AddOrderMedicines(IList<OrderMedicine> orderMedicines);
        Order UpdateStatus(int orderId, OrderStatus orderStatus);
        List<Order> FindOrdersByMedicalStaffId(int medicalStaffId);
    }
}