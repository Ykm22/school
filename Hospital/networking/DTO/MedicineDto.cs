using System;
using model;

namespace networking.DTO
{
    [Serializable]
    public class MedicineDto
    {
        public int Id { get; set; }
        public Purpose Purpose { get; set; }
        public string Name { get; set; }
        public int AvailableQuantity { get; set; }

        public MedicineDto(int id, Purpose purpose, string name, int availableQuantity)
        {
            Id = id;
            Purpose = purpose;
            Name = name;
            AvailableQuantity = availableQuantity;
        }
    }
    
}