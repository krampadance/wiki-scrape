from pydantic import BaseModel, ConfigDict, Field


class HurricaneData(BaseModel):
    name: str = Field(alias="hurricane_storm_name")
    start_date: str | None = Field(alias="date_start", default=None)
    end_date: str | None = Field(alias="date_end", default=None)
    fatalities: int | None = Field(alias="number_of_deaths", default=0)
    affected_areas: list[str] | None = Field(alias="list_of_areas_affected", default=[])

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        populate_by_name=True,
        extra="forbid",
    )
