using System;

namespace networking.DTO
{
    [Serializable]
    public class OrderMedicineDto
    {
        public int Id { get; set; }
        public int OrderId { get; set; }
        public int MedicineId { get; set; }
        public int Quantity { get; set; }

        public OrderMedicineDto(int id, int orderId, int medicineId, int quantity)
        {
            Id = id;
            OrderId = orderId;
            MedicineId = medicineId;
            Quantity = quantity;
        }
    }
}