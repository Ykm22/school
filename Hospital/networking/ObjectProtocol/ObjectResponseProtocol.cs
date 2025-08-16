using System;
using System.Collections.Generic;
using model;
using networking.DTO;

namespace networking.ObjectProtocol
{
    public interface Response{ }
    public interface UpdateResponse : Response
    {
    }

    [Serializable]
    public class UpdateAddedMedicineResponse : UpdateResponse
    {
        private MedicineDto medicineDto;

        public UpdateAddedMedicineResponse(MedicineDto medicineDto)
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
    public class UpdateAddedOrderResponse : UpdateResponse
    {
        private OrderDto orderDto;

        public UpdateAddedOrderResponse(OrderDto orderDto)
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
    public class UpdateUpdatedMedicineResponse : UpdateResponse
    {
        private MedicineDto medicineDto;

        public UpdateUpdatedMedicineResponse(MedicineDto medicineDto)
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
    public class GetOrdersByMedicalStaffIdResponse : Response
    {
        private List<OrderDto> ordersDto;

        public GetOrdersByMedicalStaffIdResponse(List<OrderDto> ordersDto)
        {
            this.ordersDto = ordersDto;
        }

        public virtual List<OrderDto> OrdersDto
        {
            get
            {
                return ordersDto;
            }
        }
    }
    [Serializable]
    public class UpdateUpdatedOrderResponse : UpdateResponse
    {
        private OrderDto orderDto;

        public UpdateUpdatedOrderResponse( OrderDto orderDto)
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
    public class UpdateDeletedMedicineResponse : UpdateResponse
    {
        private MedicineDto medicineDto;

        public UpdateDeletedMedicineResponse(MedicineDto medicineDto)
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
    public class GetAllMedicinesResponse : Response
    {
        private IList<MedicineDto> medicinesDto;

        public GetAllMedicinesResponse(IList<MedicineDto> medicinesDto)
        {
            this.medicinesDto = medicinesDto;
        }

        public virtual IList<MedicineDto> MedicinesDto
        {
            get
            {
                return medicinesDto;
            }
        }
    }
    [Serializable]
    public class GetOrderMedicinesResponse : Response
    {
        private IList<MedicineDto> medicinesDto;

        public GetOrderMedicinesResponse(IList<MedicineDto> medicinesDto)
        {
            this.medicinesDto = medicinesDto;
        }

        public virtual IList<MedicineDto> MedicinesDto
        {
            get
            {
                return medicinesDto;
            }
        }
    }
    [Serializable]
    public class AddOrderResponse : Response
    {
        private int orderId;

        public AddOrderResponse(int orderId)
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
    public class GetIncompleteOrdersResponse : Response
    {
        private IList<OrderDto> ordersDto;

        public GetIncompleteOrdersResponse(IList<OrderDto> ordersDto)
        {
            this.ordersDto = ordersDto;
        }

        public virtual  IList<OrderDto> OrdersDto
        {
            get
            {
                return ordersDto;
            }
        }
    }
    [Serializable]
    public class FindMedicineResponse : Response
    {
        private MedicineDto medicineDto;

        public FindMedicineResponse(MedicineDto medicineDto)
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
    public class FilterMedicinesResponse : Response
    {
        private IList<MedicineDto> medicinesDto;

        public FilterMedicinesResponse(IList<MedicineDto> medicinesDto)
        {
            this.medicinesDto = medicinesDto;
        }

        public virtual IList<MedicineDto> MedicinesDto
        {
            get
            {
                return medicinesDto;
            }
        }
    }
    [Serializable]
    public class OkResponse : Response
    { }
    [Serializable]
    public class ErrorResponse : Response
    {
        private string message;

        public ErrorResponse(string Message)
        {
            message = Message;
        }

        public virtual string Message
        {
            get
            {
                return message;
            }
        }
    }
    [Serializable]
    public class FindPharmacistByCredentialsResponse : Response
    {
        private PharmacistDto pharmacistDto;

        public FindPharmacistByCredentialsResponse(PharmacistDto pharmacistDto)
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
    public class FindMedicalStaffByCredentialsResponse : Response
    {
        private MedicalStaffDto medicalStaffDto;

        public FindMedicalStaffByCredentialsResponse(MedicalStaffDto medicalStaffDto)
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
}