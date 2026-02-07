"""
📥 Dataset Downloader for Coastal Pollution Classifier
=======================================================

This script helps you build a training dataset by:
1. Creating the folder structure
2. Downloading sample images from public sources
3. Providing guidance on collecting more images

Usage:
    python download_dataset.py
"""

import os
import urllib.request
import ssl
from pathlib import Path

# Create unverified SSL context for downloads
ssl._create_default_https_context = ssl._create_unverified_context

# Paths
BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / 'dataset'

# Categories
CATEGORIES = ['plastic', 'oil_spill', 'general_waste', 'marine_debris']

# Sample image URLs (public domain / Creative Commons images)
# These are placeholder URLs - in production, collect real images
SAMPLE_IMAGES = {
    'plastic': [
        # Plastic pollution images
    ],
    'oil_spill': [
        # Oil spill images
    ],
    'general_waste': [
        # General waste images
    ],
    'marine_debris': [
        # Marine debris images
    ]
}


def create_folder_structure():
    """Create the dataset folder structure."""
    print("\n📁 Creating dataset folder structure...")
    
    for category in CATEGORIES:
        category_dir = DATASET_DIR / category
        category_dir.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created: dataset/{category}/")
    
    print("\n   Dataset structure ready!")


def count_images():
    """Count existing images in dataset."""
    counts = {}
    for category in CATEGORIES:
        category_dir = DATASET_DIR / category
        if category_dir.exists():
            images = list(category_dir.glob('*.jpg')) + \
                     list(category_dir.glob('*.jpeg')) + \
                     list(category_dir.glob('*.png'))
            counts[category] = len(images)
        else:
            counts[category] = 0
    return counts


def print_instructions():
    """Print instructions for collecting dataset."""
    print("\n" + "=" * 70)
    print("📸 HOW TO BUILD YOUR COASTAL POLLUTION DATASET")
    print("=" * 70)
    
    print("""
For accurate classification, you need ~50-100 images per category.
Here's how to collect them:

🔍 OPTION 1: Google Images (Quickest)
--------------------------------------
1. Go to images.google.com
2. Search for each category:
   - "beach plastic pollution"
   - "ocean oil spill"
   - "beach garbage waste"
   - "fishing net debris ocean"
3. Download 50+ images per category
4. Save to: backend/dataset/<category>/

🗃️ OPTION 2: Kaggle Datasets (Best Quality)
---------------------------------------------
Search for these datasets on kaggle.com:
- "Marine Debris Dataset"
- "Plastic Pollution Detection"
- "Beach Litter Classification"
- "Ocean Waste Detection"

Download and extract to: backend/dataset/

🌐 OPTION 3: Public Image Collections
---------------------------------------
- NOAA Marine Debris Database
- Ocean Conservancy Photos
- Plastic Pollution Coalition
- Surfrider Foundation

📱 OPTION 4: Take Your Own Photos
----------------------------------
Best for accuracy! Visit local beaches and collect:
- 20+ photos of plastic items
- 20+ photos of general waste
- 20+ photos of fishing debris
- (Oil spill photos may be harder to get)

""")
    
    print("=" * 70)
    print("📊 TARGET: 50-100 images per category for good accuracy")
    print("=" * 70)


