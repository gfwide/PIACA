using PetManagementService.Models;

namespace PetManagementService.DTOs
{
    public class ImageResponse
    {
        public Guid Id { get; set; }
        public string? FileName { get; set; }
        public string? S3Url { get; set; }
        public Guid? PetId { get; set; }

        public static ImageResponse FromEntity(Image image)
        {
            return new ImageResponse
            {
                Id = image.Id,
                FileName = image.FileName,
                S3Url = image.S3Url,
                PetId = image.PetId,
            };
        }
    }
}
