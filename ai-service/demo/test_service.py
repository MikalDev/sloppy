#!/usr/bin/env python3
"""
Local AI Art Service Tester and Visualizer

This script tests the AI art service without needing a web browser.
It can save images locally and display them using PIL/matplotlib.
"""

import requests
import json
import base64
import time
from PIL import Image
import io
import os
from datetime import datetime

class AIArtTester:
    def __init__(self, service_url="http://localhost:8080"):
        self.service_url = service_url
        self.output_dir = "generated_images"
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Created output directory: {self.output_dir}")
    
    def test_health(self):
        """Test the health endpoint"""
        print("\n=== HEALTH CHECK ===")
        try:
            response = requests.get(f"{self.service_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print("OK: Service is healthy!")
                print(f"  Version: {data.get('version', 'Unknown')}")
                print(f"  Status: {data.get('status', 'Unknown')}")
                print(f"  Model Loaded: {data.get('model_loaded', 'Unknown')}")
                print(f"  Service: {data.get('service', 'Unknown')}")
                return True
            else:
                print(f"ERROR: Health check failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to connect to service: {e}")
            return False
    
    def generate_and_save_image(self, prompt, steps=10, seed=None):
        """Generate an image and save it locally"""
        print(f"\n=== GENERATING IMAGE ===")
        print(f"Prompt: '{prompt}'")
        print(f"Steps: {steps}")
        
        # Prepare request
        payload = {
            "prompt": prompt,
            "steps": steps
        }
        if seed is not None:
            payload["seed"] = seed
            print(f"Seed: {seed}")
        
        try:
            print("⏳ Sending request to service...")
            start_time = time.time()
            
            response = requests.post(
                f"{self.service_url}/generate",
                json=payload,
                timeout=120  # 2 minutes timeout
            )
            
            request_time = time.time() - start_time
            print(f"📡 Request completed in {request_time:.2f}s")
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    # Decode base64 image
                    image_data = base64.b64decode(data["image"])
                    image = Image.open(io.BytesIO(image_data))
                    
                    # Generate filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    safe_prompt = "".join(c if c.isalnum() or c in " -_" else "" for c in prompt)[:50]
                    filename = f"{timestamp}_{safe_prompt.strip().replace(' ', '_')}.png"
                    filepath = os.path.join(self.output_dir, filename)
                    
                    # Save image
                    image.save(filepath)
                    
                    print("✓ Image generated successfully!")
                    print(f"  🎨 Size: {image.size}")
                    print(f"  ⏱️  Generation Time: {data.get('generation_time', 'Unknown')}s")
                    print(f"  🤖 Model Type: {data.get('model_type', 'Unknown')}")
                    print(f"  💾 Saved to: {filepath}")
                    
                    # Try to display image using PIL
                    try:
                        print("\n📱 Opening image...")
                        image.show()  # This will open the default image viewer
                    except Exception as e:
                        print(f"⚠️  Could not auto-open image: {e}")
                        print(f"   You can manually open: {filepath}")
                    
                    return filepath, data
                else:
                    print(f"✗ Generation failed: {data.get('error', 'Unknown error')}")
                    return None, data
            else:
                print(f"✗ Request failed with status {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Response: {response.text}")
                return None, None
                
        except requests.exceptions.Timeout:
            print("✗ Request timed out - the model might be loading for the first time")
            return None, None
        except requests.exceptions.RequestException as e:
            print(f"✗ Request failed: {e}")
            return None, None
    
    def run_test_suite(self):
        """Run a comprehensive test suite"""
        print("🧪 AI ART SERVICE TEST SUITE")
        print("="*50)
        
        # Test 1: Health check
        if not self.test_health():
            print("\n❌ Service is not available. Please start the AI service first.")
            return False
        
        # Test 2: Simple generation
        print("\n🎨 Test 1: Simple Generation")
        self.generate_and_save_image("a red apple", steps=5, seed=42)
        
        # Test 3: More complex prompt
        print("\n🎨 Test 2: Complex Prompt")
        self.generate_and_save_image("a beautiful landscape with mountains and a lake", steps=8)
        
        # Test 4: Art style prompt
        print("\n🎨 Test 3: Art Style")
        self.generate_and_save_image("pixel art of a small house", steps=6, seed=123)
        
        print(f"\n✅ Test suite completed!")
        print(f"📁 Check the '{self.output_dir}' directory for generated images")
        
        return True

def main():
    """Main function to run tests"""
    tester = AIArtTester()
    
    print("AI Art Service Local Tester")
    print("==========================")
    
    # Check if service is running
    print("Checking if service is available...")
    if not tester.test_health():
        print("\n❌ AI Art Service is not running!")
        print("Please start it first with: cd ai-service && uv run python app.py")
        return
    
    # Interactive mode
    while True:
        print("\n" + "="*50)
        print("OPTIONS:")
        print("1. Run full test suite")
        print("2. Generate single image")
        print("3. Health check only")
        print("4. Exit")
        
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                tester.run_test_suite()
            
            elif choice == "2":
                prompt = input("Enter prompt: ").strip()
                if prompt:
                    steps = input("Enter steps (default 10): ").strip()
                    steps = int(steps) if steps.isdigit() else 10
                    
                    seed_input = input("Enter seed (optional): ").strip()
                    seed = int(seed_input) if seed_input.isdigit() else None
                    
                    tester.generate_and_save_image(prompt, steps, seed)
                else:
                    print("Please enter a valid prompt.")
            
            elif choice == "3":
                tester.test_health()
            
            elif choice == "4":
                print("👋 Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter 1-4.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()