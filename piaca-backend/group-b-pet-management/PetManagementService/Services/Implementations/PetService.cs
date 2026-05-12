using System.Linq;
using PetManagementService.DTOs;
using PetManagementService.Models;
using PetManagementService.Repositories;

namespace PetManagementService.Services
{
    public class PetService : IPetService
    {
        private readonly IPetRepository _petRepository;

        public PetService(IPetRepository petRepository)
        {
            _petRepository = petRepository;
        }

        public async Task<List<PetResponse>> GetAllPetsAsync()
        {
            var pets = await _petRepository.GetAllPetsAsync();
            return pets.Select(PetResponse.FromEntity).ToList();
        }

        public async Task<PetResponse?> GetSinglePetAsync(Guid petId)
        {
            if (petId == Guid.Empty)
            {
                throw new ArgumentException("A valid pet id must be provided.");
            }

            var pet = await _petRepository.GetSinglePetAsync(petId);
            return pet == null ? null : PetResponse.FromEntity(pet);
        }

        public async Task<PetDetailsResponse?> GetPetDetailsAsync(Guid petId)
        {
            if (petId == Guid.Empty)
            {
                throw new ArgumentException("A valid pet id must be provided.");
            }

            var petDetails = await _petRepository.GetPetDetailsAsync(petId);
            return petDetails == null ? null : PetDetailsResponse.FromEntity(petDetails);
        }

        public async Task<PetFullInfoResponse?> GetPetFullInfoAsync(Guid petId)
        {
            if (petId == Guid.Empty)
            {
                throw new ArgumentException("A valid pet id must be provided.");
            }

            var petFullInfo = await _petRepository.GetPetFullInfoAsync(petId);
            return petFullInfo == null ? null : PetFullInfoResponse.FromEntity(petFullInfo);
        }
    }
}