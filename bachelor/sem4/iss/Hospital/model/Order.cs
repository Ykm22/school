using System;
using System.Collections.Generic;

namespace model
{
    public enum OrderStatus
    {
        Incomplete,
        Completed
    }
    
    public class Order : Identifiable
    {
        public virtual int Id { get; protected set; }

        public virtual IList<OrderMedicine> OrderMedicines { get; set; }
            = new List<OrderMedicine>();

        public virtual DateTime TimeSent { get; set; }
        public virtual OrderStatus OrderStatus { get; set; }
        public virtual int medicalStaffId { get; set; }

        public virtual int GetId()
        {
            return Id;
        }

        public virtual void SetId(int id)
        {
            this.Id = id;
        }

        public Order()
        {
            OrderMedicines = new List<OrderMedicine>();
        }
    }
}