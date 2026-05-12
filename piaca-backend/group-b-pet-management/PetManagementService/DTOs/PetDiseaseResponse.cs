using PetManagementService.Models;

namespace PetManagementService.DTOs
{
    public class PetDiseaseResponse
    {
        public Guid Id { get; set; }
        public Guid PetId { get; set; }
        public string? Name { get; set; }

        public static PetDiseaseResponse FromEntity(PetDisease disease)
        {
            return new PetDiseaseResponse
            {
                Id = disease.Id,
                PetId = disease.PetId,
                Name = disease.Name,
            };
        }
    }
}
