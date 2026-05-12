using PetManagementService.DTOs;
using PetManagementService.Models;
using PetManagementService.Repositories;
using PetManagementService.Services;

namespace PetManagementService.Tests;

public class PetServiceTests
{
    private class FakePetRepository : IPetRepository
    {
        public Task<List<Pet>> GetAllPetsAsync() => Task.FromResult(new List<Pet> { new Pet { Id = Guid.NewGuid(), Name = "Pet One" } });

        public Task<Pet?> GetSinglePetAsync(Guid petId)
        {
            if (petId == Guid.Empty)
            {
                return Task.FromResult<Pet?>(null);
            }

            return Task.FromResult<Pet?>(new Pet { Id = petId, Name = "Found Pet" });
        }

        public Task<PetDetails?> GetPetDetailsAsync(Guid petId) => Task.FromResult<PetDetails?>(null);
    }

    [Fact]
    public async Task GetAllPetsAsync_Delegates_To_Repository()
    {
        var service = new PetService(new FakePetRepository());

        var result = await service.GetAllPetsAsync();

        Assert.Single(result);
        Assert.Equal("Pet One", result[0].Name);
    }

    [Fact]
    public async Task GetSinglePetAsync_Returns_Pet_From_Repository()
    {
        var expectedId = Guid.NewGuid();
        var service = new PetService(new FakePetRepository());

        var result = await service.GetSinglePetAsync(expectedId);

        Assert.NotNull(result);
        Assert.Equal(expectedId, result?.Id);
        Assert.Equal("Found Pet", result?.Name);
    }

    [Fact]
    public async Task GetSinglePetAsync_Throws_WhenPetIdIsEmpty()
    {
        var service = new PetService(new FakePetRepository());

        var exception = await Assert.ThrowsAsync<ArgumentException>(() => service.GetSinglePetAsync(Guid.Empty));

        Assert.Equal("A valid pet id must be provided.", exception.Message);
    }
}
