using System;
using System.Collections.Generic;
using System.Data.Entity.Infrastructure.Design;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using model;
using repository.MedicalStaffRepository;
using repository.MedicinesRepository;
using repository.OrdersRepository;
using repository.PharmacistsRepository;
using services;

namespace server
{
    public class Services : IServices
    {
        private IMedicinesRepository<int, Medicine> _medicinesRepository;
        private IPharmacistsRepository<int, Pharmacist> _pharmacistsRepository;
        private IMedicalStaffRepository<int, MedicalStaff> _medicalStaffRepository;
        private IOrdersRepository<int, Order> _ordersRepository;
        private readonly IDictionary<int, IObserver> LoggedClients;

        public Services(IMedicinesRepository<int, Medicine> medicinesRepository, 
            IPharmacistsRepository<int, Pharmacist> pharmacistsRepository,
            IMedicalStaffRepository<int, MedicalStaff> medicalStaffRepository,
            IOrdersRepository<int, Order> ordersRepository)
        {
            _medicinesRepository = medicinesRepository;
            _pharmacistsRepository = pharmacistsRepository;
            _medicalStaffRepository = medicalStaffRepository;
            _ordersRepository = ordersRepository;
            LoggedClients = new Dictionary<int, IObserver>();
        }

        public IEnumerable<Medicine> GetAllMedicines()
        {
            return _medicinesRepository.GetAll();
        }

        public void AddMedicine(Medicine medicine)
        {
            Medicine afterSave_Medicine = _medicinesRepository.Save(medicine);
            NotifyClients(UpdateType.AddMedicine, afterSave_Medicine);
        }

        public Medicine FindMedicine(int id)
        {
            return _medicinesRepository.Find(id);
        }

        public int AddOrder(Order order)
        {
            int orderId = _ordersRepository.Save(order).Id;
            NotifyClientsOrder(UpdateType.AddOrder, order);
            return orderId;
        }

        private void NotifyClientsOrder(UpdateType updateType, Order order)
        {
            foreach (IObserver client in LoggedClients.Values)
            {
                if (updateType == UpdateType.AddOrder)
                {
                    Task.Run(() => client.Update_AddedOrder(order));
                }
                if (updateType == UpdateType.UpdateOrder)
                {
                    Task.Run(() => client.Update_UpdatedOrder(order));
                }
            }
        }

        public List<Order> GetOrdersByMedicalStaffId(int medicalStaffId)
        {
            return _ordersRepository.FindOrdersByMedicalStaffId(medicalStaffId);
        }

        public List<Medicine> GetOrderMedicines(int orderId)
        {
            var list = _medicinesRepository.FilterByOrderId(orderId).ToList();
            // MessageBox.Show(list.Count.ToString());
            return list;
        }

        private void NotifyClients(UpdateType updateType, Medicine medicine)
        {
            // MessageBox.Show(LoggedClients.Count.ToString());
            foreach (IObserver client in LoggedClients.Values)
            {
                if (updateType == UpdateType.AddMedicine)
                {
                    Task.Run(() => client.Update_AddedMedicine(medicine));
                }

                else if (updateType == UpdateType.UpdateMedicine)
                {
                    Task.Run(() => client.Update_UpdatedMedicine(medicine));
                }
                else if (updateType == UpdateType.DeleteMedicine)
                {
                    Task.Run(() => client.Update_DeletedMedicine(medicine));
                }
            }
        }


        public void UpdateOrder(int orderId, OrderStatus orderStatus)
        {
            Order updatedOrder = _ordersRepository.UpdateStatus(orderId, orderStatus);
            // MessageBox.Show(updatedOrder.OrderStatus +  " " + updatedOrder.Id.ToString());
            NotifyClientsOrder(UpdateType.UpdateOrder, updatedOrder);
        }

        public void AddOrderMedicines(IList<OrderMedicine> orderMedicines)
        {
            _ordersRepository.AddOrderMedicines(orderMedicines);
        }

        public void UpdateMedicine(Medicine medicine, bool substract)
        {
            Medicine updatedMedicine = _medicinesRepository.Update(medicine.Id, medicine, substract);
            NotifyClients(UpdateType.UpdateMedicine, updatedMedicine);
        }

        public void DeleteMedicine(int id)
        {
            _medicinesRepository.Delete(id);
            Medicine temporary = new Medicine(Purpose.Headache, "", 0);
            temporary.SetId(id);
            NotifyClients(UpdateType.DeleteMedicine, temporary);
        }

        public IEnumerable<Medicine> FilterMedicines(Purpose purpose)
        {
            return _medicinesRepository.FindByPurpose(purpose);
        }

        public Pharmacist Login(Pharmacist pharmacist, IObserver client)
        {
            try
            {
                Pharmacist foundPharmacist = _pharmacistsRepository.FindByCredentials(pharmacist.Name, pharmacist.Password);
                if (foundPharmacist != null)
                {
                    if (LoggedClients.ContainsKey(foundPharmacist.Id))
                        throw new HospitalException("Pharmacist already locked in.");
                    LoggedClients[foundPharmacist.Id] = client;
                    return foundPharmacist;
                }
            
                throw new HospitalException("Authentication failed!");
            }
            catch (Exception e)
            {
                throw new HospitalException(e.Message);
            }
        }

        public void Logout(Pharmacist pharmacist, IObserver client)
        {
            throw new System.NotImplementedException();
        }

        public MedicalStaff FindMedicalStaffByCredentials(string medicalStaffName, string medicalStaffPassword)
        {
            MedicalStaff medicalStaff =
                _medicalStaffRepository.FindByCredentials(medicalStaffName, medicalStaffPassword);
            return medicalStaff;
        }
        public Pharmacist FindPharmacistByCredentials(string pharmacistName, string pharmacistPassword)
        {
            Pharmacist pharmacist = _pharmacistsRepository.FindByCredentials(pharmacistName, pharmacistPassword);
            return pharmacist;
        }

        public MedicalStaff LoginMedicalStaff(MedicalStaff medicalStaff, IObserver client)
        {
            try
            {
                MedicalStaff foundMedicalStaff = _medicalStaffRepository.FindByCredentials(medicalStaff.Name, medicalStaff.Password);
                if (foundMedicalStaff != null)
                {
                    if (LoggedClients.ContainsKey(foundMedicalStaff.Id))
                        throw new HospitalException("Medical staff already locked in.");
                    LoggedClients[foundMedicalStaff.Id] = client;
                    return foundMedicalStaff;
                }
            
                throw new HospitalException("Authentication failed!");
            }
            catch (Exception e)
            {
                throw new HospitalException(e.Message);
            }
        }

        public void LogoutMedicalStaff(MedicalStaff medicalStaff, IObserver client)
        {
            throw new NotImplementedException();
        }

        public List<Order> GetIncompleteOrders()
        {
            return _ordersRepository.FilterByStatus(OrderStatus.Incomplete).ToList();
        }
    }
}