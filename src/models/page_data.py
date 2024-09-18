from pydantic import BaseModel, ConfigDict


# Base model containing the common attributes.
class PageData(BaseModel):
    title: str

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        populate_by_name=True,
        extra="forbid",
    )
