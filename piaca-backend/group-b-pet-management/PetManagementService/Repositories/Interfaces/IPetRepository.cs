using PetManagementService.Models;
using PetManagementService.DTOs;

namespace PetManagementService.Repositories
{
    public interface IPetRepository
    {
        Task<List<Pet>> GetAllPetsAsync();
        Task<Pet?> GetSinglePetAsync(Guid petId);
        Task<PetDetails?> GetPetDetailsAsync(Guid petId);
        Task<Pet?> GetPetFullInfoAsync(Guid petId);
        // Task<List<Pet>> GetPetsByFilterAsync(FilterPetsRequest filter);
        // Task<Pet> CreatePetAsync(CreatePetRequest request);
        // Task<bool> UpdatePetAsync(UpdatePetRequest request);
        // Task<bool> DeletePetAsync(Guid petId);
    }
}