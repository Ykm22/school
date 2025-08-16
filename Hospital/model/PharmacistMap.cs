using FluentNHibernate.Mapping;
using model;

namespace model
{
    public class PharmacistMap : ClassMap<Pharmacist>
    {
        public PharmacistMap()
        {
            Table("Pharmacists");
            Id(p => p.Id);
            Map(p => p.Name);
            Map(p => p.Password);
        }
    }
}