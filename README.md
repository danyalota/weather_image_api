# Weather Image API


## Description

The **Weather Image API** is a FastAPI-based application that allows users to upload weather-related images along with metadata. The metadata includes information such as station ID, capture time, location, temperature, and humidity. The application processes the images, validates metadata, and stores the data in Redis, which is used to store the uploaded data in memory. Users can retrieve the stored weather entries via an API.

This API provides the following functionalities:
- Upload weather images along with metadata.
- Store processed entries in Redis.
- Fetch all stored weather entries from Redis.


## Installation

### Install Redis

To run this application, you will need Redis to store the uploaded data in memory. Follow the instructions below to install Redis depending on your operating system.

#### For Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl start redis-server
```

#### For Mac:
```bash
brew install redis
brew services start redis
```

### Installing the Module:

Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/danyalota/weather_image_api.git
cd weather_image_api
```

Install the required dependencies:

```bash
pip install .
```


## Start the Server:
```bash
python -m uvicorn weather_image_api.main:app --reload
```

## Usage

A basic frontend is provided at the base path of where the server is started. In this case, it can be accessed at `http://127.0.0.1:8000`. Here, users can upload image data via a simple form. Alternatively, you can use `curl` to upload data programmatically via the `/upload_image` endpoint.

### Example: Uploading Image and Metadata via `curl`

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/upload_image' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@image.jpg' \
  -F 'metadata={"station_id": "ABC123", "captured_at": "2025-04-13T16:38:34Z", "location": "New York", "temperature": 23.5, "humidity": 60.2}'
```


### Metadata Format:
```bash
{
  "station_id": "ABC123",
  "captured_at": "2025-04-13T16:38:34Z",
  "location": "New York",
  "temperature": 23.5,
  "humidity": 60.2
}
```

### Fetch All Existing Entires
To fetch all existing entries, make a GET request to the `/get_entires` endpoint:
```bash
curl -X 'GET' 'http://127.0.0.1:8000/get_entires'

```


## My Decisions
### Assumptions
- Metadata can be submitted as a single JSON string. 
- The in-memory storage (using Redis) is configured to persist data even after the application is shut down. 
- Timestamps are required to be in UTC, with no timezone offset

### What did I simplify or omitted on purpose?
- I did not use specific exception definitions. 
- I haven’t added a dedicated logger yet, but it should be integrated and passed through the Uvicorn config, as Uvicorn can ignore logs in certain cases. 
- I tested the core functionality manually for now, without adding unit tests.
- Keept code quality libraries local 

## Reflection on AI Use

### Which AI tools did I use – and how?
I mainly use ChatGPT to create the base structure of the code, which I can then refine and improve myself.

### Where did I deliberately avoid using AI – and why?
I avoid giving access to the whole codebase (e.g., with CursorAI). It can make the base implementation easier, but it also carries the risk of exposing sensitive data.

I'm generally cautious when it comes to generating unit tests with AI, since there might be very specific edge cases that need to be handled—ones that aren’t foreseeable just by providing a single function from a more complex algorithm.

### How did I ensure that AI-generated code is robust, secure, and understandable?

Without assuming the AI is all-knowing, I make sure to ask about every part of the code I'm not familiar with and look for slimmer, more performant solutions.

Sometimes, a simple "Improve the code to..." can be useful, depending on what I'm aiming for.

To get the exact solution I need, providing a detailed prompt always helps.

## Example Prompt for Base Structure
Create a robust and performant Python application with FastApi with API endpoints that process weather station data. The application should support image uploads and json metadata together using multipart form-data

The upload should contain a Image and some metadata 
The metadata should look like this:
{
  "station_id": "WXT-320",
  "captured_at": "2024-12-01T12:00:00Z",
  "location": "Munich",
  "temperature": 22.4,
  "humidity": 55.1
}


The API should:

Validate the meta data with pydantic models
Extract image info: width, height, and format
Combine the metadata and image info into one structured dataset
Store entries in an inmemory store
Provide a GET endpoint to retrieve all processed entries


The processed data should look like this:

{
  "station_id": "WXT-320",
  "captured_at": "2024-12-01T12:00:00Z",
  "location": "Munich",
  "temperature": 22.4,
  "humidity": 55.1,
  "image": {
    "width": 1024,
    "height": 768,
    "format": "JPEG"
  },
  "processed_at": "2025-04-01T15:00:00Z"
}


Use FastAPI and include a solid structure, typing and good performance


## Tech Stack Justification
### FastApi:
Lightweight and ideal for building high-performance APIs. It makes data validation super straightforward with Pydantic and supports asynchronous operations out of the box.

### Redis:
A simple and extremely fast in-memory database, perfect for quickly saving and retrieving data. It also supports persistence across restarts and is very easy to integrate.

### Pillow:
A lightweight and simple way to extract metadata from images. OpenCV could have been an alternative, but it felt like overkill for this use case.