using FluentNHibernate.Mapping;

namespace model
{
    public class OrderMap : ClassMap<Order>
    {
        public OrderMap()
        {
            Table("Orders");
            Id(x => x.Id).GeneratedBy.Identity();
            Map(x => x.TimeSent);
            Map(x => x.OrderStatus);
            Map(x => x.medicalStaffId);
            
            HasMany(x => x.OrderMedicines)
                .Table("Order_Medicine")
                .KeyColumn("OrderId")
                .Inverse()
                .Cascade.AllDeleteOrphan()
                .Not.LazyLoad();

        }
    }
}