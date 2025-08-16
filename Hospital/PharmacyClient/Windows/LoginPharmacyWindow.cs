using System;
using System.Windows.Forms;
using model;

namespace client
{
    public partial class LoginPharmacyWindow : Form
    {
        private PharmacyController ctrl;
        public LoginPharmacyWindow(PharmacyController ctrl)
        {
            InitializeComponent();
            this.ctrl = ctrl;
            maskedTextBox_Password.UseSystemPasswordChar = true;
        }

        private void button_Login_Click(object sender, EventArgs e)
        {
            string pharmacistName = textBox_Name.Text;
            string pharmacistPassword = maskedTextBox_Password.Text;
            textBox_Name.Clear();
            maskedTextBox_Password.Clear();
            Pharmacist pharmacist = new Pharmacist(pharmacistName, pharmacistPassword);
            try
            {
                pharmacist = ctrl.Login(pharmacist);
                PharmacyWindow pharmacyWindow = new PharmacyWindow(ctrl);
                pharmacyWindow.Show();
                pharmacyWindow.setLoginWindow(this);
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