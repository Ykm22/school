using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Threading.Tasks;
using System.Windows.Forms;
using model;

namespace client
{
    public partial class OrderMedicinesWindow : Form
    {
        private PharmacyController ctrl;
        private Order selectedOrder;
        private BindingList<Medicine> modelMedicines;
        public OrderMedicinesWindow(PharmacyController ctrl, Order selectedOrder)
        {
            InitializeComponent();
            this.ctrl = ctrl;
            this.selectedOrder = selectedOrder;
            modelMedicines = new BindingList<Medicine>(ctrl.GetOrderMedicines(selectedOrder.Id));
            initMedicinesDGV();
            dataGridView_Medicines.DataSource = modelMedicines;
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
        private async void button_Complete_Click(object sender, EventArgs e)
        {
            IList<Medicine> medicines = new List<Medicine>(modelMedicines);
            foreach (var medicine in medicines)
            {
                ctrl.UpdateMedicine(medicine, true);
            }

            ctrl.CompleteOrder(selectedOrder.Id);
            
            MessageBox.Show("Order completed!");
            await Task.Delay(500);
            Hide();
        }
    }
}