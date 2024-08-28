from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
from typing import Optional
import torch
from diffusers import FluxPipeline
from io import BytesIO
from fastapi.responses import StreamingResponse
import logging
import uvicorn

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the FastAPI app
app = FastAPI()

# Load the model and ensure it's using the CPU or GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"Using device: {device}")
pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell", torch_dtype=torch.bfloat16)
pipe.to(device)

# Define the request model using Pydantic
class ImageRequest(BaseModel):
    prompt: constr(min_length=1, max_length=1024)
    guidance_scale: Optional[float] = 0.0
    num_inference_steps: Optional[int] = 4
    max_sequence_length: Optional[int] = 256
    seed: Optional[int] = 0

@app.post("/generate-image/")
async def generate_image(request: ImageRequest):
    try:
        logger.info(f"Received request: {request}")

        # Generate the image
        generator = torch.Generator(device).manual_seed(request.seed)
        image = pipe(
            request.prompt,
            guidance_scale=request.guidance_scale,
            num_inference_steps=request.num_inference_steps,
            max_sequence_length=request.max_sequence_length,
            generator=generator
        ).images[0]

        # Save the image to a byte buffer
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        logger.info("Image generated successfully")

        # Return the image as a streaming response
        return StreamingResponse(buffer, media_type="image/png")

    except Exception as e:
        logger.error(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the image.")

# Root endpoint for health check
@app.get("/")
async def root():
    return {"message": "Welcome to the image generation API. Use the /generate-image/ endpoint to generate images."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
