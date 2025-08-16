using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Formatters.Binary;
using System.ServiceModel.Channels;
using System.Threading;
using System.Windows.Forms;
using model;
using networking.DTO;
using networking.ObjectProtocol;
using services;
using Message = System.Windows.Forms.Message;

namespace networking
{
    public class ServerProxy : IServices
    {
        private string host;
        private int port;

        private IObserver client;
        private NetworkStream stream;

        private IFormatter formatter;
        private TcpClient connection;

        private Queue<Response> responses;
        private volatile bool finished;
        private EventWaitHandle _waitHandle;
        
        public ServerProxy(string Host, int Port)
        {
            host = Host;
            port = Port;
            this.responses = new Queue<Response>();
        }


        public void UpdateOrder(int orderId, OrderStatus orderStatus)
        {
            sendRequest(new UpdateOrderRequest(orderId, orderStatus));
            Response response = readResponse();
            if (response is ErrorResponse)
            {
                ErrorResponse err = (ErrorResponse)response;
                throw new HospitalException(err.Message);
            }
        }

        private void sendRequest(Request request)
        {
            try
            {
                // MessageBox.Show(request.ToString());
                formatter.Serialize(stream, request);
                stream.Flush();
            }
            catch (Exception e)
            {
                throw new HospitalException("Error sending object" + e);
            }
        }
        private Response readResponse()
        {
            Response response = null;
            try
            {
                _waitHandle.WaitOne();
                lock (responses)
                {
                    response = responses.Dequeue();
                    // MessageBox.Show("in proxy");
                    // MessageBox.Show(response.ToString());
                }
            }
            catch (Exception e)
            {
                Console.WriteLine(e.StackTrace);
            }

            return response;
        }
        private void initializeConnection()
        {
            try
            {
                connection = new TcpClient(host, port);
                stream = connection.GetStream();
                formatter = new BinaryFormatter();
                finished = false;
                _waitHandle = new AutoResetEvent(false);
                startReader();
            }
            catch (Exception e)
            {
                Console.WriteLine(e.StackTrace);
            }
        }
        private void closeConnection()
        {
            finished = true;
            try
            {
                stream.Close();
                connection.Close();
                _waitHandle.Close();
                client = null;
            }
            catch (Exception e)
            {
                Console.WriteLine(e.StackTrace);
            }
        }
        private void startReader()
        {
            Thread tw = new Thread(run);
            tw.Start();
        }
        public virtual void run()
        {
            while (!finished)
            {
                try
                {
                    object response = formatter.Deserialize(stream);
                    if (response is UpdateResponse)
                    {
                        handleUpdate((UpdateResponse)response);
                    }
                    else
                    {
                        lock (responses)
                        {
                            responses.Enqueue((Response)response);
                        }

                        _waitHandle.Set();
                    }
                }
                catch (Exception e)
                {
                    Console.WriteLine("Reading error" + e);
                }
            }
        }
        
        // todo
        private void handleUpdate(UpdateResponse Response)
        {
            try
            {
                if (Response is UpdateAddedOrderResponse)
                {
                    UpdateAddedOrderResponse resp = (UpdateAddedOrderResponse)Response;
                    Order addedOrder = DtoUtils.GetFromDto(resp.OrderDto);
                    client.Update_AddedOrder(addedOrder);
                }
                if (Response is UpdateAddedMedicineResponse)
                {
                    UpdateAddedMedicineResponse resp = (UpdateAddedMedicineResponse)Response;
                    Medicine addedMedicine = DtoUtils.GetFromDto(resp.MedicineDto);
                    client.Update_AddedMedicine(addedMedicine);
                }

                if (Response is UpdateUpdatedMedicineResponse)
                {
                    UpdateUpdatedMedicineResponse resp = (UpdateUpdatedMedicineResponse)Response;
                    Medicine updatedMedicine = DtoUtils.GetFromDto(resp.MedicineDto);
                    client.Update_UpdatedMedicine(updatedMedicine);
                }
                if (Response is UpdateDeletedMedicineResponse)
                {
                    UpdateDeletedMedicineResponse resp = (UpdateDeletedMedicineResponse)Response;
                    Medicine updatedMedicine = DtoUtils.GetFromDto(resp.MedicineDto);
                    client.Update_DeletedMedicine(updatedMedicine);
                }
                if (Response is UpdateUpdatedOrderResponse)
                {
                    // MessageBox.Show("ALOOOOOOOOO");
                    UpdateUpdatedOrderResponse resp = (UpdateUpdatedOrderResponse)Response;
                    Order updatedOrder = DtoUtils.GetFromDto(resp.OrderDto);
                    client.Update_UpdatedOrder(updatedOrder);
                }
            }
            catch (Exception e)
            {
                Console.WriteLine(e.StackTrace);
            }
        }

