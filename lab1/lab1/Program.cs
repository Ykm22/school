using System.Configuration;

namespace lab1
{
    internal static class Program
    {
        /// <summary>
        ///  The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            // To customize application configuration such as set high DPI settings or default font,
            // see https://aka.ms/applicationconfiguration.
            //var fileConfig = ConfigurationManager.OpenExeConfiguration("/bd.config");
            ConnectionStringSettings settings = ConfigurationManager.ConnectionStrings["FermaDeAnimaleDB"];
            string stringConn = settings.ConnectionString;
            //parent table
            string parentTable = ConfigurationManager.AppSettings["parentTable_SpatiiDeAnimale"];
            string selectParentCommand = ConfigurationManager.AppSettings["selectParentCommand_SpatiiDeAnimale"];
            //child table -animale
            int noParams = int.Parse(ConfigurationManager.AppSettings["noParams_Animale"]);
            string paramTypes = ConfigurationManager.AppSettings["paramTypes_Animale"];
            string childTable = ConfigurationManager.AppSettings["childTable_Animale"];
            string selectChildCommand = ConfigurationManager.AppSettings["selectChildCommand_Animale"];
            string deleteChildCommand = ConfigurationManager.AppSettings["deleteChildCommand_Animale"];
            string updateChildCommand = ConfigurationManager.AppSettings["updateChildCommand_Animale"];
            string insertChildCommand = ConfigurationManager.AppSettings["insertChildCommand_Animale"];
            //child table - ingrijitori
            //int noParams = int.Parse(ConfigurationManager.AppSettings["noParams_Ingrijitori"]);
            //string paramTypes = ConfigurationManager.AppSettings["paramTypes_Ingrijitori"];
            //string childTable = ConfigurationManager.AppSettings["childTable_Ingrijitori"];
            //string selectChildCommand = ConfigurationManager.AppSettings["selectChildCommand_Ingrijitori"];
            //string deleteChildCommand = ConfigurationManager.AppSettings["deleteChildCommand_Ingrijitori"];
            //string updateChildCommand = ConfigurationManager.AppSettings["updateChildCommand_Ingrijitori"];
            //string insertChildCommand = ConfigurationManager.AppSettings["insertChildCommand_Ingrijitori"];
            ApplicationConfiguration.Initialize();
            Application.Run(new Form1(stringConn, noParams, paramTypes, parentTable, childTable, selectParentCommand, selectChildCommand, deleteChildCommand, updateChildCommand, insertChildCommand));
        }
    }
}