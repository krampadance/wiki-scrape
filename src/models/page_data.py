import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class PageMetadata(BaseModel):
    url: str | None
    last_updated: datetime

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        populate_by_name=True,
        extra="forbid",
    )

    @field_validator("last_updated", mode="before")
    def parse_last_updated(cls, value):
        # Check if the input value is a string
        if isinstance(value, str):
            # Regex to extract the date and time from the input string
            match = re.search(r"(\d{1,2} \w+ \d{4}), at (\d{2}:\d{2})", value)
            if match:
                # Extract the date and time
                date_str = match.group(1)  # '20 July 2024'
                time_str = match.group(2)  # '18:53'

                # Combine date and time into one string
                datetime_str = f"{date_str} {time_str}"

                # Convert the string to a datetime object
                return datetime.strptime(datetime_str, "%d %B %Y %H:%M")

        raise ValueError("Invalid last updated format")


class SectionData(BaseModel):
    title: str
    text: str | None = ""
    id: str
    parent_id: str | None = None
    element_type: str

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        populate_by_name=True,
        extra="forbid",
    )


# Base model containing the common attributes.
class PageData(BaseModel):
    title: str
    sections: list[SectionData]
    metadata: PageMetadata

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        populate_by_name=True,
        extra="forbid",
    )
