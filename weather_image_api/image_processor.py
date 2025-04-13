from io import BytesIO

from fastapi import HTTPException, UploadFile
from PIL import Image

from weather_image_api.dtos import ImageInfo, WeatherMetaData


class ImageProcessor:

    def validate_metadata(self, metadata: dict) -> WeatherMetaData:
        """Validate metadata to ensure required fields are present and valid."""
        try:
            metadata_obj = WeatherMetaData(**metadata)
            return metadata_obj
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid metadata: {str(e)}")

    def extract_image_info(self, file: UploadFile) -> ImageInfo:
        """Extract image data (width, height, format) from the uploaded image."""
        try:
            img = Image.open(BytesIO(file.file.read()))
            img_info = ImageInfo(
                width=img.width,
                height=img.height,
                format=img.format,
            )
            return img_info
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error processing image: {str(e)}"
            )
