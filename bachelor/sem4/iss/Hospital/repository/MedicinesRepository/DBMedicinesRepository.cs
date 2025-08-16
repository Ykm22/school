using System;
using System.Collections.Generic;
using System.Linq;
using model;
using NHibernate;
using NHibernate.Criterion;
using NHibernate.Transform;

namespace repository.MedicinesRepository
{
    public class DBMedicinesRepository : IMedicinesRepository<int, Medicine>
    {
        public Medicine Update(int id, Medicine entity, bool substract)
        {
            if (substract == false)
            {
                using (var session = _sessionFactory.OpenSession())
                {
                    var medicine = session.Get<Medicine>(id);
                    if (medicine != null)
                    {
                        medicine.Name = entity.Name;
                        medicine.Purpose = entity.Purpose;
                        medicine.AvailableQuantity = entity.AvailableQuantity;
                        
                        session.Update(medicine);
                        session.Flush();
                    }

                    return medicine;
                }
            }
            else
            {
                using (var session = _sessionFactory.OpenSession())
                {
                    var medicine = session.Get<Medicine>(id);
                    if (medicine != null)
                    {
                        medicine.Name = entity.Name;
                        medicine.Purpose = entity.Purpose;
                        medicine.AvailableQuantity -= entity.AvailableQuantity;
                        
                        session.Update(medicine);
                        session.Flush();
                    }

                    return medicine;
                }
            }
        }

        private ISessionFactory _sessionFactory;
        public DBMedicinesRepository(ISessionFactory sessionFactory)
        {
            _sessionFactory = sessionFactory;
        }

        public Medicine Save(Medicine entity)
        {
            using (var session = _sessionFactory.OpenSession())
            {
                session.Save(entity);
            }

            return entity;
        }

        public IEnumerable<Medicine> FilterByOrderId(int orderId)
        {
            IList<Medicine> medicines_quantity = new List<Medicine>();
            using (var session = _sessionFactory.OpenSession())
            {
                var result = session.Query<OrderMedicine>()
                    .Where(om => om.orderId == orderId)
                    .Select(om => new { om.medicineId, om.Quantity })
                    .ToList();

                foreach (var item in result)
                {
                    int medicineId = item.medicineId;
                    int quantity = item.Quantity;

                    Medicine medicine = session.Query<Medicine>()
                        .FirstOrDefault(m => m.Id == medicineId);
                    medicine.AvailableQuantity = quantity;
                    medicines_quantity.Add(medicine);
                }
                
                return medicines_quantity;
            }
        }

        public Medicine Delete(int id)
        {
            using (var session = _sessionFactory.OpenSession())
            {
                using (var transaction = session.BeginTransaction())
                {
                    var medicine = session.Get<Medicine>(id);
                    if (medicine != null)
                    {
                        session.Delete(medicine);
                    }
                    transaction.Commit();
                    return medicine;
                }
                
            }
        }

        public IEnumerable<Medicine> GetAll()
        {
            using (var session = _sessionFactory.OpenSession())
            {
                ICriteria criteria = session.CreateCriteria(typeof(Medicine));
                IList<Medicine> medicines = criteria.List<Medicine>();
                return medicines;
            }
        }

        public IEnumerable<Medicine> FindByPurpose(Purpose purpose)
        {
            using (var session = _sessionFactory.OpenSession())
            {
                return session.Query<Medicine>()
                    .Where(m => m.Purpose == purpose)
                    .ToList();
            }
        }

        public Medicine Find(int id)
        {
            using (var session = _sessionFactory.OpenSession())
            {
                return session.Query<Medicine>()
                    .FirstOrDefault(m => m.Id == id);
            }
        }

        public Medicine Update(int id, Medicine entity)
        {
            using (var session = _sessionFactory.OpenSession())
            {
                var medicine = session.Get<Medicine>(id);
                if (medicine != null)
                {
                    medicine.Name = entity.Name;
                    medicine.Purpose = entity.Purpose;
                    medicine.AvailableQuantity = entity.AvailableQuantity;
                    
                    session.Update(medicine);
                    session.Flush();
                }

                return medicine;
            }
        }
    }
}