        public IEnumerable<Medicine> GetAllMedicines()
        {
            sendRequest(new GetAllMedicinesRequest());
            Response response = readResponse();
            if (response is ErrorResponse)
            {
                ErrorResponse err = (ErrorResponse)response;
                throw new HospitalException(err.Message);
            }

            GetAllMedicinesResponse resp = (GetAllMedicinesResponse)response;
            return DtoUtils.GetFromDto(resp.MedicinesDto);
        }
        
        public void AddMedicine(Medicine medicine)
        {
            MedicineDto medicineDto = DtoUtils.GetDto(medicine);
            sendRequest(new AddMedicineRequest(medicineDto));
            Response response = readResponse();
            if (response is ErrorResponse)
            {
                ErrorResponse err = (ErrorResponse)response;
                throw new HospitalException(err.Message);
            }
        }

        public List<Order> GetOrdersByMedicalStaffId(int medicalStaffId)
        {
            sendRequest(new GetOrdersByMedicalStaffIdRequest(medicalStaffId));
            Response response = readResponse();
            if (response is ErrorResponse)
            {
                ErrorResponse err = (ErrorResponse)response;
                throw new HospitalException(err.Message);
            }
            GetOrdersByMedicalStaffIdResponse resp = (GetOrdersByMedicalStaffIdResponse)response;
            return DtoUtils.GetFromDto(resp.OrdersDto).ToList();
        }

        public int AddOrder(Order order)
        {
            // MessageBox.Show("does it pass");
            OrderDto orderDto = DtoUtils.GetDto(order);
            // MessageBox.Show("it passed dto");
            sendRequest(new AddOrderRequest(orderDto));
            Response response = readResponse();
            if (response is ErrorResponse)
            {
                ErrorResponse err = (ErrorResponse)response;
                throw new HospitalException(err.Message);
            }

            AddOrderResponse resp = (AddOrderResponse)response;
            return resp.OrderId;
        }

        public void AddOrderMedicines(IList<OrderMedicine> orderMedicines)
        {
            IList<OrderMedicineDto> orderMedicinesDto = DtoUtils.GetDto(orderMedicines);
            sendRequest(new AddOrderMedicinesRequest(orderMedicinesDto));
            Response response = readResponse();
            // MessageBox.Show("Response read");
            if (response is ErrorResponse)
            {
                ErrorResponse err = (ErrorResponse)response;
                throw new HospitalException(err.Message);
            }
        }

        public Medicine FindMedicine(int id)
        {
            // MessageBox.Show("Sending find medicine request");
            sendRequest(new FindMedicineRequest(id));
            // MessageBox.Show("Request sent");
            Response response = readResponse();
            // MessageBox.Show("Response read");
            if (response is ErrorResponse)
            {
                ErrorResponse err = (ErrorResponse)response;
                throw new HospitalException(err.Message);
            }

            FindMedicineResponse resp = (FindMedicineResponse)response;
            MedicineDto medicineDto = resp.MedicineDto;
            return DtoUtils.GetFromDto(medicineDto);
        }
        public void UpdateMedicine(Medicine medicine, bool substract)
        {
            MedicineDto medicineDto = DtoUtils.GetDto(medicine);
            sendRequest(new UpdateMedicineRequest(medicineDto, substract));
            Response response = readResponse();
            if (response is ErrorResponse)
            {
                ErrorResponse err = (ErrorResponse)response;
                throw new HospitalException(err.Message);
            }
            
        }

        public List<Order> GetIncompleteOrders()
        {
            // MessageBox.Show("sending incomplete orders request");
            sendRequest(new GetIncompleteOrdersRequest());
            // MessageBox.Show("sent incomplete orders request");
            Response response = readResponse();
            // MessageBox.Show("read incomplete orders response");
            // MessageBox.Show("got response");
            if (response is ErrorResponse)
            {
                ErrorResponse err = (ErrorResponse)response;
                throw new HospitalException(err.Message);
            }

            GetIncompleteOrdersResponse resp = (GetIncompleteOrdersResponse)response;
            return DtoUtils.GetFromDto(resp.OrdersDto);
        }

        public List<Medicine> GetOrderMedicines(int orderId)
        {
            sendRequest(new GetOrderMedicinesRequest(orderId));
            Response response = readResponse();
            if (response is ErrorResponse)
            {
                ErrorResponse err = (ErrorResponse)response;
                throw new HospitalException(err.Message);
            }
            GetOrderMedicinesResponse resp = (GetOrderMedicinesResponse)response;
            return DtoUtils.GetFromDto(resp.MedicinesDto).ToList();
        }

        public void DeleteMedicine(int id)
        {
            sendRequest(new DeleteMedicineRequest(id));
            Response response = readResponse();
            if (response is ErrorResponse)
            {
                ErrorResponse err = (ErrorResponse)response;
                throw new HospitalException(err.Message);
            }
        }

