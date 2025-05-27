# utils/classify.py
import torch
from torchvision import transforms
from PIL import Image
from model.classifier_model import AadharClassifier

# Load model
model = AadharClassifier()
model.load_state_dict(torch.load("models/aadhar_classifier.pt", map_location=torch.device('cpu')))
model.eval()

def is_aadhar_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)
        prob = output.item()

    return prob > 0.5
