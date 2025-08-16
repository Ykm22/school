using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Threading.Tasks;
using System.Windows.Forms;
using model;

namespace MedicalStaffClient
{
    public partial class OrderWindow : Form
    {
        private MedicalStaffController ctrl;
        // private BindingList<Medicine> selectedMedicines;
        public OrderWindow(MedicalStaffController ctrl)
        {
            InitializeComponent();
            this.ctrl = ctrl;
            // selectedMedicines = new BindingList<Medicine>();
            // dataGridView_Medicines.DataSource = selectedMedicines;
            initMedicinesDGV();
            ctrl.SetDGV(dataGridView_Medicines);
            
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
        private async void button_Send_Click(object sender, EventArgs e)
        {
            ctrl.SetFirstElement(true);
            IList<Medicine> medicines = new List<Medicine>();
            foreach (DataGridViewRow row in dataGridView_Medicines.Rows)
            {
                Medicine medicine = (Medicine)row.DataBoundItem;
                if (medicine != null)
                {
                    // Medicine toModifyMedicine = ctrl.FindMedicine(medicine.Id);
                    // toModifyMedicine.AvailableQuantity -= medicine.AvailableQuantity;
                    // ctrl.UpdateMedicine(toModifyMedicine);
                    medicines.Add(medicine);
                }
            }

            Order order = new Order();
            order.TimeSent = DateTime.Now;
            order.OrderStatus = OrderStatus.Incomplete;
            order.medicalStaffId = ctrl.GetMedicalStaff().Id;
            
            int orderId = ctrl.SaveOrder(order);
            IList<OrderMedicine> orderMedicines = new List<OrderMedicine>();
            foreach (var x in medicines)
            {
                OrderMedicine orderMedicine = new OrderMedicine(
                    orderId,
                    x.Id,
                    x.AvailableQuantity);
                orderMedicines.Add(orderMedicine);
            }

            ctrl.SaveOrderMedicines(orderMedicines);

            MessageBox.Show("Order sent successfully!");
            await Task.Delay(500);
            Hide();
        }
    }
    
}