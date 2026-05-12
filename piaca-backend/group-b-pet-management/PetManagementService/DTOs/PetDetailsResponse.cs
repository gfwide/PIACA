using PetManagementService.Models;

namespace PetManagementService.DTOs
{
    public class PetDetailsResponse
    {
        public Guid Id { get; set; }
        public Guid PetId { get; set; }
        public string? Breed { get; set; }
        public string? Size { get; set; }
        public float? Weight { get; set; }
        public string? Coat { get; set; }
        public string? Color { get; set; }
        public string? Reactivity { get; set; }
        public bool? Microchip { get; set; }

        public static PetDetailsResponse FromEntity(PetDetails details)
        {
            return new PetDetailsResponse
            {
                Id = details.Id,
                PetId = details.PetId,
                Breed = details.Breed,
                Size = details.Size,
                Weight = details.Weight,
                Coat = details.Coat,
                Color = details.Color,
                Reactivity = details.Reactivity,
                Microchip = details.Microchip,
            };
        }
    }
}
