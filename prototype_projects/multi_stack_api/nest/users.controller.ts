import {
  BadRequestException,
  Body,
  Controller,
  Get,
  Headers,
  HttpCode,
  NotFoundException,
  Param,
  Patch,
  Post,
  Query,
} from "@nestjs/common";

class CreateUserDto {
  name: string;
  email: string;
}

class UpdateUserDto {
  name?: string;
  active?: boolean;
}

@Controller("nest-users")
export class UsersController {
  @Get()
  listUsers(
    @Query("role") role?: string,
    @Headers("x-request-id") requestId?: string,
  ) {
    return [];
  }

  @Get(":id")
  getUser(@Param("id") id: string) {
    if (!id) {
      throw new BadRequestException("id is required");
    }
    throw new NotFoundException("User not found");
  }

  @Post()
  createUser(@Body() body: CreateUserDto) {
    if (!body.name) {
      throw new BadRequestException("name is required");
    }
    return body;
  }

  @Patch(":id")
  @HttpCode(200)
  updateUser(@Param("id") id: string, @Body() body: UpdateUserDto) {
    return { id };
  }
}
