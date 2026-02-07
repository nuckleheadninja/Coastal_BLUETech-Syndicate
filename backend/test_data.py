"""
Test Data Generator for Coastal Pollution Monitor
Creates sample pollution reports for demonstration purposes
"""

import os
import random
from datetime import datetime, timedelta
from database import init_database, insert_report
from PIL import Image
import numpy as np

# Sample locations around Indian coast
SAMPLE_LOCATIONS = [
    {"name": "Marina Beach, Chennai", "lat": 13.0500, "lng": 80.2824},
    {"name": "Juhu Beach, Mumbai", "lat": 19.0883, "lng": 72.8262},
    {"name": "Kovalam Beach, Kerala", "lat": 8.4004, "lng": 76.9787},
    {"name": "Puri Beach, Odisha", "lat": 19.7983, "lng": 85.8250},
    {"name": "Goa Beach", "lat": 15.2993, "lng": 74.1240},
    {"name": "Digha Beach, West Bengal", "lat": 21.6275, "lng": 87.5097},
    {"name": "Vizag Beach, Andhra", "lat": 17.7231, "lng": 83.3013},
    {"name": "Mandvi Beach, Gujarat", "lat": 22.8333, "lng": 69.3500},
    {"name": "Karwar Beach, Karnataka", "lat": 14.8139, "lng": 74.1296},
    {"name": "Varkala Beach, Kerala", "lat": 8.7378, "lng": 76.7047},
]

# Sample descriptions for each pollution type
DESCRIPTIONS = {
    "plastic": [
        "Found multiple plastic bottles and bags near the shore",
        "Large accumulation of plastic waste after high tide",
        "Plastic wrappers and containers scattered on beach",
        "Microplastics visible in sand near waterline",
    ],
    "oil_spill": [
        "Oil sheen visible on water surface",
        "Tar balls found along the beach",
        "Suspected fuel leak from nearby boats",
        "Dark oily residue on rocks and sand",
    ],
    "other_solid_waste": [
        "Mixed garbage including food waste and paper",
        "Trash left behind by beach visitors",
        "Debris washed up from recent storm",
        "Assorted litter near fishing area",
    ],
    "marine_debris": [
        "Abandoned fishing net tangled in rocks",
        "Old ropes and buoys washed ashore",
        "Broken fishing equipment on beach",
        "Nylon nets entangling marine plants",
    ],
}


def create_sample_image(pollution_type: str, filename: str):
    """
    Create a simple sample image representing each pollution type.
    Uses color patterns to simulate different types of pollution.
    """
    # Create image based on pollution type
    size = (400, 300)
    
    if pollution_type == "plastic":
        # Bright, colorful for plastic
        base_color = (200, 220, 230)  # Light blue-gray
        accent_colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
    elif pollution_type == "oil_spill":
        # Dark, oily appearance
        base_color = (40, 50, 60)
        accent_colors = [(20, 25, 30), (60, 50, 40)]
    elif pollution_type == "other_solid_waste":
        # Brown, earthy tones
        base_color = (180, 160, 130)
        accent_colors = [(139, 90, 43), (210, 180, 140)]
    else:  # marine_debris
        # Blue-green ocean colors
        base_color = (100, 150, 180)
        accent_colors = [(70, 120, 100), (150, 180, 200)]
    
    # Create base image
    img_array = np.full((size[1], size[0], 3), base_color, dtype=np.uint8)
    
    # Add some random patterns
    for _ in range(50):
        x = random.randint(0, size[0] - 30)
        y = random.randint(0, size[1] - 30)
        w = random.randint(10, 40)
        h = random.randint(10, 40)
        color = random.choice(accent_colors)
        img_array[y:y+h, x:x+w] = color
    
    # Add noise for realism
    noise = np.random.randint(-20, 20, (size[1], size[0], 3))
    img_array = np.clip(img_array.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Save image
    img = Image.fromarray(img_array)
    img.save(filename)
    
    return filename


def generate_test_data(num_reports: int = 10):
    """
    Generate sample pollution reports for testing.
    
    Args:
        num_reports: Number of sample reports to create
    """
    # Initialize database
    init_database()
    
    # Create uploads directory
    upload_dir = os.path.join(os.path.dirname(__file__), "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    
    pollution_types = ["plastic", "oil_spill", "other_solid_waste", "marine_debris"]
    
    print(f"\n🧪 Generating {num_reports} test pollution reports...\n")
    
    for i in range(num_reports):
        # Random pollution type
        ptype = random.choice(pollution_types)
        
        # Random location (with small offset for variety)
        location = random.choice(SAMPLE_LOCATIONS)
        lat = location["lat"] + random.uniform(-0.05, 0.05)
        lng = location["lng"] + random.uniform(-0.05, 0.05)
        
        # Random description
        desc = random.choice(DESCRIPTIONS[ptype])
        
        # Create sample image
        filename = f"test_{i+1}_{ptype}.jpg"
        filepath = os.path.join(upload_dir, filename)
        create_sample_image(ptype, filepath)
        
        # Random confidence
        confidence = round(random.uniform(0.65, 0.95), 2)
        
        # Insert into database
        report_id = insert_report(
            image_path=filename,
            latitude=lat,
            longitude=lng,
            pollution_type=ptype,
            confidence=confidence,
            description=desc
        )
        
        print(f"  ✅ Report #{report_id}: {ptype} at {location['name']}")
        print(f"     📍 ({lat:.4f}, {lng:.4f}) - {confidence:.0%} confidence")
    
    print(f"\n✨ Generated {num_reports} test reports successfully!")
    print(f"📁 Images saved in: {upload_dir}")
    print("\n💡 You can now view these reports on the map!")


if __name__ == "__main__":
    generate_test_data(10)
