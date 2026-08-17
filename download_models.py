#!/usr/bin/env python3
"""
Download SSD MobileNet v1 models for Face-API.js
"""
import os
import urllib.request
import json

def download_file(url, filepath):
    """Download a file from URL to filepath"""
    print(f"Downloading {os.path.basename(filepath)}...")
    try:
        urllib.request.urlretrieve(url, filepath)
        print(f"✅ Downloaded {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {os.path.basename(filepath)}: {e}")
        return False

def download_ssd_mobilenet_models():
    """Download all SSD MobileNet v1 model files"""
    
    # Create directory
    model_dir = "models/ssd_mobilenetv1"
    os.makedirs(model_dir, exist_ok=True)
    
    # Base URL for face-api.js models
    base_url = "https://github.com/justadudewhohacks/face-api.js/raw/master/weights"
    
    # Files to download for SSD MobileNet v1
    files = [
        "ssd_mobilenetv1_model-weights_manifest.json",
        "ssd_mobilenetv1_model-shard1",
        "ssd_mobilenetv1_model-shard2"  # Try downloading shard2 as well
    ]
    
    success_count = 0
    for filename in files:
        url = f"{base_url}/{filename}"
        filepath = os.path.join(model_dir, filename)
        if download_file(url, filepath):
            success_count += 1
    
    print(f"\n📊 Downloaded {success_count}/{len(files)} files")
    
    # Check if we have the minimum required files
    required_files = [
        os.path.join(model_dir, "ssd_mobilenetv1_model-weights_manifest.json"),
        os.path.join(model_dir, "ssd_mobilenetv1_model-shard1")
    ]
    
    if all(os.path.exists(f) for f in required_files):
        print("✅ SSD MobileNet v1 models downloaded successfully!")
        return True
    else:
        print("❌ Some required files are missing")
        return False

if __name__ == "__main__":
    print("🚀 Downloading SSD MobileNet v1 models...")
    if download_ssd_mobilenet_models():
        print("\n🎯 You can now use SSD MobileNet v1 in your face recognition app!")
    else:
        print("\n⚠️  Download failed. You can still use TinyFaceDetector models.")
