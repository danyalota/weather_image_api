import json
from typing import Any
from datetime import datetime, timezone

import redis
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse

from weather_image_api.dtos import ProcessedMetaData
from weather_image_api.image_processor import ImageProcessor

app = FastAPI()
image_uploader = ImageProcessor()
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


@app.get("/")
async def root():
    return FileResponse("weather_image_api/frontend/index.html")


@app.post("/upload_image")
async def upload_image(
    file: UploadFile = File(...), metadata: str = Form(...)
) -> JSONResponse:
    """Handle image upload along with metadata."""
    try:
        metadata_dict = json.loads(metadata)
        validated_metadata = image_uploader.validate_metadata(metadata_dict)
        image_data = image_uploader.extract_image_info(file)

        processed_meta_data = ProcessedMetaData(
            station_id=validated_metadata.station_id,
            captured_at=str(validated_metadata.captured_at),
            location=validated_metadata.location,
            temperature=validated_metadata.temperature,
            humidity=validated_metadata.humidity,
            image=image_data,
            processed_at=str(
                datetime.now(timezone.utc)
                .replace(microsecond=0)
                .isoformat()
                .replace("+00:00", "Z")
            ),
        )
        redis_key = f"weather_entry:{processed_meta_data.station_id}:{processed_meta_data.processed_at}"

        redis_client.set(redis_key, processed_meta_data.model_dump_json())

        return JSONResponse(processed_meta_data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/get_entries")
async def get_all_weather_entries() -> list[Any]:
    """Fetch all processed entries from Redis."""
    try:
        pattern = "weather_entry:*"
        all_keys = redis_client.scan_iter(pattern)

        all_entries = []

        for key in all_keys:
            entry_json = redis_client.get(key)
            if entry_json:
                all_entries.append(json.loads(entry_json))

        return all_entries
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching data from Redis: {str(e)}"
        )
