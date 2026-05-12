namespace PetManagementService.DTOs
{
    public class UpdatePetRequest
    {
        public Guid Id { get; set; }
        public string? Name { get; set; }
        public string? Species { get; set; }
        public int? Age { get; set; }
        public string? Breed { get; set; }
    }
}