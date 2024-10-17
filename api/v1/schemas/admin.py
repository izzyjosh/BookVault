from pydantic import BaseModel, ConfigDict


class AdminUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role: str
