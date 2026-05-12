using PetManagementService.Models;

namespace PetManagementService.DTOs
{
public class PetFullInfoResponse
{
    public PetResponse Pet { get; set; } = null!;
    public PetDetailsResponse? Details { get; set; }
    public List<PetDiseaseResponse> Diseases { get; set; } = new();
    public List<PetTemperamentResponse> Temperaments { get; set; } = new();
    public List<PetSociabilityResponse> Sociabilities { get; set; } = new();
    public List<VeterinaryCareResponse> VeterinaryCares { get; set; } = new();

    public static PetFullInfoResponse FromEntity(Pet pet)
    {
        return new PetFullInfoResponse
        {
            Pet = PetResponse.FromEntity(pet),
            Details = pet.Details != null ? PetDetailsResponse.FromEntity(pet.Details) : null,
            Diseases = pet.Diseases?.Select(PetDiseaseResponse.FromEntity).ToList() ?? new(),
            Temperaments = pet.Temperament?.Select(PetTemperamentResponse.FromEntity).ToList() ?? new(),
            Sociabilities = pet.Sociability?.Select(PetSociabilityResponse.FromEntity).ToList() ?? new(),
            VeterinaryCares = pet.VeterinaryCare?.Select(VeterinaryCareResponse.FromEntity).ToList() ?? new(),
        };
    }
}
}