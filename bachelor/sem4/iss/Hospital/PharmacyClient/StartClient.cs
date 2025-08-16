using System;
using System.Windows.Forms;
using networking;
using services;

namespace client
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
            PharmacyController ctrl = new PharmacyController(server);
            LoginPharmacyWindow loginWindow = new LoginPharmacyWindow(ctrl);
            Application.Run(loginWindow);
        }
    }
}