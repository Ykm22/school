using System;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Formatters.Binary;
using System.Windows.Forms;
using model;
using networking.DTO;
using networking.ObjectProtocol;
using NHibernate;
using services;

namespace networking
{
    public class ClientWorker : IObserver
    {
        private IServices server;
        private TcpClient connection;

        private NetworkStream stream;
        private IFormatter formatter;
        private volatile bool connected;
        
        public ClientWorker(IServices server, TcpClient connection)
        {
            this.server = server;
            this.connection = connection;
            try
            {
                stream = connection.GetStream();
                formatter = new BinaryFormatter();
                connected = true;
            }
            catch (Exception e)
            {
                Console.WriteLine(e.StackTrace);
            }
        }
        public virtual void run()
        {
            while (connected)
            {
                try
                {
                    object request = formatter.Deserialize(stream);
                    object response = handleRequest((Request)request);
                    if (response != null)
                    {
                        sendResponse((Response)response);
                    }
                }
                catch (Exception e)
                {
                    Console.WriteLine(e.StackTrace);
                }

                // try
                // {
                //     Thread.Sleep(1000);
                // }
                // catch (Exception e)
                // {
                //     Console.WriteLine(e.StackTrace);
                // }
            }

            try
            {
                stream.Close();
                connection.Close();
            }
            catch (Exception e)
            {
                Console.WriteLine("error " + e);
            }
        }
        private void sendResponse(Response Response)
        {
            // MessageBox.Show("sending response from worker" + Response);
            Console.WriteLine("sending response " + Response);
            lock (stream)
            {
                formatter.Serialize(stream, Response);
                stream.Flush();
            }

            // Console.WriteLine("finished sending response");
        }
        private Response handleRequest(Request request)
        {
            Response response = null;
            if (request is FindPharmacistByCredentialsRequest)
            {
                FindPharmacistByCredentialsRequest req = (FindPharmacistByCredentialsRequest)request;
                return handleFIND_PHARMACIST_BY_CREDENTIALS(req);
            }
            if (request is GetOrdersByMedicalStaffIdRequest)
            {
                GetOrdersByMedicalStaffIdRequest req = (GetOrdersByMedicalStaffIdRequest)request;
                return handleGET_ORDERS_BY_MEDICAL_STAFF_ID(req);
            }
            if (request is UpdateOrderRequest)
            {
                UpdateOrderRequest req = (UpdateOrderRequest)request;
                return handleUPDATE_ORDER(req);
            }
            if (request is GetOrderMedicinesRequest)
            {
                GetOrderMedicinesRequest req = (GetOrderMedicinesRequest)request;
                return handleGET_ORDER_MEDICINES(req);
            }
            if (request is AddOrderMedicinesRequest)
            {
                AddOrderMedicinesRequest req = (AddOrderMedicinesRequest)request;
                return handleADD_ORDER_MEDICINES(req);
            }
            if (request is GetIncompleteOrdersRequest)
            {
                // MessageBox.Show("in worker");
                GetIncompleteOrdersRequest req = (GetIncompleteOrdersRequest)request;
                return handleGET_INCOMPLETE_ORDERS(req);
            }
            if (request is FindMedicineRequest)
            {
                FindMedicineRequest req = (FindMedicineRequest)request;
                return handleFIND_MEDICINE(req);
            }
            if (request is FindMedicalStaffByCredentialsRequest)
            {
                FindMedicalStaffByCredentialsRequest req = (FindMedicalStaffByCredentialsRequest)request;
                return handleFIND_MEDICAL_STAFF_BY_CREDENTIALS(req);
            }
            if (request is LoginRequest)
            {
                LoginRequest req = (LoginRequest)request;
                return handleLOGIN(req);
            }
            if (request is LoginMedicalStaffRequest)
            {
                LoginMedicalStaffRequest req = (LoginMedicalStaffRequest)request;
                return handleLOGIN_MEDICAL_STAFF(req);
            }
            //
            // if (request is LogoutRequest)
            // {
            //     LogoutRequest req = (LogoutRequest)request;
            //     return handleLOGOUT(req);
            // }
            //
            if (request is GetAllMedicinesRequest)
            {
                GetAllMedicinesRequest req = (GetAllMedicinesRequest)request;
                return handleGET_ALL_MEDICINES(req);
            }
            if (request is FilterMedicinesRequest)
            {
                FilterMedicinesRequest req = (FilterMedicinesRequest)request;
                return handleFILTER_MEDICINES(req);
            }
            if (request is DeleteMedicineRequest)
            {
                DeleteMedicineRequest req = (DeleteMedicineRequest)request;
                return handleDELETE_MEDICINE(req);
            }
            //
            // if (request is FindArtistRequest)
            // {
            //     FindArtistRequest req = (FindArtistRequest)request;
            //     return handleFIND_ARTIST(req);
            // }
            //
            // if (request is FindSpectaclesByDayRequest)
            // {
            //     FindSpectaclesByDayRequest req = (FindSpectaclesByDayRequest)request;
            //     return handleFIND_SPECTACLES_BY_DAY(req);
            // }
            //
            // if (request is FindSpectacleRequest)
            // {
            //     FindSpectacleRequest req = (FindSpectacleRequest)request;
            //     return handleFIND_SPECTACLE(req);
            // }
            //
            if (request is AddMedicineRequest)
            {
                AddMedicineRequest req = (AddMedicineRequest)request;
                return handleADD_MEDICINE(req);
            }
            if (request is AddOrderRequest)
            {
                AddOrderRequest req = (AddOrderRequest)request;
                return handleADD_ORDER(req);
            }
            if (request is UpdateMedicineRequest)
            {
                UpdateMedicineRequest req = (UpdateMedicineRequest)request;
                return handleUPDATE_MEDICINE(req);
            }

            return response;
        }

