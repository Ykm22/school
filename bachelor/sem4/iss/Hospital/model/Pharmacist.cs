namespace model
{
    public class Pharmacist : Identifiable
    {
        public virtual int Id { get; protected set; }
        public virtual string Name { get; set; }
        public virtual string Password { get; set; }

        public Pharmacist()
        {
        }

        public Pharmacist(string name, string password)
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