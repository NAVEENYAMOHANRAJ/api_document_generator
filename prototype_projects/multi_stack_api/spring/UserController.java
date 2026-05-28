import org.springframework.web.bind.annotation.*;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

class CreateSpringUserRequest {
    private String name;
    private String email;
    private Integer age;
}

class UpdateSpringUserRequest {
    private String name;
    private Boolean active;
}

@RestController
@RequestMapping("/api/spring-users")
public class UserController {
    @GetMapping
    public String listUsers(
        @RequestParam(value = "role", required = false) String role,
        @RequestHeader(value = "x-request-id", required = false) String requestId
    ) { return ""; }

    @GetMapping("/{id}")
    public String getUser(@PathVariable("id") String id) {
        if (id == null) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "id is required");
        }
        throw new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found");
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public String createUser(@RequestBody CreateSpringUserRequest body) { return ""; }

    @PatchMapping("/{id}")
    public String updateUser(
        @PathVariable("id") String id,
        @RequestBody UpdateSpringUserRequest body
    ) { return ""; }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteUser(@PathVariable("id") String id) {}
}
