using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Windows.Forms;
using model;

namespace client
{
    public partial class PharmacyWindow : Form
    {
        private Form loginWindow;
        private PharmacyController ctrl;
        // private IList<Medicine> modelMedicines;
        private BindingList<Medicine> modelMedicines;
        private BindingList<Order> modelOrders;
        public void setLoginWindow(Form loginWindow)
        {
            this.loginWindow = loginWindow;
        }
        public PharmacyWindow(PharmacyController ctrl)
        {
            InitializeComponent();
            this.ctrl = ctrl;
            // modelMedicines = ctrl.GetAllMedicines();
            modelMedicines = new BindingList<Medicine>(ctrl.GetAllMedicines());
            modelOrders = ctrl.GetIncompleteOrders();
            // MessageBox.Show(modelMedicines.GetType().ToString());
            initOrdersDGV();
            initMedicinesDGV();
            dataGridView_Medicines.DataSource = modelMedicines;
            
            dataGridView_Orders.DataSource = modelOrders;
            // dataGridView_Medicines.DataSource = null;
            ctrl.updateEvent += userUpdate;
        }

        private void initMedicinesDGV()
        {
            dataGridView_Medicines.AutoGenerateColumns = false; // Disable automatic column generation

            // Create and configure columns for the desired attributes
            DataGridViewTextBoxColumn idColumn = new DataGridViewTextBoxColumn();
            idColumn.DataPropertyName = "Id";
            idColumn.HeaderText = "Medicine Id";

            DataGridViewTextBoxColumn purposeColumn = new DataGridViewTextBoxColumn();
            purposeColumn.DataPropertyName = "Purpose";
            purposeColumn.HeaderText = "Purpose";

            DataGridViewTextBoxColumn nameColumn = new DataGridViewTextBoxColumn();
            nameColumn.DataPropertyName = "Name";
            nameColumn.HeaderText = "Name";
            
            DataGridViewTextBoxColumn availableQuantityColumn = new DataGridViewTextBoxColumn();
            availableQuantityColumn.DataPropertyName = "AvailableQuantity";
            availableQuantityColumn.HeaderText = "Available Quantity";

            // Add the columns to the DataGridView
            dataGridView_Medicines.Columns.Add(idColumn);
            dataGridView_Medicines.Columns.Add(purposeColumn);
            dataGridView_Medicines.Columns.Add(nameColumn);
            dataGridView_Medicines.Columns.Add(availableQuantityColumn);
        }

        private void initOrdersDGV()
        {
            dataGridView_Orders.AutoGenerateColumns = false; // Disable automatic column generation

            // Create and configure columns for the desired attributes
            DataGridViewTextBoxColumn idColumn = new DataGridViewTextBoxColumn();
            idColumn.DataPropertyName = "Id";
            idColumn.HeaderText = "Order ID";

            DataGridViewTextBoxColumn timeSentColumn = new DataGridViewTextBoxColumn();
            timeSentColumn.DataPropertyName = "timeSent";
            timeSentColumn.HeaderText = "Time Sent";

            DataGridViewTextBoxColumn orderStatusColumn = new DataGridViewTextBoxColumn();
            orderStatusColumn.DataPropertyName = "orderStatus";
            orderStatusColumn.HeaderText = "Order Status";

            DataGridViewTextBoxColumn medicalStaffIdColumn = new DataGridViewTextBoxColumn();
            medicalStaffIdColumn.DataPropertyName = "medicalStaffId";
            medicalStaffIdColumn.HeaderText = "Medical Staff Id";
            
            // Add the columns to the DataGridView
            dataGridView_Orders.Columns.Add(idColumn);
            dataGridView_Orders.Columns.Add(timeSentColumn);
            dataGridView_Orders.Columns.Add(orderStatusColumn);
            dataGridView_Orders.Columns.Add(medicalStaffIdColumn);

        }

