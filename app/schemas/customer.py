from pydantic import BaseModel, EmailStr, ConfigDict


class CustomerResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True,
    )