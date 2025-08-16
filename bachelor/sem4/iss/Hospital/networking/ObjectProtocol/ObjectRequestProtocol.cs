using System;
using System.Collections.Generic;
using model;
using networking.DTO;

namespace networking.ObjectProtocol
{
    public interface Request {}
    [Serializable]
    public class LoginRequest : Request
    {
        private PharmacistDto pharmacistDto;

        public LoginRequest(PharmacistDto pharmacistDto)
        {
            this.pharmacistDto = pharmacistDto;
        }

        public virtual PharmacistDto PharmacistDto
        {
            get
            {
                return pharmacistDto;
            }
        }
    }
    [Serializable]
    public class LoginMedicalStaffRequest : Request
    {
        private MedicalStaffDto medicalStaffDto;

        public LoginMedicalStaffRequest(MedicalStaffDto medicalStaffDto)
        {
            this.medicalStaffDto = medicalStaffDto;
        }

        public virtual MedicalStaffDto MedicalStaffDto
        {
            get
            {
                return medicalStaffDto;
            }
        }
    }
    [Serializable]
    public class AddMedicineRequest : Request
    {
        private MedicineDto medicineDto;

        public AddMedicineRequest(MedicineDto medicineDto)
        {
            this.medicineDto = medicineDto;
        }

        public virtual MedicineDto MedicineDto
        {
            get
            {
                return medicineDto;
            }
        }
    }
    [Serializable]
    public class AddOrderRequest : Request
    {
        private OrderDto orderDto;

        public AddOrderRequest(OrderDto orderDto)
        {
            this.orderDto = orderDto;
        }

        public virtual OrderDto OrderDto
        {
            get
            {
                return orderDto;
            }
        }
    }
    [Serializable]
    public class AddOrderMedicinesRequest : Request
    {
        private IList<OrderMedicineDto> orderMedicinesDto;

        public AddOrderMedicinesRequest(IList<OrderMedicineDto> orderMedicinesDto)
        {
            this.orderMedicinesDto = orderMedicinesDto;
        }

        public virtual IList<OrderMedicineDto> OrderMedicinesDto
        {
            get
            {
                return orderMedicinesDto;
            }
        }
    }
    [Serializable]
    public class GetOrderMedicinesRequest : Request
    {
        private int orderId;

        public GetOrderMedicinesRequest(int orderId)
        {
            this.orderId = orderId;
        }

        public virtual int OrderId
        {
            get
            {
                return orderId;
            }
        }
    }
    [Serializable]
    public class UpdateMedicineRequest : Request
    {
        private MedicineDto medicineDto;
        private bool substract;

        public UpdateMedicineRequest(MedicineDto medicineDto, bool substract)
        {
            this.medicineDto = medicineDto;
            this.substract = substract;
        }

        public virtual MedicineDto MedicineDto
        {
            get
            {
                return medicineDto;
            }
        }
        public virtual bool Substract
        {
            get
            {
                return substract;
            }
        }
    }
    [Serializable]
    public class UpdateOrderRequest : Request
    {
        private int orderId;
        private OrderStatus orderStatus;

        public UpdateOrderRequest(int orderId, OrderStatus orderStatus)
        {
            this.orderId = orderId;
            this.orderStatus = orderStatus;
        }

        public virtual int OrderId
        {
            get
            {
                return orderId;
            }
        }
        public virtual OrderStatus OrderStatus
        {
            get
            {
                return orderStatus;
            }
        }
    }
    [Serializable]
    public class DeleteMedicineRequest : Request
    {
        private int idToDelete;

        public DeleteMedicineRequest(int IdToDelete)
        {
            idToDelete = IdToDelete;
        }

        public virtual int IdToDelete
        {
            get
            {
                return idToDelete;
            }
        }
    }
    [Serializable]
    public class GetOrdersByMedicalStaffIdRequest : Request
    {
        private int medicalStaffId;

        public GetOrdersByMedicalStaffIdRequest(int medicalStaffId)
        {
            this.medicalStaffId = medicalStaffId;
        }

        public virtual int MedicalStaffId
        {
            get
            {
                return medicalStaffId;
            }
        }
    }
    [Serializable]
    public class FilterMedicinesRequest : Request
    {
        private Purpose purpose;

        public FilterMedicinesRequest(Purpose purpose)
        {
            this.purpose = purpose;
        }

        public virtual Purpose Purpose
        {
            get
            {
                return purpose;
            }
        }
    }
    [Serializable]
    public class GetAllMedicinesRequest : Request
    {
        public GetAllMedicinesRequest()
        {
            
        }
    }
    [Serializable]
    public class GetIncompleteOrdersRequest : Request
    {
        public GetIncompleteOrdersRequest()
        {
            
        }
    }
    
    [Serializable]
    public class FindPharmacistByCredentialsRequest : Request
    {
        private string pharmacistName;
        private string pharmacistPassword;

        public FindPharmacistByCredentialsRequest(string pharmacistName, string pharmacistPassword)
        {
            this.pharmacistName = pharmacistName;
            this.pharmacistPassword = pharmacistPassword;
        }

        public virtual string PharmacistName
        {
            get
            {
                return pharmacistName;
            }
        }
        public virtual string PharmacistPassword
        {
            get
            {
                return pharmacistPassword;
            }
        }
    }
    [Serializable]
    public class FindMedicalStaffByCredentialsRequest : Request
    {
        private string medicalStaffName;
        private string medicalStaffPassword;

        public FindMedicalStaffByCredentialsRequest(string medicalStaffName, string medicalStaffPassword)
        {
            this.medicalStaffName = medicalStaffName;
            this.medicalStaffPassword = medicalStaffPassword;
        }

        public virtual string MedicalStaffName
        {
            get
            {
                return medicalStaffName;
            }
        }
        public virtual string MedicalStaffPassword
        {
            get
            {
                return medicalStaffPassword;
            }
        }
    }
    [Serializable]
    public class LogoutRequest : Request
    {
        private PharmacistDto pharmacistDto;

        public LogoutRequest(PharmacistDto pharmacistDto)
        {
            this.pharmacistDto = pharmacistDto;
        }

        public virtual PharmacistDto PharmacistDto
        {
            get
            {
                return pharmacistDto;
            }
        }
    }
    [Serializable]
    public class LogoutMedicalStaffRequest : Request
    {
        private MedicalStaffDto medicalStaffDto;

        public LogoutMedicalStaffRequest(MedicalStaffDto medicalStaffDto)
        {
            this.medicalStaffDto = medicalStaffDto;
        }

        public virtual MedicalStaffDto MedicalStaffDto
        {
            get
            {
                return medicalStaffDto;
            }
        }
    }
    [Serializable]
    public class FindMedicineRequest : Request
    {
        private int id;

        public FindMedicineRequest(int Id)
        {
            this.id = Id;
        }

        public virtual int Id
        {
            get
            {
                return id;
            }
        }
    }
}