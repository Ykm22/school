using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;
using model;
using NHibernate;

namespace networking.DTO
{
    public class DtoUtils
    {
        public static OrderDto GetDto(Order order)
        {
            OrderDto orderDto = new OrderDto(order.Id,
                GetDto(order.OrderMedicines),
                order.TimeSent,
                order.OrderStatus,
                order.medicalStaffId);
            return orderDto;

        }
        public static Order GetFromDto(OrderDto orderDto)
        {
            Order order = new Order();
            order.SetId(orderDto.Id);
            order.OrderMedicines = GetFromDto(orderDto.orderMedicinesDto);
            order.OrderStatus = orderDto.orderStatus;
            order.TimeSent = orderDto.timeSent;
            order.medicalStaffId = orderDto.medicalStaffId;
            return order;
        }
        
        public static List<OrderDto> GetDto(IList<Order> orders)
        {
            List<OrderDto> ordersDto = new List<OrderDto>();
            foreach (var order in orders)
            {
                OrderDto orderDto = GetDto(order);
                ordersDto.Add(orderDto);
            }

            return ordersDto;
        }
        public static List<Order> GetFromDto(IList<OrderDto> orderDtos)
        {
            return orderDtos.Select(orderDto => GetFromDto(orderDto)).ToList();
        }
        public static Medicine GetFromDto(MedicineDto medicineDto)
        {
            Medicine medicine = new Medicine(
                medicineDto.Purpose,
                medicineDto.Name,
                medicineDto.AvailableQuantity);
            medicine.SetId(medicineDto.Id);
            return medicine;
        }

        public static MedicineDto GetDto(Medicine medicine)
        {
            return new MedicineDto(
                medicine.GetId(),
                medicine.Purpose,
                medicine.Name,
                medicine.AvailableQuantity);
        }
        
        public static OrderMedicine GetFromDto(OrderMedicineDto orderMedicineDto)
        {
            OrderMedicine orderMedicine = new OrderMedicine(
                orderMedicineDto.OrderId,
                orderMedicineDto.MedicineId,
                orderMedicineDto.Quantity);
            orderMedicine.SetId(orderMedicine.Id);
            return orderMedicine;
        }
        public static List<OrderMedicine> GetFromDto(IList<OrderMedicineDto> orderMedicinesDto)
        {
            List<OrderMedicine> orderMedicines = new List<OrderMedicine>();
            foreach (OrderMedicineDto orderMedicineDto in orderMedicinesDto)
            {
                OrderMedicine orderMedicine = GetFromDto(orderMedicineDto);
                orderMedicines.Add(orderMedicine);
            }
            return orderMedicines;
        }

        public static List<OrderMedicineDto> GetDto(IList<OrderMedicine> orderMedicines)
        {
            List<OrderMedicineDto> orderMedicinesDto = new List<OrderMedicineDto>();
            // NHibernateUtil.Initialize(orderMedicines);
            foreach (var orderMedicine in orderMedicines)
            {
                OrderMedicineDto orderMedicineDto = GetDto(orderMedicine);
                orderMedicinesDto.Add(orderMedicineDto);
            }
            return orderMedicinesDto;
        }


        public static OrderMedicineDto GetDto(OrderMedicine orderMedicine)
        {
            OrderMedicineDto orderMedicineDto = new OrderMedicineDto(
                orderMedicine.Id,
                orderMedicine.orderId,
                orderMedicine.medicineId,
                orderMedicine.Quantity);
            return orderMedicineDto;
        }
        

        public static Pharmacist GetFromDto(PharmacistDto pharmacistDto)
        {
            Pharmacist pharmacist = new Pharmacist(
                pharmacistDto.Name,
                pharmacistDto.Password);
            pharmacist.SetId(pharmacistDto.Id);
            return pharmacist;
        }

        public static PharmacistDto GetDto(Pharmacist pharmacist)
        {
            return new PharmacistDto(
                pharmacist.GetId(),
                pharmacist.Name,
                pharmacist.Password);
        }
        public static IList<Medicine> GetFromDto(IList<MedicineDto> medicinesDto){
            IList<Medicine> medicines = new List<Medicine>();
            foreach(MedicineDto medicineDto in medicinesDto){
                Medicine medicine = GetFromDto(medicineDto);
                medicines.Add(medicine);
            }
            return medicines;
        }
        public static IList<MedicineDto> GetDto(IEnumerable<Medicine> medicines){
            IList<MedicineDto> medicinesDto = new List<MedicineDto>();
            foreach(Medicine medicine in medicines){
                MedicineDto medicineDto = GetDto(medicine);
                medicinesDto.Add(medicineDto);
            }
            return medicinesDto;
        }
        // public static IList<Order> GetFromDto(IList<OrderDto> ordersDto){
        //     IList<Order> orders = new List<Order>();
        //     foreach(OrderDto orderDto in ordersDto){
        //         Order order = GetFromDto(orderDto);
        //         orders.Add(order);
        //     }
        //     return orders;
        // }
        // public static IList<OrderDto> GetDto(IEnumerable<Order> orders){
        //     IList<OrderDto> ordersDto = new List<OrderDto>();
        //     foreach(Order order in orders){
        //         OrderDto orderDto = GetDto(order);
        //         ordersDto.Add(orderDto);
        //     }
        //     return ordersDto;
        // }
        
        public static MedicalStaff GetFromDto(MedicalStaffDto medicalStaffDto)
        {
            MedicalStaff medicalStaff = new MedicalStaff(
                medicalStaffDto.Name,
                medicalStaffDto.Password);
            medicalStaff.SetId(medicalStaffDto.Id);
            return medicalStaff;
        }

        public static MedicalStaffDto GetDto(MedicalStaff medicalStaff)
        {
            return new MedicalStaffDto(
                medicalStaff.GetId(),
                medicalStaff.Name,
                medicalStaff.Password);
        }
    }
}