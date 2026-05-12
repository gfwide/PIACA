using PetManagementService.Models;

namespace PetManagementService.DTOs
{
    public class PetResponse
    {
        public Guid Id { get; set; }
        public Guid? NgoId { get; set; }
        public Guid? ProtectorId { get; set; }
        public int Status { get; set; }
        public string? Species { get; set; }
        public string? Name { get; set; }
        public string? Age { get; set; }
        public DateTime? BirthDate { get; set; }
        public string? IdLink { get; set; }
        public char Gender { get; set; }
        public string? Description { get; set; }
        public string? City { get; set; }
        public string? State { get; set; }

        public static PetResponse FromEntity(Pet pet)
        {
            return new PetResponse
            {
                Id = pet.Id,
                NgoId = pet.NgoId,
                ProtectorId = pet.ProtectorId,
                Status = pet.Status,
                Species = pet.Species,
                Name = pet.Name,
                Age = pet.Age,
                BirthDate = pet.BirthDate,
                IdLink = pet.IdLink,
                Gender = pet.Gender,
                Description = pet.Description,
                City = pet.City,
                State = pet.State,
            };
        }
    }
}
