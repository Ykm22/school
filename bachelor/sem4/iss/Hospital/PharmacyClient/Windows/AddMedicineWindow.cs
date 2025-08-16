using System;
using System.Windows.Forms;
using model;

namespace client
{
    public partial class AddMedicineWindow : Form
    {
        private PharmacyController ctrl;
        public AddMedicineWindow(PharmacyController ctrl)
        {
            InitializeComponent();
            comboBox_Purpose.Text = "Headache";
            comboBox_Purpose.Items.Add("Headache");
            comboBox_Purpose.Items.Add("Stomachache");
            comboBox_Purpose.Items.Add("Sore throat");
            this.ctrl = ctrl;
        }

        private void button_AddMedicine_Click(object sender, EventArgs e)
        {
            string Name = textBox_Name.Text;
            Purpose purpose = GetPurpose(comboBox_Purpose);
            int AvailableQuantity = (int)numericUpDown_Quantity.Value;
            ctrl.AddMedicine(new Medicine(purpose, Name, AvailableQuantity));
            MessageBox.Show("Medicine added successfully!");
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