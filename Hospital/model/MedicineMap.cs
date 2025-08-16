    using FluentNHibernate.Mapping;

    namespace model
    {
        public class MedicineMap : ClassMap<Medicine>
        {
            public MedicineMap()
            {
                Table("Medicines");
                Id(m => m.Id).Column("Id");
                Map(m => m.Name);
                Map(m => m.Purpose);
                Map(m => m.AvailableQuantity);
                HasManyToMany(x => x.Orders)
                    .Table("Order_Medicine")
                    .ParentKeyColumn("MedicineId")
                    .ChildKeyColumn("OrderId")
                    .Cascade.All();
            }
        }
    }