using Microsoft.EntityFrameworkCore;
using PetManagementService.Data;
using PetManagementService.Models;
using PetManagementService.DTOs;

namespace PetManagementService.Repositories
{
    public class PetRepository : IPetRepository
    {
        private readonly AppDbContext _context;

        public PetRepository(AppDbContext context)
        {
            _context = context;
        }

        public async Task<List<Pet>> GetAllPetsAsync()
        {
            return await _context.Pets
                .AsNoTracking()
                .ToListAsync();
        }

        public async Task<Pet?> GetSinglePetAsync(Guid petId)
        {
            return await _context.Pets
                .AsNoTracking()
                .FirstOrDefaultAsync(p => p.Id == petId);
        }

        public async Task<PetDetails?> GetPetDetailsAsync(Guid petId)
        {
            return await _context.PetDetails
                .AsNoTracking()
                .FirstOrDefaultAsync(d => d.PetId == petId);
        }

        public async Task<Pet?> GetPetFullInfoAsync(Guid petId)
        {
            return await _context.Pets
                            .Include(p => p.Details)
                            .Include(p => p.Temperament)
                            .Include(p => p.Sociability)
                            .Include(p => p.VeterinaryCare)
                            .Include(p => p.Diseases)
                            .Where(p => p.Id == petId)
                            .FirstOrDefaultAsync();
        }

        // public async Task<List<Pet>> GetPetsByFilterAsync(FilterPetsRequest filter) 
        // {

        // }

        // public async Task<Pet> CreatePetAsync(CreatePetRequest request) 
        // {

        // }
        // public async Task<bool> UpdatePetAsync(UpdatePetRequest request) 
        // {

        // }
        // public async Task<bool> DeletePetAsync(Guid petId) 
        // {

        // }

        // public async Task<Pet> CreatePet()
        // {
            
        // }
    }
}