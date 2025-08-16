using System;
using System.Windows.Forms;
using model;

namespace client
{
    public partial class UpdateMedicineWindow : Form
    {
        private PharmacyController ctrl;
        public UpdateMedicineWindow(PharmacyController ctrl)
        {
            InitializeComponent();
            this.ctrl = ctrl;
            comboBox_NewPurpose.Text = "Headache";
            comboBox_NewPurpose.Items.Add("Headache");
            comboBox_NewPurpose.Items.Add("Stomachache");
            comboBox_NewPurpose.Items.Add("Sore throat");
        }

        private void button_Update_Click(object sender, EventArgs e)
        {
            int IdToUpdate = (int)numericUpDown_IdToUpdate.Value;
            string NewName = textBox_NewName.Text;
            Purpose purpose = GetPurpose(comboBox_NewPurpose);
            int NewAvailableQuantity = (int)numericUpDown_NewQuantity.Value;
            Medicine medicine = new Medicine(purpose, NewName, NewAvailableQuantity);
            medicine.SetId(IdToUpdate);
            ctrl.UpdateMedicine(medicine, false);
            MessageBox.Show("Medicine updated successfully!");
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