        private Response handleGET_ORDERS_BY_MEDICAL_STAFF_ID(GetOrdersByMedicalStaffIdRequest req)
        {
            int medicalStaffId = req.MedicalStaffId;
            try
            {
                List<Order> orders;
                lock (server)
                {
                    orders = server.GetOrdersByMedicalStaffId(medicalStaffId);
                }

                return new GetOrdersByMedicalStaffIdResponse(DtoUtils.GetDto(orders));
            }
            catch (HospitalException e)
            {
                return new ErrorResponse(e.Message);
            }
        }

        private Response handleUPDATE_ORDER(UpdateOrderRequest req)
        {
            int orderId = req.OrderId;
            OrderStatus orderStatus = req.OrderStatus;
            try
            {
                lock (server)
                {
                    server.UpdateOrder(orderId, orderStatus);
                }

                return new OkResponse();
            }
            catch (HospitalException e)
            {
                return new ErrorResponse(e.Message);
            }
        }

        public void Update_UpdatedOrder(Order order)
        {
            try
            {
                OrderDto orderDto = DtoUtils.GetDto(order);
                sendResponse(new UpdateUpdatedOrderResponse(orderDto));
            }
            catch (Exception e)
            {
                Console.WriteLine(e.StackTrace);
            }
        }

        private Response handleGET_ORDER_MEDICINES(GetOrderMedicinesRequest req)
        {
            Console.WriteLine("Get order medicines request...");
            try
            {
                IEnumerable<Medicine> medicines;
                lock (server)
                {
                    medicines = server.GetOrderMedicines(req.OrderId);
                }

                IList<MedicineDto> medicinesDto = DtoUtils.GetDto(medicines);
                return new GetOrderMedicinesResponse(medicinesDto);
            }
            catch (HospitalException e)
            {
                return new ErrorResponse(e.Message);
            }
        }

        private Response handleADD_ORDER_MEDICINES(AddOrderMedicinesRequest req)
        {
            Console.WriteLine("Add order medicines request...");
            // MessageBox.Show("does it pass getfromdto");
            IList<OrderMedicine> orderMedicines = DtoUtils.GetFromDto(req.OrderMedicinesDto);
            // MessageBox.Show("it passed");
            try
            {
                lock (server)
                {
                    server.AddOrderMedicines(orderMedicines);
                }

                return new OkResponse();
            }
            catch (HospitalException e)
            {
                return new ErrorResponse(e.Message);
            }
        }

