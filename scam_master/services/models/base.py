from pydantic import BaseModel as PydanticBaseModel, Field
from humps import camelize



class BaseModel(PydanticBaseModel):
    class Config:
        alias_generator = camelize
        populate_by_name = True
        from_attributes = True
        use_enum_values = True
