using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Windows.Forms;
using Hospital;
using model;

namespace MedicalStaffClient
{
    public partial class MedicalStaffWindow : Form
    {
        private bool newOrderClicked = false;
        private Form loginWindow;
        private MedicalStaffController ctrl;
        private IList<Medicine> modelMedicines;
        private BindingList<Medicine> modelMedicines2;
        private BindingList<Order> modelOrders;
        private OrderWindow orderWindow;
        public MedicalStaffWindow(MedicalStaffController medicalStaffController)
        {
            InitializeComponent();
            this.ctrl = medicalStaffController;
            modelMedicines = ctrl.GetAllMedicines();
            modelMedicines2 = new BindingList<Medicine>(modelMedicines);
            // dataGridView_Medicines.DataSource = modelMedicines;
            initMedicinesDGV();
            initOrdersDGV();
            dataGridView_Medicines.DataSource = modelMedicines2;
            modelOrders = ctrl.GetOrdersByMedicalStaffId(ctrl.GetMedicalStaff().Id);
            dataGridView_Orders.DataSource = modelOrders;
            // dataGridView_Medicines.DataSource = null;
            ctrl.updateEvent += userUpdate;
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
        public void setLoginWindow(Form loginWindow)
        {
            this.loginWindow = loginWindow;
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
        
        private void userUpdate(object Sender, UserEventArgs E)
        {
            if (E.UserEventType == UserEvent.Update_AddedOrder)
            {
                Order addedOrder = (Order)E.Data;
                modelOrders.Add(addedOrder);
                // dataGridView_Medicines.DataSource = null;
                modelOrders.ResetBindings();
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
                // dataGridView_Medicines.DataSource = null;
                modelOrders.ResetBindings();
            }
            if (E.UserEventType == UserEvent.Update_AddedMedicine)
            {
                Medicine addedMedicine = (Medicine)E.Data;
                // modelMedicines.Add(addedMedicine);
                modelMedicines2.Add(addedMedicine);
                // MessageBox.Show(dataGridView_Medicines.ToString());
                // MessageBox.Show("lole");
                // dataGridView_Medicines.DataSource = typeof(List<Medicine>);
                // dataGridView_Medicines.DataSource = modelMedicines;
            }

            if (E.UserEventType == UserEvent.Update_UpdatedMedicine)
            {
                Medicine updatedMedicine = (Medicine)E.Data;
                // Medicine toUpdateMedicine = modelMedicines.FirstOrDefault(m => m.Id == updatedMedicine.Id);
                Medicine toUpdateMedicine = modelMedicines2.FirstOrDefault(m => m.Id == updatedMedicine.Id);
                if (toUpdateMedicine != null)
                {
                    toUpdateMedicine.Name = updatedMedicine.Name;
                    toUpdateMedicine.Purpose = updatedMedicine.Purpose;
                    toUpdateMedicine.AvailableQuantity = updatedMedicine.AvailableQuantity;
                    
                    modelMedicines2.ResetBindings();
                    // dataGridView_Medicines.DataSource = null;
                    // dataGridView_Medicines.DataSource = modelMedicines2;
                }

            }

            if (E.UserEventType == UserEvent.Update_DeletedMedicine)
            {
                Medicine medicine = (Medicine)E.Data;
                int IdToDelete = medicine.Id;
                // Medicine toDeleteMedicine = modelMedicines.FirstOrDefault(m => m.Id == IdToDelete);
                Medicine toDeleteMedicine = modelMedicines2.FirstOrDefault(m => m.Id == IdToDelete);
                if (toDeleteMedicine != null)
                {
                    // modelMedicines.Remove(toDeleteMedicine);
                    modelMedicines2.Remove(toDeleteMedicine);
                }

                // dataGridView_Medicines.DataSource = null;
                // dataGridView_Medicines.DataSource = modelMedicines;
            }
        }

        private void button_NewOrder_Click(object sender, EventArgs e)
        {
            newOrderClicked = true;
            orderWindow = new OrderWindow(ctrl);
            orderWindow.Show();
        }

        private void dataGridView_Medicines_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            if (newOrderClicked)
            {
                DataGridViewRow row = dataGridView_Medicines.SelectedRows[0];
                Medicine selectedMedicine = (Medicine)row.DataBoundItem;
                MedicineQuantityWindow medicineQuantityWindow = new MedicineQuantityWindow(ctrl, selectedMedicine);
                medicineQuantityWindow.Show();
            }
        }
    }
}