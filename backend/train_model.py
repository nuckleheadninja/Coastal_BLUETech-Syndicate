"""
🧠 Coastal Pollution Classifier - EfficientNet Training
=======================================================

Model: EfficientNet-B0 (State-of-the-art accuracy/efficiency)
Features:
- Balanced training
- Strong augmentation
- Weighted loss for optimal accuracy
"""

import os
import json
import random
from pathlib import Path
from PIL import Image

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
import numpy as np

print(f"✅ PyTorch {torch.__version__}")
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"   Device: {DEVICE}")

# Config
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 15
LEARNING_RATE = 0.0005

CATEGORIES = ['plastic', 'oil_spill', 'other_solid_waste', 'marine_debris']
NUM_CLASSES = len(CATEGORIES)

# Paths
BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / 'newdataset'
MODEL_DIR = BASE_DIR / 'models'
MODEL_PATH = MODEL_DIR / 'pollution_classifier.pth'
CLASS_INDICES_PATH = MODEL_DIR / 'class_indices.json'

MAX_PER_CLASS = 300


class BalancedDataset(Dataset):
    def __init__(self, root_dir, transform=None, is_train=True):
        self.root_dir = Path(root_dir)
        self.transform = transform
        self.samples = []
        self.idx_to_class = {i: c for i, c in enumerate(CATEGORIES)}
        self.class_to_idx = {c: i for i, c in enumerate(CATEGORIES)}
        
        print(f"\n📊 Loading dataset ({'train' if is_train else 'val'}):")
        
        for category in CATEGORIES:
            cat_dir = self.root_dir / category
            if cat_dir.exists():
                images = []
                for ext in ['*.jpg', '*.jpeg', '*.png']:
                    images.extend(list(cat_dir.glob(ext)))
                
                random.shuffle(images)
                selected = images[:MAX_PER_CLASS]
                
                for img in selected:
                    self.samples.append((img, self.class_to_idx[category]))
                
                print(f"   {category}: {len(selected)} images")
        
        random.shuffle(self.samples)
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        path, label = self.samples[idx]
        try:
            img = Image.open(path).convert('RGB')
            if self.transform:
                img = self.transform(img)
            return img, label
        except:
            return torch.zeros((3, IMG_SIZE, IMG_SIZE)), label


def create_model():
    print("\n🔨 Creating EfficientNet-B0 model...")
    # Use EfficientNet V2 (newer/better) or B0
    try:
        model = models.efficientnet_b0(weights='IMAGENET1K_V1')
    except:
        # Fallback if V1 weights name differs in older torchvision
        model = models.efficientnet_b0(pretrained=True)
    
    # Unfreeze last blocks for fine-tuning
    for param in model.parameters():
        param.requires_grad = True  # Fine-tune all layers for best accuracy
    
    # Custom head
    num_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.4, inplace=True),
        nn.Linear(num_features, NUM_CLASSES),
    )
    
    return model.to(DEVICE)


def get_transforms():
    train_transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.RandomCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(p=0.2),
        transforms.RandomRotation(20),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    return train_transform, val_transform


def train():
    print("=" * 60)
    print("🌊 EfficientNet Pollution Training")
    print("=" * 60)
    
    train_tf, val_tf = get_transforms()
    full_ds = BalancedDataset(DATASET_DIR, train_tf)
    
    # Split
    train_len = int(0.8 * len(full_ds))
    val_len = len(full_ds) - train_len
    train_ds, val_ds = torch.utils.data.random_split(full_ds, [train_len, val_len])
    
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE)
    
    model = create_model()
    
    # Optimizer
    optimizer = optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=0.01)
    criterion = nn.CrossEntropyLoss()
    scheduler = optim.lr_scheduler.OneCycleLR(
        optimizer, max_lr=LEARNING_RATE, steps_per_epoch=len(train_loader), epochs=EPOCHS
    )
    
    print(f"\n🚀 Training {EPOCHS} epochs...")
    best_acc = 0.0
    
    for epoch in range(EPOCHS):
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        for images, labels in train_loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            scheduler.step()
            
            train_loss += loss.item()
            _, pred = outputs.max(1)
            train_total += labels.size(0)
            train_correct += pred.eq(labels).sum().item()
            
        # Validation
        model.eval()
        val_correct = 0
        val_total = 0
        class_hits = [0] * NUM_CLASSES
        class_counts = [0] * NUM_CLASSES
        
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(DEVICE), labels.to(DEVICE)
                outputs = model(images)
                _, pred = outputs.max(1)
                
                val_total += labels.size(0)
                val_correct += pred.eq(labels).sum().item()
                
                for i in range(len(labels)):
                    lbl = labels[i].item()
                    class_counts[lbl] += 1
                    if pred[i] == lbl:
                        class_hits[lbl] += 1
        
        train_acc = 100. * train_correct / train_total
        val_acc = 100. * val_correct / val_total
        
        # Per class stats
        stats = []
        for i, cat in enumerate(CATEGORIES):
            if class_counts[i] > 0:
                acc = 100. * class_hits[i] / class_counts[i]
                stats.append(f"{cat[:3]}:{acc:.0f}%")
        
        print(f"Epoch {epoch+1:2d}: Train {train_acc:5.1f}% | Val {val_acc:5.1f}% | {' '.join(stats)}")
        
        if val_acc > best_acc:
            best_acc = val_acc
            MODEL_DIR.mkdir(parents=True, exist_ok=True)
            torch.save(model.state_dict(), MODEL_PATH)
            print(f"   💾 Best model saved! ({best_acc:.1f}%)")
            
    # Save indices
    with open(CLASS_INDICES_PATH, 'w') as f:
        json.dump({str(i): c for i, c in enumerate(CATEGORIES)}, f)
    
    print(f"\n✅ Done! Best Accuracy: {best_acc:.1f}%")


if __name__ == "__main__":
    train()
