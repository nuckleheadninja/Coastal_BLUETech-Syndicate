"""
🧠 Coastal Pollution Classifier - Powered by OpenAI CLIP
=======================================================
Uses CLIP (Contrastive Language-Image Pre-training) for high-accuracy 
zero-shot classification. No training required.
"""

from PIL import Image
import numpy as np
import os
from pathlib import Path

# Try to import CLIP
try:
    from transformers import CLIPProcessor, CLIPModel
    import torch
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    USE_CLIP = True
    print("✅ CLIP model loaded successfully!")
except ImportError:
    USE_CLIP = False
    print("⚠️ CLIP not available. Installing...")

CATEGORIES = ['plastic', 'oil_spill', 'other_solid_waste', 'marine_debris', 'no_waste']

def classify_pollution(image_path: str) -> tuple:
    """Classify pollution using CLIP AI."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    # Validation check
    try:
        with Image.open(image_path) as img:
            img.verify()
    except:
        return "other_solid_waste", 0.0

    if USE_CLIP:
        try:
            image = Image.open(image_path).convert("RGB")
            
            # Labels designed to only match OBVIOUS pollution
            # Order: plastic, oil_spill, solid_waste, marine_debris, no_waste
            labels = [
                "plastic bottles and plastic bags littering a beach with visible garbage",
                "oil spill petroleum contamination dark brown black murky polluted water",
                "garbage pile trash heap rubbish dump on sandy beach",
                "fishing nets ropes tangled in water or on beach shore",
                "natural clean ocean water waves sea view without any garbage or pollution"
            ]
            
            inputs = processor(text=labels, images=image, return_tensors="pt", padding=True)
            
            with torch.no_grad():
                outputs = model(**inputs)
                probs = outputs.logits_per_image.softmax(dim=1)[0]
            
            # Get all probabilities
            all_probs = probs.tolist()
            idx = probs.argmax().item()
            confidence = probs[idx].item()
            no_waste_prob = all_probs[4]  # no_waste is index 4
            
            # Map back to category keys
            category_map = {
                0: "plastic",
                1: "oil_spill",
                2: "other_solid_waste",
                3: "marine_debris",
                4: "no_waste"
            }
            
            predicted = category_map[idx]
            
            # CONFIDENCE THRESHOLD: If confidence is below 85% for pollution categories,
            # default to no_waste (to avoid false positives)
            if predicted != "no_waste" and confidence < 0.85:
                # Check if no_waste probability is reasonable (>15%)
                if no_waste_prob > 0.15:
                    print(f"🧠 Low confidence ({confidence*100:.1f}%) - defaulting to no_waste")
                    predicted = "no_waste"
                    confidence = no_waste_prob
            
            print(f"🧠 CLIP Prediction: {predicted} ({confidence*100:.1f}%)")
            
            return predicted, round(confidence, 4)
            
        except Exception as e:
            print(f"CLIP Error: {e}")
            return "other_solid_waste", 0.5
    
    else:
        # Fallback if CLIP fails (should not happen after install)
        return "other_solid_waste", 0.5


def extract_gps_from_exif(image_path: str) -> dict:
    """Extract GPS from EXIF."""
    try:
        img = Image.open(image_path)
        exif = img._getexif()
        if not exif: return {'has_gps': False}
        
        gps = exif.get(34853)
        if not gps: return {'has_gps': False}
        
        def to_deg(v): return float(v[0]) + float(v[1])/60 + float(v[2])/3600
        
        lat = to_deg(gps[2])
        lon = to_deg(gps[4])
        
        if gps.get(1) == 'S': lat = -lat
        if gps.get(3) == 'W': lon = -lon
        
        return {'has_gps': True, 'latitude': lat, 'longitude': lon}
    except:
        return {'has_gps': False}


def validate_image(image_path: str) -> dict:
    """Validate image."""
    try:
        img = Image.open(image_path)
        w, h = img.size
        
        if min(w, h) < 100:
            return {
                'is_valid': False, 
                'is_suspicious': True, 
                'confidence_penalty': 0.5, 
                'warnings': ['Too small']
            }
        
        return {
            'is_valid': True,
            'is_suspicious': False, 
            'confidence_penalty': 0.0,
            'warnings': []
        }
    except Exception as e:
        return {
            'is_valid': False, 
            'is_suspicious': True,
            'confidence_penalty': 0.5, 
            'warnings': [str(e)]
        }


def get_pollution_info(ptype: str) -> dict:
    info = {
        "plastic": {"name": "Plastic Pollution", "icon": "🥤", "color": "#ef4444"},
        "oil_spill": {"name": "Oil Spill", "icon": "🛢️", "color": "#1f2937"},
        "other_solid_waste": {"name": "Solid Waste", "icon": "🗑️", "color": "#92400e"},
        "marine_debris": {"name": "Marine Debris", "icon": "🎣", "color": "#0ea5e9"},
        "no_waste": {"name": "No Waste Detected", "icon": "✅", "color": "#22c55e"}
    }
    return info.get(ptype, info["other_solid_waste"])


def analyze_image(image_path: str) -> dict:
    """Wrapper for main classification logic."""
    label, confidence = classify_pollution(image_path)
    info = get_pollution_info(label)
    return {
        "label": label,
        "confidence": confidence,
        "pollution_name": info["name"],
        "pollution_icon": info["icon"],
        "pollution_color": info["color"]
    }


def extract_gps_data(image_path: str) -> dict:
    """Wrapper for GPS extraction."""
    return extract_gps_from_exif(image_path)

