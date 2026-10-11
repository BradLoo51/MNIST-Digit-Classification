from training.ClassifierModel import ImageClassifier
import torch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import uvicorn
from PIL import Image
from io import BytesIO
from torchvision import transforms
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "training" / "mnist_model.pt"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImagePayload(BaseModel):
    image: str

model = ImageClassifier()
with open(MODEL_PATH, "rb") as model_file:
    model.load_state_dict(torch.load(model_file))
model.eval()

@app.post("/predict")
async def predict(payload: ImagePayload):
    # Strip out the metadata header
    img_data = payload.image.split(",")[1] # Payload received: 'data:image/png;base64,iVBOR...

    # Decode the base64 string back to bytes
    img_bytes = base64.b64decode(img_data)
    
    # Load bytes into a PIL Image
    image = Image.open(BytesIO(img_bytes)).convert('L') # Convert to grayscale

    # Resize to 28x28 and convert to tensor
    img = transforms.ToTensor()(image.resize((28, 28)))

    with torch.no_grad():
        output = model(img.unsqueeze(0))  # Add batch dimension
        pred = output.argmax().item()

    return {
        "prediction": pred
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)