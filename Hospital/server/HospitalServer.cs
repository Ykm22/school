using System;
using System.Collections.Generic;
using System.Configuration;
using System.Diagnostics.Eventing.Reader;
using System.Net.Sockets;
using System.Reflection;
using System.Threading;
using System.Windows.Forms;
using model;
using networking;
using NHibernate.Dialect;
using NHibernate.Driver;
using repository.MedicalStaffRepository;
using repository.MedicinesRepository;
using repository.OrdersRepository;
using repository.PharmacistsRepository;
using services;
using Configuration = NHibernate.Cfg.Configuration;

namespace server
{
    public class HospitalServer
    {
        static void Main(string[] args)
        {
            // using (var session = NHibernateHelper.GetSession())
            // {
            //     Medicine med1 = new Medicine(Purpose.Headache, "asd", 1);
            //     IList<Medicine> medicines = new List<Medicine>();
            //     medicines.Add(med1);
            //     session.Save(new Order(medicines, DateTime.Now));
                //     session.Save(new MedicalStaff("Andrei", "Andrei"));
                // session.Save(new Medicine(Purpose.Headache, "Aspirin", 300));
                // session.Save(new Medicine(Purpose.Headache, "Ibuprofen", 200));
                // session.Save(new Medicine(Purpose.Headache, "Naproxen", 150));
                // session.Save(new Medicine(Purpose.Stomachace, "Camylofin", 20));
                // session.Save(new Medicine(Purpose.Stomachace, "Dexlansoprazole", 130));
                // session.Save(new Medicine(Purpose.Stomachace, "Drotaverine", 30));
                // session.Save(new Medicine(Purpose.SoreThroat, "Actamin", 20));
                // session.Save(new Medicine(Purpose.SoreThroat, "Tylenol", 40));

            // }
            // !!!works
            // using (var session = NHibernateHelper.GetSession())
            // {
            //     using (var transaction = session.BeginTransaction())
            //     {
            //         try
            //         {
            //             Medicine med1 = new Medicine(Purpose.Headache, "Aspirin", 10);
            //             Medicine med2 = new Medicine(Purpose.Headache, "Tylenol", 20);
            //
            //             Order order1 = new Order(new List<Medicine> { med1 }, DateTime.Now, OrderStatus.Incomplete);
            //             Order order2 = new Order(new List<Medicine> { med2 }, DateTime.Now, OrderStatus.Incomplete);
            //
            //             med1.Orders.Add(order1);
            //             med2.Orders.Add(order2);
            //
            //             session.SaveOrUpdate(order1);
            //             session.SaveOrUpdate(order2);
            //
            //             transaction.Commit();
            //         }
            //         catch (Exception ex)
            //         {
            //             transaction.Rollback();
            //             // Handle or log the exception
            //         }
            //     }
            // }
            
            // m-n orm mapping x)x)x):D:D:D!!!!!!
            // using (var session = NHibernateHelper.GetSession())
            // {
            //     // Get the medicines by their IDs
            //     var medicine1 = session.Get<Medicine>(2); // Assuming medicine with ID 2 exists in the database
            //     var medicine2 = session.Get<Medicine>(3); // Assuming medicine with ID 3 exists in the database
            //
            //     // Create an order
            //     var order = new Order();
            //     order.TimeSent = DateTime.Now;
            //     order.OrderStatus = OrderStatus.Incomplete;
            //
            //     // Save the order in the database
            //     using (var transaction = session.BeginTransaction())
            //     {
            //         session.Save(order);
            //         transaction.Commit();
            //     }
            //
            //     // Set the OrderId for each OrderMedicine item and save them in the database
            //     using (var transaction = session.BeginTransaction())
            //     {
            //         var orderMedicine1 = new OrderMedicine(order.Id, medicine1.Id, 5);
            //         var orderMedicine2 = new OrderMedicine(order.Id, medicine2.Id, 10);
            //
            //         session.Save(orderMedicine1);
            //         session.Save(orderMedicine2);
            //
            //         transaction.Commit();
            //     }
            // }







            IMedicinesRepository<int, Medicine> medicinesRepository = new DBMedicinesRepository(NHibernateHelper.SessionFactory);
            IPharmacistsRepository<int, Pharmacist> pharmacistsRepository = new DBPharmacistsRepository(NHibernateHelper.SessionFactory);
            IMedicalStaffRepository<int, MedicalStaff> medicalStaffRepository = new DBMedicalStaffRepository(NHibernateHelper.SessionFactory);
            IOrdersRepository<int, Order> ordersRepository = new DBOrdersRepository(NHibernateHelper.SessionFactory);
            IServices services = new Services(medicinesRepository, pharmacistsRepository, medicalStaffRepository, ordersRepository);
            SerialServer server = new SerialServer("127.0.0.1", 55556, services);
            server.Start();
            Console.WriteLine("Server started...");
        }
    }

    public class SerialServer : ConcurrentServer
    {
        private IServices server;
        private ClientWorker worker;

        public SerialServer(string host, int port, IServices server) : base(host, port)
        {
            this.server = server;
            Console.WriteLine("Serial server ...");
        }

        protected override Thread createWorker(TcpClient client)
        {
            worker = new ClientWorker(server, client);
            return new Thread(new ThreadStart(worker.run));
        }
    }
}