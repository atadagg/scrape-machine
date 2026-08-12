from pydantic import BaseModel, Field

class RuneScapeGEConfig(BaseModel):
    url: str = Field(default="https://secure.runescape.com/m=itemdb_oldschool/", description="Target GE URL")
    max_items: int = Field(default=100, description="Maximum items to scrape")
    output_format: str = Field(default="json", description="Output format")
