using System;
using System.Windows.Forms;
using model;

namespace MedicalStaffClient
{
    public partial class LoginMedicalStaffWindow : Form
    {
        private MedicalStaffController ctrl;
        public LoginMedicalStaffWindow(MedicalStaffController ctrl)
        {
            InitializeComponent();
            this.ctrl = ctrl;
            textBox_Password.UseSystemPasswordChar = true;
        }

        private void button_Login_Click(object sender, EventArgs e)
        {
            string medicalStaffName = textBox_Name.Text;
            string medicalStaffPassword = textBox_Password.Text;
            textBox_Name.Clear();
            textBox_Password.Clear();
            MedicalStaff medicalStaff = new MedicalStaff(medicalStaffName, medicalStaffPassword);
            try
            {
                medicalStaff = ctrl.Login(medicalStaff);
                // MessageBox.Show("success");
                ctrl.SetMedicalStaff(medicalStaff);
                MedicalStaffWindow medicalStaffWindow = new MedicalStaffWindow(ctrl);
                medicalStaffWindow.Show();
                medicalStaffWindow.setLoginWindow(this);
                Hide();
            }
            catch (Exception ex)
            {
                MessageBox.Show(text: ex.Message, caption: "Error!");
                return;
            }
        }
    }
}