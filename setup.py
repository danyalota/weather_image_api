from setuptools import find_packages, setup
setup(
    name="weather_image_api",  
    version="0.1.0",  
    packages=find_packages(), 
    install_requires=[ 
        "fastapi>=0.115.11",
        "pillow>=11.1.0",
        "pydantic>=1.8.2",
        "python-multipart>=0.0.20",
        "redis>=5.2.0",
        "uvicorn>=0.34.0"
    ],
    python_requires=">=3.9", 
)
