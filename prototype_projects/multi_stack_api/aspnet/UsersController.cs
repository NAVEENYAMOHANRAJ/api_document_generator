using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/aspnet-users")]
public class UsersController : ControllerBase
{
    [HttpGet]
    public IActionResult ListUsers() => Ok();

    [HttpGet("{id}")]
    public IActionResult GetUser(string id) => Ok();

    [HttpPost]
    public IActionResult CreateUser() => Created();
}
