using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Windows.Forms;
using Hospital;
using model;
using services;

namespace MedicalStaffClient
{
    public class MedicalStaffController : IObserver
    {
        public void Update_AddedOrder(Order order)
        {
            UserEventArgs userArgs = new UserEventArgs(UserEvent.Update_AddedOrder, order);
            OnUserEvent(userArgs);
        }

        public void Update_UpdatedOrder(Order order)
        {
            UserEventArgs userArgs = new UserEventArgs(UserEvent.Update_UpdatedOrder, order);
            OnUserEvent(userArgs);
        }

        public event EventHandler<UserEventArgs> updateEvent;
        private readonly IServices server;
        private MedicalStaff loggedMedicalStaff;
        public DataGridView dataGridView_OrderMedicines;
        public BindingList<Medicine> selectedMedicines;
        private bool firstElement = true;
        private MedicalStaff medicalStaff;

        public MedicalStaffController(IServices server)
        {
            this.server = server;
            loggedMedicalStaff = null;
        }
        public MedicalStaff Login(MedicalStaff medicalStaff)
        {
            loggedMedicalStaff = server.LoginMedicalStaff(medicalStaff, this);
            Console.WriteLine("Current user {0}", loggedMedicalStaff);
            return loggedMedicalStaff;
        }
        public IList<Medicine> GetAllMedicines()
        {
            return server.GetAllMedicines().ToList();
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
        protected virtual void OnUserEvent(UserEventArgs e)
        {
            if (updateEvent == null) return;
            updateEvent(this, e);
        }

        public void SetDGV(DataGridView dataGridViewMedicines)
        {
            // MessageBox.Show("lol");
            dataGridView_OrderMedicines = dataGridViewMedicines;
            selectedMedicines = new BindingList<Medicine>();
            // dataGridView_OrderMedicines.DataSource = selectedMedicines;
        }

        public void AddMedicineToOrder(Medicine selectedMedicine, int quantity)
        {
            Medicine toAddMedicine = new Medicine(selectedMedicine.Purpose, selectedMedicine.Name, quantity);
            toAddMedicine.SetId(selectedMedicine.Id);
            selectedMedicines.Add(toAddMedicine);
            if (firstElement)
            {
                firstElement = false;
                dataGridView_OrderMedicines.DataSource = selectedMedicines;
            }
            
        }
        public void UpdateMedicine(Medicine medicine)
        {
            server.UpdateMedicine(medicine, false);
        }
        
        public Medicine FindMedicine(int id)
        {
            return server.FindMedicine(id);
        }

        public int SaveOrder(Order order)
        {
            return server.AddOrder(order);
        }

        public void SaveOrderMedicines(IList<OrderMedicine> orderMedicines)
        {
            server.AddOrderMedicines(orderMedicines);
        }

        public void SetMedicalStaff(MedicalStaff medicalStaff)
        {
            this.medicalStaff = medicalStaff;
        }

        public MedicalStaff GetMedicalStaff()
        {
            return this.medicalStaff;
        }

        public BindingList<Order> GetOrdersByMedicalStaffId(int medicalStaffId)
        {
            return new BindingList<Order>(server.GetOrdersByMedicalStaffId(medicalStaffId));
        }

        public void SetFirstElement(bool b)
        {
            this.firstElement = b;
        }
    }
}