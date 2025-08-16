namespace model
{
    public class OrderMedicine : Identifiable
    {
        public virtual int Id { get; set; }
        public virtual int orderId { get; set; }
        public virtual int medicineId { get; protected set; }
        public virtual int Quantity { get; set; }

        public virtual int GetId()
        {
            return Id;
        }

        public virtual void SetId(int id)
        {
            this.Id = Id;
        }

        public OrderMedicine(int orderId, int medicineId, int Quantity)
        {
            this.orderId = orderId;
            this.medicineId = medicineId;
            this.Quantity = Quantity;
        }

        public OrderMedicine()
        {
            
        }
    }
}