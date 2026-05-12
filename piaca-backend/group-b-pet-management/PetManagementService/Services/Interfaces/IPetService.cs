using PetManagementService.DTOs;

namespace PetManagementService.Services
{
    public interface IPetService
    {
        Task<List<PetResponse>> GetAllPetsAsync();
        Task<PetResponse?> GetSinglePetAsync(Guid petId);
        Task<PetDetailsResponse?> GetPetDetailsAsync(Guid petId);
        Task<PetFullInfoResponse?> GetPetFullInfoAsync(Guid petId);
    }
}