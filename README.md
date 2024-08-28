# Flux Image Generator API on Local System

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://hub.docker.com/)

A FastAPI-based web service that generates images using the FLUX model from Black Forest Labs. This API takes user prompts and returns generated images on your local system.

## Features

- **Prompt-based Image Generation**: Generate images based on user-defined text prompts.
- **Dockerized**: Ready-to-deploy with Docker and Docker Compose.
- **Easy Integration**: Can be integrated into existing applications or used as a standalone service.

## Quick Start

### Prerequisites

- **Python 3.11**
- **Docker and Docker Compose**

### Local Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ffiruzi/flux-local-image-generator-api.git
    cd flux-local-image-generator-api
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```bash
    uvicorn main:app --reload
    ```

4. **Access the API**:
    - Open your browser and navigate to `http://localhost:8000/docs` to explore the API documentation.

### Docker Setup

1. **Build and run the Docker container**:
    ```bash
    docker-compose up --build
    ```

2. **Access the API**:
    - The API will be available at `http://localhost:8000`.

### API Endpoints

- **GET /**: Health check endpoint.
- **POST /generate-image/**: Generates an image based on the provided prompt.

### Example Request

```json
POST /generate-image/
Content-Type: application/json

{
    "prompt": "A cat holding a sign that says hello world",
    "guidance_scale": 7.5,
    "num_inference_steps": 50,
    "max_sequence_length": 256,
    "seed": 42
}
