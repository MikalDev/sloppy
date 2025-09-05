#!/usr/bin/env python3
"""Simple demo script to generate and display an image from the AI art service"""

import requests
import json
import base64
from PIL import Image
import io
import time

def generate_image():
    print("Generating image...")
    start_time = time.time()

    try:
        response = requests.post(
            'http://localhost:8080/generate',
            json={
                'prompt': 'a beautiful red rose in a garden, photorealistic',
                'steps': 8,
                'width': 512,
                'height': 512
            },
            timeout=120
        )

        end_time = time.time()
        print(f"Request completed in {end_time - start_time:.2f} seconds")

        if response.status_code == 200:
            data = response.json()
            if data['success']:
                # Decode base64 image
                image_data = base64.b64decode(data['image'])
                image = Image.open(io.BytesIO(image_data))
                
                # Save the image
                filename = 'generated_rose.png'
                image.save(filename)
                
                print(f"SUCCESS: Image generated and saved as {filename}")
                print(f"  Size: {image.size}")
                print(f"  Generation time: {data['generation_time']}s")
                print(f"  Model: {data['model_type']}")
                print(f"  Device: {data['device']}")
                print(f"  Memory after: {data['memory_after']['available_gb']:.1f}GB available")
                
                return filename
            else:
                print(f"FAILED: Generation failed: {data['error']}")
                return None
        else:
            print(f"ERROR: Request failed: {response.status_code}")
            print(response.text)
            return None
            
    except requests.exceptions.Timeout:
        print("TIMEOUT: Request timed out - model may be loading for the first time")
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    filename = generate_image()
    if filename:
        print(f"\nImage saved successfully!")
        print(f"  Location: {filename}")
        print(f"  You can now view the image in your file explorer or image viewer")