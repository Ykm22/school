using FluentNHibernate.Mapping;

namespace model
{
    public class MedicalStaffMap : ClassMap<MedicalStaff>
    {
        public MedicalStaffMap()
        {
            Table("MedicalStaffMembers");
            Id(ms => ms.Id);
            Map(ms => ms.Name);
            Map(ms => ms.Password);
        }
    }
}