        private Response handleADD_ORDER(AddOrderRequest req)
        {
            Console.WriteLine("Add order request...");
            // MessageBox.Show("does it pass getfromdto");
            Order order = DtoUtils.GetFromDto(req.OrderDto);
            // MessageBox.Show("it passed");
            try
            {
                lock (server)
                {
                    server.AddOrder(order);
                }

                return new AddOrderResponse(order.Id);
            }
            catch (HospitalException e)
            {
                return new ErrorResponse(e.Message);
            }
        }

        private Response handleGET_INCOMPLETE_ORDERS(GetIncompleteOrdersRequest req)
        {
            // MessageBox.Show("in worker = handle_get_incomplete_orders");
            Console.WriteLine("Get incomplete orders request...");
            try
            {
                IList<Order> orders;
                lock (server)
                {
                    orders = server.GetIncompleteOrders();
                }
                // MessageBox.Show("in worker = got orders from server");

                IList<OrderDto> ordersDto = DtoUtils.GetDto(orders);
                return new GetIncompleteOrdersResponse(ordersDto);
            }
            catch (HospitalException e)
            {
                return new ErrorResponse(e.Message);
            }
        }
    

        private Response handleFIND_MEDICINE(FindMedicineRequest req)
        {
            // MessageBox.Show("in client worker, handling find medicine request");
            Console.WriteLine("Find medicine request...");
            int id = req.Id;
            try
            {
                // MessageBox.Show("in client worker, handling find medicine requestv2");
                Medicine medicine = null;
                lock (server)
                {
                    medicine = server.FindMedicine(id);
                    // MessageBox.Show("in client worker, handling find medicine requestv3");
                }

                // MessageBox.Show("in client worker, handling find medicine requestv4");
                return new FindMedicineResponse(DtoUtils.GetDto(medicine));
            }
            catch (HospitalException ex)
            {
                return new ErrorResponse(ex.Message);
            }
        }

        private Response handleLOGIN_MEDICAL_STAFF(LoginMedicalStaffRequest req)
        {
            Console.WriteLine("Login medical staff request...");                          
            MedicalStaff medicalStaff = DtoUtils.GetFromDto(req.MedicalStaffDto);
            try                                                             
            {                                                               
                lock (server)                                               
                {                                                           
                    server.LoginMedicalStaff(medicalStaff, this);                        
                }                                                           
                return new OkResponse();                                    
            }                                                               
            catch (HospitalException e)                                     
            {                                                               
                connected = false;                                          
                return new ErrorResponse(e.Message);                        
            }                                                               
        }

        private Response handleFIND_MEDICAL_STAFF_BY_CREDENTIALS(FindMedicalStaffByCredentialsRequest req)
        {
            Console.WriteLine("Find medical staff by credentials request...");
            string medicalStaffName = req.MedicalStaffName;
            string medicalStaffPassword = req.MedicalStaffPassword;
            try
            {
                MedicalStaff medicalStaff = null;
                lock (server)
                {
                    medicalStaff = server.FindMedicalStaffByCredentials(medicalStaffName, medicalStaffPassword);
                }

                return new FindMedicalStaffByCredentialsResponse(DtoUtils.GetDto(medicalStaff));
            }
            catch (HospitalException ex)
            {
                return new ErrorResponse(ex.Message);
            }
        }

        private Response handleFILTER_MEDICINES(FilterMedicinesRequest req)
        {
            Console.WriteLine("Filter medicines request...");
            try
            {
                IEnumerable<Medicine> medicines;
                lock (server)
                {
                    medicines = server.FilterMedicines(req.Purpose);
                }

                IList<MedicineDto> medicinesDto = DtoUtils.GetDto(medicines);
                return new FilterMedicinesResponse(medicinesDto);
            }
            catch (HospitalException e)
            {
                return new ErrorResponse(e.Message);
            }
        }

