using System;
using System.Windows.Forms;

namespace client
{
    public partial class DeleteMedicineWindow : Form
    {
        private PharmacyController ctrl;
        public DeleteMedicineWindow(PharmacyController ctrl)
        {
            InitializeComponent();
            this.ctrl = ctrl;
        }

        private void button_Delete_Click(object sender, EventArgs e)
        {
            int IdToDelete = (int)numericUpDown_IdDelete.Value;
            ctrl.DeleteMedicine(IdToDelete);
            MessageBox.Show("Medicine deleted successfully");
            Hide();
        }
    }
}