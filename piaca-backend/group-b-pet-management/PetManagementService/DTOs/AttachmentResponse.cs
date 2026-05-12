using PetManagementService.Models;

namespace PetManagementService.DTOs
{
    public class AttachmentResponse
    {
        public Guid Id { get; set; }
        public Guid OccurrenceId { get; set; }
        public string? FileName { get; set; }
        public string? S3Url { get; set; }

        public static AttachmentResponse FromEntity(Attachment attachment)
        {
            return new AttachmentResponse
            {
                Id = attachment.Id,
                OccurrenceId = attachment.OccurrenceId,
                FileName = attachment.FileName,
                S3Url = attachment.S3Url,
            };
        }
    }
}
