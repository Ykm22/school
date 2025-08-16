using System;

namespace networking.DTO
{
    [Serializable]
    public class MedicalStaffDto
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Password { get; set; }

        public MedicalStaffDto(int id, string name, string password)
        {
            Id = id;
            Name = name;
            Password = password;
        }
    }
}