        private Response handleDELETE_MEDICINE(DeleteMedicineRequest req)
        {
            int IdToDelete = req.IdToDelete;
            try
            {
                lock (server)
                {
                    server.DeleteMedicine(IdToDelete);
                }
                return new OkResponse();
            }
            catch (HospitalException e)
            {
                return new ErrorResponse(e.Message);
            }
        }

        private Response handleUPDATE_MEDICINE(UpdateMedicineRequest req)
        {
            Medicine medicine = DtoUtils.GetFromDto(req.MedicineDto);
            bool substract = req.Substract;
            try
            {
                lock (server)
                {
                    server.UpdateMedicine(medicine, substract);
                }

                return new OkResponse();
            }
            catch (HospitalException e)
            {
                return new ErrorResponse(e.Message);
            }
        }

        private Response handleADD_MEDICINE(AddMedicineRequest req)
        {
            Console.WriteLine("Add medicine request...");
            Medicine medicine = DtoUtils.GetFromDto(req.MedicineDto);
            try
            {
                lock (server)
                {
                    server.AddMedicine(medicine);
                }

                return new OkResponse();
            }
            catch (HospitalException e)
            {
                return new ErrorResponse(e.Message);
            }
        }

        private Response handleGET_ALL_MEDICINES(GetAllMedicinesRequest req)
        {
            Console.WriteLine("Get all medicines request...");
            try
            {
                IEnumerable<Medicine> medicines;
                lock (server)
                {
                    medicines = server.GetAllMedicines();
                }

                IList<MedicineDto> medicinesDto = DtoUtils.GetDto(medicines);
                return new GetAllMedicinesResponse(medicinesDto);
            }
            catch (HospitalException e)
            {
                return new ErrorResponse(e.Message);
            }
        }

        private Response handleFIND_PHARMACIST_BY_CREDENTIALS(FindPharmacistByCredentialsRequest req)
        {
            Console.WriteLine("Find pharmacist by credentials request...");
            string pharmacistName = req.PharmacistName;
            string pharmacistPassword = req.PharmacistPassword;
            try
            {
                Pharmacist pharmacist = null;
                lock (server)
                {
                    pharmacist = server.FindPharmacistByCredentials(pharmacistName, pharmacistPassword);
                }

                return new FindPharmacistByCredentialsResponse(DtoUtils.GetDto(pharmacist));
            }
            catch (HospitalException ex)
            {
                return new ErrorResponse(ex.Message);
            }
        }

        private Response handleLOGIN(LoginRequest req)
        {
            Console.WriteLine("Login request...");
            Pharmacist pharmacist = DtoUtils.GetFromDto(req.PharmacistDto);
            try
            {
                lock (server)
                {
                    server.Login(pharmacist, this);
                }
                return new OkResponse();
            }
            catch (HospitalException e)
            {
                connected = false;
                return new ErrorResponse(e.Message);
            }
        }

        public void Update_AddedMedicine(Medicine medicine)
        {
            try
            {
                MedicineDto medicineDto = DtoUtils.GetDto(medicine);
                sendResponse(new UpdateAddedMedicineResponse(medicineDto));
            }
            catch (Exception e)
            {
                Console.WriteLine(e.StackTrace);
            }
        }
        public void Update_AddedOrder(Order order)
        {
            try
            {
                OrderDto orderDto = DtoUtils.GetDto(order);
                sendResponse(new UpdateAddedOrderResponse(orderDto));
            }
            catch (Exception e)
            {
                Console.WriteLine(e.StackTrace);
            }
        }

        public void Update_UpdatedMedicine(Medicine medicine)
        {
            try
            {
                MedicineDto medicineDto = DtoUtils.GetDto(medicine);
                sendResponse(new UpdateUpdatedMedicineResponse(medicineDto));
            }
            catch (Exception e)
            {
                Console.WriteLine(e.StackTrace);
            }
        }
        public void Update_DeletedMedicine(Medicine medicine)
        {
            try
            {
                MedicineDto medicineDto = DtoUtils.GetDto(medicine);
                sendResponse(new UpdateDeletedMedicineResponse(medicineDto));
            }
            catch (Exception e)
            {
                Console.WriteLine(e.StackTrace);
            }
        }
    }
}