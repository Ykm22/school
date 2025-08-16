using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Windows.Forms;
using model;
using services;

namespace client
{
    public class PharmacyController : IObserver
    {
        public event EventHandler<UserEventArgs> updateEvent;
        private readonly IServices server;
        private Pharmacist loggedPharmacist;

        public PharmacyController(IServices server)
        {
            this.server = server;
            loggedPharmacist = null;
        }
        public Pharmacist Login(Pharmacist pharmacist)
        {
            loggedPharmacist = server.Login(pharmacist, this);
            Console.WriteLine("Current user {0}", loggedPharmacist);
            return loggedPharmacist;
        }
        public void Update_AddedMedicine(Medicine addedMedicine)
        {
            UserEventArgs userArgs = new UserEventArgs(UserEvent.Update_AddedMedicine, addedMedicine);
            OnUserEvent(userArgs);
        }
        public void Update_UpdatedMedicine(Medicine updatedMedicine)
        {
            UserEventArgs userArgs = new UserEventArgs(UserEvent.Update_UpdatedMedicine, updatedMedicine);
            OnUserEvent(userArgs);
        }
        public void Update_DeletedMedicine(Medicine deletedMedicine)
        {
            UserEventArgs userArgs = new UserEventArgs(UserEvent.Update_DeletedMedicine, deletedMedicine);
            OnUserEvent(userArgs);
        }
        public void Update_AddedOrder(Order order)
        {
            UserEventArgs userArgs = new UserEventArgs(UserEvent.Update_AddedOrder, order);
            OnUserEvent(userArgs);
        }
        protected virtual void OnUserEvent(UserEventArgs e)
        {
            if (updateEvent == null) return;
            updateEvent(this, e);
        }
        public IList<Medicine> GetAllMedicines()
        {
            return server.GetAllMedicines().ToList();
        }
        public void AddMedicine(Medicine medicine)
        {
            server.AddMedicine(medicine);
        }
        public void UpdateMedicine(Medicine medicine, bool substract)
        {
            server.UpdateMedicine(medicine, substract);
        }
        public void DeleteMedicine(int idToDelete)
        {
            server.DeleteMedicine(idToDelete);
        }
        public List<Medicine> GetOrderMedicines(int orderId)
        {
            return server.GetOrderMedicines(orderId);
        }
        public IList<Medicine> FilterMedicines(Purpose purpose)
        {
            return server.FilterMedicines(purpose).ToList();
        }
        public Medicine FindMedicine(int id)
        {
            return server.FindMedicine(id);
        }
        public BindingList<Order> GetIncompleteOrders()
        {
            return new BindingList<Order>(server.GetIncompleteOrders());
        }
        public void CompleteOrder(int orderId)
        {
            server.UpdateOrder(orderId, OrderStatus.Completed);
        }
        public void Update_UpdatedOrder(Order order)
        {
            UserEventArgs userArgs = new UserEventArgs(UserEvent.Update_UpdatedOrder, order);
            OnUserEvent(userArgs);
        }
    }
}