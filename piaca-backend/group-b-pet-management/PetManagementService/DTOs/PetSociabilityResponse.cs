using PetManagementService.Models;

namespace PetManagementService.DTOs
{
    public class PetSociabilityResponse
    {
        public Guid Id { get; set; }
        public Guid PetId { get; set; }
        public string? Title { get; set; }

        public static PetSociabilityResponse FromEntity(PetSociability sociability)
        {
            return new PetSociabilityResponse
            {
                Id = sociability.Id,
                PetId = sociability.PetId,
                Title = sociability.Title,
            };
        }
    }
}
