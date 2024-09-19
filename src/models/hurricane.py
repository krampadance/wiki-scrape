from pydantic import BaseModel, ConfigDict


class HurricaneData(BaseModel):
    name: str
    start_date: str | None
    end_date: str | None
    fatalities: int | None = 0
    affected_areas: list[str] | None = []

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        populate_by_name=True,
        extra="forbid",
    )