        private BindingList<Order> SortOrdersModel()
        {
            return new BindingList<Order>(modelOrders.OrderBy(o => o.TimeSent).ToList());
        }
        private void userUpdate(object Sender, UserEventArgs E)
        {
            if (E.UserEventType == UserEvent.Update_AddedMedicine)
            {
                Medicine addedMedicine = (Medicine)E.Data;
                modelMedicines.Add(addedMedicine);
                // dataGridView_Medicines.DataSource = null;
                dataGridView_Medicines.DataSource = modelMedicines;
            }
            if (E.UserEventType == UserEvent.Update_UpdatedOrder)
            {
                // MessageBox.Show("aloooooooooooo");
                Order updatedOrder = (Order)E.Data;
                Order toUpdateOrder = modelOrders.FirstOrDefault(o => o.Id == updatedOrder.Id);
                if (toUpdateOrder != null)
                {
                    toUpdateOrder.OrderStatus = updatedOrder.OrderStatus;
                }

                if (toUpdateOrder.OrderStatus == OrderStatus.Completed)
                {
                    // MessageBox.Show("lol");
                    modelOrders.Remove(toUpdateOrder);
                }
                // modelOrders = ctrl.GetIncompleteOrders();
                // modelOrders = SortOrdersModel();
                // modelOrders.ResetBindings();
                dataGridView_Orders.DataSource = null;
                dataGridView_Orders.DataSource = modelOrders;
            }
            if (E.UserEventType == UserEvent.Update_AddedOrder)
            {
                Order addedOrder = (Order)E.Data;
                modelOrders.Add(addedOrder);
                // dataGridView_Medicines.DataSource = null;
                // modelOrders = SortOrdersModel();
                modelOrders.ResetBindings();
                dataGridView_Orders.DataSource = null;
                dataGridView_Orders.DataSource = modelOrders;
            }
            
            if (E.UserEventType == UserEvent.Update_UpdatedMedicine)
            {
                Medicine updatedMedicine = (Medicine)E.Data;
                Medicine toUpdateMedicine = modelMedicines.FirstOrDefault(m => m.Id == updatedMedicine.Id);
                if (toUpdateMedicine != null)
                {
                    toUpdateMedicine.Name = updatedMedicine.Name;
                    toUpdateMedicine.Purpose = updatedMedicine.Purpose;
                    toUpdateMedicine.AvailableQuantity = updatedMedicine.AvailableQuantity;
                }
                // dataGridView_Medicines.DataSource = null;
                modelMedicines.ResetBindings();
                // dataGridView_Medicines.DataSource = modelMedicines;
                // dataGridView_Medicines.DataSource = modelMedicines;
            }

            if (E.UserEventType == UserEvent.Update_DeletedMedicine)
            {
                Medicine medicine = (Medicine)E.Data;
                int IdToDelete = medicine.Id;
                Medicine toDeleteMedicine = modelMedicines.FirstOrDefault(m => m.Id == IdToDelete);
                if (toDeleteMedicine != null)
                {
                    modelMedicines.Remove(toDeleteMedicine);
                }

                // dataGridView_Medicines.DataSource = null;
                dataGridView_Medicines.DataSource = modelMedicines;
            }
        }
        private void button_AddMedicine_Click(object sender, EventArgs e)
        {
            AddMedicineWindow addMedicineWindow = new AddMedicineWindow(ctrl);
            addMedicineWindow.Show();
        }

        private void button_UpdateMedicine_Click(object sender, EventArgs e)
        {
            UpdateMedicineWindow updateMedicineWindow = new UpdateMedicineWindow(ctrl);
            updateMedicineWindow.Show();
        }

        private void button_DeleteMedicine_Click(object sender, EventArgs e)
        {
            DeleteMedicineWindow deleteMedicineWindow = new DeleteMedicineWindow(ctrl);
            deleteMedicineWindow.Show();
        }

        private void button_FilterMedicines_Click(object sender, EventArgs e)
        {
            FilterMedicinesWindow filterMedicinesWindow = new FilterMedicinesWindow(ctrl, dataGridView_Medicines);
            filterMedicinesWindow.Show();
        }

        private void button_Refresh_Click(object sender, EventArgs e)
        {
            modelMedicines = new BindingList<Medicine>(ctrl.GetAllMedicines());
            dataGridView_Medicines.DataSource = null;
            dataGridView_Medicines.DataSource = modelMedicines;
        }

        private void dataGridView_Orders_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            DataGridViewRow row = dataGridView_Orders.SelectedRows[0];
            Order selectedOrder = (Order)row.DataBoundItem;
            OrderMedicinesWindow orderMedicinesWindow = new OrderMedicinesWindow(ctrl, selectedOrder);
            orderMedicinesWindow.Show();
        }
    }
}