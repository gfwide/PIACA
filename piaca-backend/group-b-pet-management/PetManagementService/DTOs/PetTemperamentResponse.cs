using PetManagementService.Models;

namespace PetManagementService.DTOs
{
    public class PetTemperamentResponse
    {
        public Guid Id { get; set; }
        public Guid PetId { get; set; }
        public string? Type { get; set; }

        public static PetTemperamentResponse FromEntity(PetTemperament temperament)
        {
            return new PetTemperamentResponse
            {
                Id = temperament.Id,
                PetId = temperament.PetId,
                Type = temperament.Type,
            };
        }
    }
}
