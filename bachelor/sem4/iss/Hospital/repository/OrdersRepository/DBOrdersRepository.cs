using System.Collections.Generic;
using System.Linq;
using model;
using NHibernate;

namespace repository.OrdersRepository
{
    public class DBOrdersRepository : IOrdersRepository<int, Order>
    {
        public Order UpdateStatus(int orderId, OrderStatus orderStatus)
        {
            using (var session = _sessionFactory.OpenSession())
            {
                var order = session.Get<Order>(orderId);
                if (order != null)
                {
                    // Update the order status
                    order.OrderStatus = orderStatus;

                    // Save the changes
                    using (var transaction = session.BeginTransaction())
                    {
                        session.Update(order);
                        transaction.Commit();
                    }
                }

                return order;
            }
        }

        public List<Order> FindOrdersByMedicalStaffId(int medicalStaffId)
        {
            using (var session = _sessionFactory.OpenSession())
            {
                var orders = session.Query<Order>()
                    .Where(o => o.medicalStaffId == medicalStaffId)
                    .ToList();
                return orders;
            }
        }

        public Order Update(int id, Order entity, bool substract)
        {
            throw new System.NotImplementedException();
        }

        private ISessionFactory _sessionFactory;
        
        public DBOrdersRepository(ISessionFactory sessionFactory)
        {
            _sessionFactory = sessionFactory;
        }
        public Order Save(Order entity)
        {
            using (var session = _sessionFactory.OpenSession())
            {
                session.Save(entity);
            }

            return entity;
        }

        public void AddOrderMedicines(IList<OrderMedicine> orderMedicines)
        {
            using (var session = _sessionFactory.OpenSession()) {
                // Set the OrderId for each OrderMedicine item and save them in the database
                using (var transaction = session.BeginTransaction())
                {
                    foreach (var orderMedicine in orderMedicines)
                    {
                        session.Save(orderMedicine);
                    }

                    transaction.Commit();
                }
            }
        }

        public Order Delete(int id)
        {
            throw new System.NotImplementedException();
        }

        public IEnumerable<Order> GetAll()
        {
            throw new System.NotImplementedException();
        }

        public Order Find(int id)
        {
            throw new System.NotImplementedException();
        }

        public Order Update(int id, Order entity)
        {
            throw new System.NotImplementedException();
        }

        public IEnumerable<Order> FilterByStatus(OrderStatus orderStatus)
        {
            using (var session = _sessionFactory.OpenSession())
            {
                var orders = session.Query<Order>()
                    .Where(o => o.OrderStatus == orderStatus)
                    .ToList();

                return orders;
            }
        }
    }
}