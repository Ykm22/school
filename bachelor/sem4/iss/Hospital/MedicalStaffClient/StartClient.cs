using System;
using System.Windows.Forms;
using networking;
using services;

namespace MedicalStaffClient
{
    public class StartClient
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            IServices server = new ServerProxy("127.0.0.1", 55556);
            MedicalStaffController ctrl = new MedicalStaffController(server);
            LoginMedicalStaffWindow loginWindow = new LoginMedicalStaffWindow(ctrl);
            Application.Run(loginWindow);
        }
    }
}