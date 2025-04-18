import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from timm import create_model
import os
from tqdm import tqdm

# --------------------------
# 1. Configuration
# --------------------------
BATCH_SIZE = 32
EPOCHS = 20
LR = 0.0001
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DATA_DIR = "D:/Github/Programming-Sign-Language-PSL-/asl_dataset"
MODEL_PATH = "D:/Github/Programming-Sign-Language-PSL-/best_model.pth"

# --------------------------
# 2. Transforms
# --------------------------
transform = transforms.Compose([
    transforms.Resize((400, 400)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# --------------------------
# 3. Dataset & Dataloaders
# --------------------------
train_dataset = datasets.ImageFolder(os.path.join(DATA_DIR, "train"), transform=transform)
val_dataset = datasets.ImageFolder(os.path.join(DATA_DIR, "val"), transform=transform)
test_dataset = datasets.ImageFolder(os.path.join(DATA_DIR, "test"), transform=transform)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE)

# --------------------------
# 4. Model Setup
# --------------------------
model = create_model("efficientnet_b3", pretrained=True, num_classes=len(train_dataset.classes))
model.to(DEVICE)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LR)

# --------------------------
# 5. Training + Validation Loop
# --------------------------
best_acc = 0

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0

    for images, labels in tqdm(train_loader, desc=f"Training Epoch {epoch+1}/{EPOCHS}"):
        images, labels = images.to(DEVICE), labels.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    # Validation
    model.eval()
    correct = total = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

    val_acc = correct / total
    print(f"Validation Accuracy: {val_acc:.4f}")

    # Save best model
    if val_acc > best_acc:
        best_acc = val_acc
        torch.save(model.state_dict(), MODEL_PATH)
        print(f"Best model saved with accuracy: {best_acc:.4f}")

print("Training Complete!")

# --------------------------
# 6. Testing Phase
# --------------------------
print("\nStarting Testing Phase...")
model.load_state_dict(torch.load(MODEL_PATH))
model.eval()

correct = total = 0

with torch.no_grad():
    for images, labels in tqdm(test_loader, desc="Testing"):
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        outputs = model(images)
        _, preds = torch.max(outputs, 1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

test_acc = correct / total
print(f"Test Accuracy: {test_acc:.4f}")
