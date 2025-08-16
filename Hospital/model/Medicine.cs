using System;
using System.Collections.Generic;

namespace model
{
    public class Medicine : Identifiable
    {
        public virtual int Id { get; protected set; }
        public virtual Purpose Purpose { get; set; }
        public virtual string Name { get; set; }
        public virtual int AvailableQuantity { get; set; }
        
        public virtual IList<Order> Orders { get; set; } = new List<Order>();
        public Medicine()
        {
        }

        public Medicine(Purpose purpose, string name, int availableQuantity)
        {
            Purpose = purpose;
            Name = name;
            AvailableQuantity = availableQuantity;
        }

        public virtual int GetId()
        {
            return Id;
        }

        public virtual void SetId(int id)
        {
            this.Id = id;
        }
    }
}