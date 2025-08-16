using System;
using System.Collections.Generic;
using model;

namespace networking.DTO
{
    [Serializable]
    public class OrderDto
    {
        public int medicalStaffId { get; set; }
        public int Id { get; set; }
        public IList<OrderMedicineDto> orderMedicinesDto { get; set; }
        public DateTime timeSent { get; set; }
        public OrderStatus orderStatus { get; set; }

        public OrderDto(int id, IList<OrderMedicineDto> orderMedicinesDto, DateTime timeSent, OrderStatus orderStatus, int medicalStaffId)
        {
            Id = id;
            this.orderMedicinesDto = orderMedicinesDto;
            this.timeSent = timeSent;
            this.orderStatus = orderStatus;
            this.medicalStaffId = medicalStaffId;
        }
    }
}