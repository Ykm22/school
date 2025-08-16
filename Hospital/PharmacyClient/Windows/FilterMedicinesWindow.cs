using System;
using System.Collections.Generic;
using System.Windows.Forms;
using model;

namespace client
{
    public partial class FilterMedicinesWindow : Form
    {
        private PharmacyController ctrl;
        private DataGridView toFilter;
        public FilterMedicinesWindow(PharmacyController ctrl, DataGridView dataGridView)
        {
            InitializeComponent();
            this.ctrl = ctrl;
            toFilter = dataGridView;
            comboBox_FilterPurpose.Text = "Headache";
            comboBox_FilterPurpose.Items.Add("Headache");
            comboBox_FilterPurpose.Items.Add("Stomachache");
            comboBox_FilterPurpose.Items.Add("Sore throat");
        }

        private void button_Filter_Click(object sender, EventArgs e)
        {
            Purpose purpose = GetPurpose(comboBox_FilterPurpose);
            IList<Medicine> medicines = ctrl.FilterMedicines(purpose);
            MessageBox.Show("Filtering realized succesfully!");
            toFilter.DataSource = null;
            toFilter.DataSource = medicines;
            Hide();
        }
        private Purpose GetPurpose(ComboBox comboBoxPurpose)
        {
            if (comboBoxPurpose.Text == "Headache")
                return Purpose.Headache;
            if (comboBoxPurpose.Text == "Stomachache")
                return Purpose.Stomachache;
            if (comboBoxPurpose.Text == "Sore throat")
                return Purpose.SoreThroat;
            return Purpose.Headache;
        }
    }
}