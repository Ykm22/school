using FluentNHibernate.Mapping;

namespace model
{
    public class OrderMedicineMap : ClassMap<OrderMedicine>
    {
        public OrderMedicineMap()
        {
            Table("Order_Medicine");
            Id(x => x.Id).GeneratedBy.Identity();
            Map(x => x.orderId).Column("OrderId");
            Map(x => x.medicineId).Column("MedicineId");
            Map(x => x.Quantity);

        }
    }
}