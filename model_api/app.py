from fastapi import FastAPI, File, UploadFile
from io import BytesIO
from PIL import Image
import torch
from torchvision import transforms
from model import SimpleModel

app = FastAPI()

# Load the trained model
model = SimpleModel()
model.load_state_dict(torch.load('model.pth'))
model.eval()

# Preprocessing function
def preprocess_image(img):
    pil_img = Image.open(BytesIO(img)).convert("L").resize((28, 28))
    img_tensor = transforms.ToTensor()(pil_img).unsqueeze(0)
    return img_tensor

# Prediction endpoint
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    img_bytes = await file.read()
    img_tensor = preprocess_image(img_bytes)
    
    with torch.no_grad():
        output = model(img_tensor)
        probabilities = torch.nn.functional.softmax(output, dim=1)
        confidence = torch.max(probabilities).item()
        predicted_label = torch.argmax(output, 1).item()

    return {"prediction": predicted_label, "confidence": confidence}
