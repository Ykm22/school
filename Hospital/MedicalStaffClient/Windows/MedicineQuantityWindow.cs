using System;
using System.Windows.Forms;
using model;

namespace MedicalStaffClient
{
    public partial class MedicineQuantityWindow : Form
    {
        private MedicalStaffController ctrl;
        private Medicine selectedMedicine;
        public MedicineQuantityWindow(MedicalStaffController ctrl, Medicine selectedMedicine)
        {
            InitializeComponent();
            this.ctrl = ctrl;
            this.selectedMedicine = selectedMedicine;
        }

        private void button_Confirm_Click(object sender, EventArgs e)
        {
            int quantity = (int)numericUpDown_Quantity.Value;
            // MessageBox.Show(selectedMedicine.Name +  ' ' + selectedMedicine.Purpose + ' ' +
            //     quantity);
            ctrl.AddMedicineToOrder(selectedMedicine, quantity);
            Hide();
        }
    }
}