def print_status():
    """Print current dataset status."""
    counts = count_images()
    total = sum(counts.values())
    
    print("\n📊 CURRENT DATASET STATUS:")
    print("-" * 40)
    
    for category in CATEGORIES:
        count = counts[category]
        if count >= 50:
            status = "✅ Ready"
        elif count >= 20:
            status = "⚠️ Need more"
        elif count > 0:
            status = "❌ Too few"
        else:
            status = "❌ Empty"
        
        bar = "█" * min(count // 5, 10) + "░" * (10 - min(count // 5, 10))
        print(f"   {category:16} [{bar}] {count:3} images {status}")
    
    print("-" * 40)
    print(f"   Total: {total} images")
    
    if total < 80:
        print("\n   ⚠️ Need at least 80 total images (20 per category)")
        print("   📥 Follow the instructions above to add more images")
    else:
        print("\n   ✅ Dataset ready for training!")
        print("   🚀 Run: python train_model.py")


def create_synthetic_samples():
    """Create synthetic sample images for testing."""
    from PIL import Image, ImageDraw
    import random
    
    print("\n🎨 Creating synthetic sample images for testing...")
    
    # Color palettes for each category
    palettes = {
        'plastic': {
            'base': [(230, 50, 50), (50, 100, 230), (240, 240, 240), (50, 180, 50)],
            'accent': [(255, 100, 100), (100, 150, 255), (200, 200, 200)],
            'shapes': 'mixed'
        },
        'oil_spill': {
            'base': [(20, 20, 25), (40, 35, 30), (60, 50, 45)],
            'accent': [(30, 30, 35), (50, 45, 40)],
            'shapes': 'blobs'
        },
        'general_waste': {
            'base': [(139, 90, 43), (160, 120, 60), (180, 140, 80)],
            'accent': [(100, 80, 40), (120, 100, 50), (200, 180, 140)],
            'shapes': 'mixed'
        },
        'marine_debris': {
            'base': [(0, 100, 120), (30, 80, 100), (50, 120, 100)],
            'accent': [(100, 150, 150), (80, 130, 120), (60, 100, 90)],
            'shapes': 'lines'
        }
    }
    
    for category in CATEGORIES:
        category_dir = DATASET_DIR / category
        existing = len(list(category_dir.glob('*.jpg')))
        
        if existing < 20:
            num_to_create = 25 - existing
            print(f"   Creating {num_to_create} samples for {category}...")
            
            palette = palettes[category]
            
            for i in range(num_to_create):
                # Create base image with gradient
                img = Image.new('RGB', (224, 224))
                pixels = img.load()
                
                base = random.choice(palette['base'])
                
                # Create gradient or noisy background
                for x in range(224):
                    for y in range(224):
                        noise_r = random.randint(-30, 30)
                        noise_g = random.randint(-30, 30)
                        noise_b = random.randint(-30, 30)
                        
                        r = max(0, min(255, base[0] + noise_r + (x + y) // 10))
                        g = max(0, min(255, base[1] + noise_g + (x - y) // 10))
                        b = max(0, min(255, base[2] + noise_b))
                        
                        pixels[x, y] = (r, g, b)
                
                # Add shapes based on category
                draw = ImageDraw.Draw(img)
                
                num_shapes = random.randint(5, 15)
                for _ in range(num_shapes):
                    accent = random.choice(palette['accent'])
                    x1 = random.randint(0, 200)
                    y1 = random.randint(0, 200)
                    
                    if palette['shapes'] == 'lines':
                        # Draw lines (for fishing nets)
                        x2 = x1 + random.randint(20, 100)
                        y2 = y1 + random.randint(-50, 50)
                        draw.line([(x1, y1), (x2, y2)], fill=accent, width=2)
                    elif palette['shapes'] == 'blobs':
                        # Draw blobs (for oil)
                        x2 = x1 + random.randint(30, 80)
                        y2 = y1 + random.randint(30, 80)
                        draw.ellipse([x1, y1, x2, y2], fill=accent)
                    else:
                        # Mixed shapes
                        x2 = x1 + random.randint(10, 50)
                        y2 = y1 + random.randint(10, 50)
                        if random.random() > 0.5:
                            draw.rectangle([x1, y1, x2, y2], fill=accent)
                        else:
                            draw.ellipse([x1, y1, x2, y2], fill=accent)
                
                # Save
                img.save(category_dir / f'synthetic_{existing + i + 1:03d}.jpg', 'JPEG')
            
            print(f"      ✅ Created {num_to_create} images")
    
    print("\n   ⚠️ These are SYNTHETIC images for testing only!")
    print("   📸 Replace with REAL photos for accurate classification!")


def main():
    print("=" * 70)
    print("🌊 Coastal Pollution Dataset Builder")
    print("=" * 70)
    
    # Create folder structure
    create_folder_structure()
    
    # Show current status
    print_status()
    
    # Check if we need synthetic data
    counts = count_images()
    total = sum(counts.values())
    
    if total < 80:
        print("\n" + "-" * 70)
        response = input("Create synthetic sample images for testing? (y/n): ").lower()
        if response == 'y':
            try:
                create_synthetic_samples()
                print_status()
            except ImportError:
                print("   ❌ PIL not installed. Run: pip install pillow")
    
    # Print collection instructions
    print_instructions()
    
    # Final message
    counts = count_images()
    total = sum(counts.values())
    
    if total >= 80:
        print("\n🚀 Ready to train! Run:")
        print("   python train_model.py")


if __name__ == "__main__":
    main()
