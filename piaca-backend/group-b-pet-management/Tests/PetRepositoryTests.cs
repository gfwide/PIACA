using Microsoft.EntityFrameworkCore;
using PetManagementService.Data;
using PetManagementService.Models;
using PetManagementService.Repositories;

namespace PetManagementService.Tests;

public class PetRepositoryTests
{
    private static AppDbContext CreateInMemoryContext(string databaseName)
    {
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseInMemoryDatabase(databaseName)
            .Options;

        return new AppDbContext(options);
    }

    [Fact]
    public async Task GetAllPetsAsync_Returns_All_Pets()
    {
        using var context = CreateInMemoryContext(nameof(GetAllPetsAsync_Returns_All_Pets));
        context.Pets.AddRange(
            new Pet { Id = Guid.NewGuid(), Name = "Alpha" },
            new Pet { Id = Guid.NewGuid(), Name = "Beta" }
        );
        await context.SaveChangesAsync();

        var repository = new PetRepository(context);

        var result = await repository.GetAllPetsAsync();

        Assert.Equal(2, result.Count);
        Assert.Contains(result, p => p.Name == "Alpha");
        Assert.Contains(result, p => p.Name == "Beta");
    }

    [Fact]
    public async Task GetSinglePetAsync_Returns_Pet_WhenFound()
    {
        using var context = CreateInMemoryContext(nameof(GetSinglePetAsync_Returns_Pet_WhenFound));
        var expected = new Pet { Id = Guid.NewGuid(), Name = "Found" };
        context.Pets.Add(expected);
        await context.SaveChangesAsync();

        var repository = new PetRepository(context);

        var result = await repository.GetSinglePetAsync(expected.Id);

        Assert.NotNull(result);
        Assert.Equal(expected.Id, result?.Id);
        Assert.Equal("Found", result?.Name);
    }

    [Fact]
    public async Task GetSinglePetAsync_Returns_Null_WhenNotFound()
    {
        using var context = CreateInMemoryContext(nameof(GetSinglePetAsync_Returns_Null_WhenNotFound));
        context.Pets.Add(new Pet { Id = Guid.NewGuid(), Name = "Another" });
        await context.SaveChangesAsync();

        var repository = new PetRepository(context);

        var result = await repository.GetSinglePetAsync(Guid.NewGuid());

        Assert.Null(result);
    }

    [Fact]
    public async Task GetPetDetailsAsync_Returns_PetDetails_WhenFound()
    {
        using var context = CreateInMemoryContext(nameof(GetPetDetailsAsync_Returns_PetDetails_WhenFound));
        var pet = new Pet { Id = Guid.NewGuid(), Name = "DetailPet" };
        var details = new PetDetails { Id = Guid.NewGuid(), PetId = pet.Id, Breed = "Breed" };

        context.Pets.Add(pet);
        context.PetDetails.Add(details);
        await context.SaveChangesAsync();

        var repository = new PetRepository(context);

        var result = await repository.GetPetDetailsAsync(pet.Id);

        Assert.NotNull(result);
        Assert.Equal(pet.Id, result?.PetId);
        Assert.Equal("Breed", result?.Breed);
    }

    [Fact]
    public async Task GetPetDetailsAsync_Returns_Null_WhenNotFound()
    {
        using var context = CreateInMemoryContext(nameof(GetPetDetailsAsync_Returns_Null_WhenNotFound));
        context.PetDetails.Add(new PetDetails { Id = Guid.NewGuid(), PetId = Guid.NewGuid(), Breed = "Breed" });
        await context.SaveChangesAsync();

        var repository = new PetRepository(context);

        var result = await repository.GetPetDetailsAsync(Guid.NewGuid());

        Assert.Null(result);
    }
}
