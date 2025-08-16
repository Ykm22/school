using System.Collections.Generic;
using model;

namespace services
{
    public interface IOrderServices
    {
        List<Order> GetIncompleteOrders();
        int AddOrder(Order order);
        void AddOrderMedicines(IList<OrderMedicine> orderMedicines);
        List<Medicine> GetOrderMedicines(int orderId);
        void UpdateOrder(int orderId, OrderStatus orderStatus);
        List<Order> GetOrdersByMedicalStaffId(int medicalStaffId);
    }
}