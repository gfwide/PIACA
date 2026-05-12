using Microsoft.AspNetCore.Mvc;
using PetManagementService.DTOs;
using PetManagementService.Services;

namespace PetManagementService.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class PetController : ControllerBase
    {
        private readonly IPetService _petService;

        public PetController(IPetService petService)
        {
            _petService = petService;
        }

        [HttpGet("getAllPets")]
        public async Task<ActionResult<List<PetResponse>>> GetAllPets()
        {
            try
            {
                var pets = await _petService.GetAllPetsAsync();
                return Ok(pets);
            }
            catch
            {
                throw new Exception("An error occurred while fetching pets.");
            }

        }

        [HttpGet("getPet")]
        public async Task<ActionResult<PetResponse>> GetSinglePets(Guid petId)
        {
            try
            {
                var pet = await _petService.GetSinglePetAsync(petId);

                if (pet == null)
                {
                    return NotFound("Pet not found.");
                }

                return Ok(pet);
            }
            catch (ArgumentException ex)
            {
                return BadRequest(ex.Message);
            }
            catch
            {
                return StatusCode(500, "An unexpected error occurred.");
            }
        }

        [HttpGet("getPetDetails")]
        public async Task<ActionResult<PetDetailsResponse>> GetPetDetails(Guid petId)
        {
            try
            {
                var petDetails = await _petService.GetPetDetailsAsync(petId);

                if (petDetails == null)
                {
                    return NotFound("Pet details not found.");
                }

                return Ok(petDetails);
            }
            catch (ArgumentException ex)
            {
                return BadRequest(ex.Message);
            }
            catch
            {
                return StatusCode(500, "An unexpected error occurred.");
            }
        }

            [HttpGet("getPetFullInfo")]
        public async Task<ActionResult<PetFullInfoResponse>> GetPetFullInfo(Guid petId)
        {
            try
            {
                var petFullInfo = await _petService.GetPetFullInfoAsync(petId);

                if (petFullInfo == null)
                {
                    return NotFound("Pet full info not found.");
                }

                return Ok(petFullInfo);
            }
            catch (ArgumentException ex)
            {
                return BadRequest(ex.Message);
            }
            catch
            {
                return StatusCode(500, "An unexpected error occurred.");
            }
        }
    }
}