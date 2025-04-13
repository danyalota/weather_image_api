from pydantic import BaseModel


class ImageInfo(BaseModel):
    width: int
    height: int
    format: str


class WeatherMetaData(BaseModel):
    station_id: str
    captured_at: str
    location: str
    temperature: float
    humidity: float


class ProcessedMetaData(BaseModel):
    station_id: str
    captured_at: str
    location: str
    temperature: float
    humidity: float
    image: ImageInfo
    processed_at: str