        public IEnumerable<Medicine> FilterMedicines(Purpose purpose)
        {
            sendRequest(new FilterMedicinesRequest(purpose));
            Response response = readResponse();
            if (response is ErrorResponse)
            {
                ErrorResponse err = (ErrorResponse)response;
                throw new HospitalException(err.Message);
            }

            FilterMedicinesResponse resp = (FilterMedicinesResponse)response;
            IList<Medicine> medicines =  DtoUtils.GetFromDto(resp.MedicinesDto);
            return medicines;
        }

        public Pharmacist Login(Pharmacist pharmacist, IObserver client)
        {
            initializeConnection();
            Pharmacist foundPharmacist = FindPharmacistByCredentials(pharmacist.Name, pharmacist.Password);
            PharmacistDto pharmacistDto = DtoUtils.GetDto(foundPharmacist);
            sendRequest(new LoginRequest(pharmacistDto));
            
            Response response = readResponse();
            if (response is OkResponse)
            {
                this.client = client;
                return foundPharmacist;
            }

            if (response is ErrorResponse)
            {
                ErrorResponse err = (ErrorResponse)response;
                closeConnection();
                throw new HospitalException(err.Message);
            }

            return null;
        }

        public MedicalStaff LoginMedicalStaff(MedicalStaff medicalStaff, IObserver client)
        {
            initializeConnection();
            MedicalStaff foundMedicalStaff = FindMedicalStaffByCredentials(medicalStaff.Name, medicalStaff.Password);
            MedicalStaffDto medicalStaffDto = DtoUtils.GetDto(foundMedicalStaff);
            sendRequest(new LoginMedicalStaffRequest(medicalStaffDto));
            
            Response response = readResponse();
            
            if (response is OkResponse)
            {
                this.client = client;
                return foundMedicalStaff;
            }

            if (response is ErrorResponse)
            {
                ErrorResponse err = (ErrorResponse)response;
                closeConnection();
                throw new HospitalException(err.Message);
            }

            return null;
        }
        public Pharmacist FindPharmacistByCredentials(string pharmacistName, string pharmacistPassword)
        {
            // MessageBox.Show("Sending request!");
            sendRequest(new FindPharmacistByCredentialsRequest(pharmacistName, pharmacistPassword));
            // MessageBox.Show("Sending request!");
            Response response = readResponse();
            // MessageBox.Show("Sending request!");
            if (response is ErrorResponse)
            {
                ErrorResponse err = (ErrorResponse)response;
                closeConnection();
                throw new HospitalException(err.Message);
            }

            FindPharmacistByCredentialsResponse resp = (FindPharmacistByCredentialsResponse)response;
            PharmacistDto pharmacistDto = resp.PharmacistDto;
            Pharmacist pharmacist = DtoUtils.GetFromDto(pharmacistDto);
            return pharmacist;
        }

        public MedicalStaff FindMedicalStaffByCredentials(string medicalStaffName, string medicalStaffPassword)
        {
            // MessageBox.Show("sending request NOW!");
            sendRequest(new FindMedicalStaffByCredentialsRequest(medicalStaffName, medicalStaffPassword));
            Response response = readResponse();
            if (response is ErrorResponse)
            {
                ErrorResponse err = (ErrorResponse)response;
                closeConnection();
                throw new HospitalException(err.Message);
            }
            

            FindMedicalStaffByCredentialsResponse resp = (FindMedicalStaffByCredentialsResponse)response;
            // MessageBox.Show(resp.ToString());
            MedicalStaffDto medicalStaffDto = resp.MedicalStaffDto;
            MedicalStaff medicalStaff = DtoUtils.GetFromDto(medicalStaffDto);
            // MessageBox.Show(medicalStaff.ToString());
            return medicalStaff;
        }

        public void Logout(Pharmacist pharmacist, IObserver client)
        {
            PharmacistDto pharmacistDto = DtoUtils.GetDto(pharmacist);
            sendRequest(new LogoutRequest(pharmacistDto));
            Response response = readResponse();
            closeConnection();
            if (response is ErrorResponse)
            {
                ErrorResponse err = (ErrorResponse)response;
                throw new HospitalException(err.Message);
            }
        }

        public void LogoutMedicalStaff(MedicalStaff medicalStaff, IObserver client)
        {
            MedicalStaffDto medicalStaffDto = DtoUtils.GetDto(medicalStaff);
            sendRequest(new LogoutMedicalStaffRequest(medicalStaffDto));
            Response response = readResponse();
            closeConnection();
            if (response is ErrorResponse)
            {
                ErrorResponse err = (ErrorResponse)response;
                throw new HospitalException(err.Message);
            }
        }
    }
}