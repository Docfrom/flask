from pydantic import  BaseModel, field_validator

class UserBase(BaseModel):
    name: str | None
    password: str | None

    @field_validator("password")
    @classmethod
    def check_pwd(cls, value):
        if len(value) < 8:
            raise ValueError("PWD is to short")
        return value

class UpdateUser(UserBase):
    name: str | None
    password: str | None



class CreateUser(UserBase):
    name: str
    password: str