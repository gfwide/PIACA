using PetManagementService.Models;

namespace PetManagementService.DTOs
{
    public class OccurrenceResponse
    {
        public Guid Id { get; set; }
        public Guid PetId { get; set; }
        public string? Type { get; set; }
        public string? Title { get; set; }
        public DateTime? Date { get; set; }
        public string? Description { get; set; }

        public static OccurrenceResponse FromEntity(Occurrence occurrence)
        {
            return new OccurrenceResponse
            {
                Id = occurrence.Id,
                PetId = occurrence.PetId,
                Type = occurrence.Type,
                Title = occurrence.Title,
                Date = occurrence.Date,
                Description = occurrence.Description,
            };
        }
    }
}
