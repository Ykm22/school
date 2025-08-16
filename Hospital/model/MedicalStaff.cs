namespace model
{
    public class MedicalStaff : Identifiable
    {
        public virtual int Id { get; protected set; }
        public virtual string Name { get; set; }
        public virtual string Password { get; set; }

        public MedicalStaff()
        {
        }

        public MedicalStaff(string name, string password)
        {
            Name = name;
            Password = password;
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