using PetManagementService.Models;

namespace PetManagementService.DTOs
{
    public class VeterinaryCareResponse
    {
        public Guid Id { get; set; }
        public Guid PetId { get; set; }
        public string? Type { get; set; }

        public static VeterinaryCareResponse FromEntity(VeterinaryCare care)
        {
            return new VeterinaryCareResponse
            {
                Id = care.Id,
                PetId = care.PetId,
                Type = care.Type,
            };
        }
    }
}
