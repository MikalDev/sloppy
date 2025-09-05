#!/usr/bin/env python3
"""Direct demo using the StableDiffusionService class"""

from app import StableDiffusionService
import time

def main():
    print("=== AI ART GENERATION DEMO ===")
    print("Initializing AI Art Service...")
    
    # Create service instance
    service = StableDiffusionService()
    
    print("Loading Stable Diffusion model...")
    start_time = time.time()
    
    if service.load_model():
        load_time = time.time() - start_time
        print(f"Model loaded successfully in {load_time:.1f}s")
        print(f"Device: {service.device}")
        print(f"Available memory: {service.get_memory_info()['available_gb']:.1f}GB")
        
        print("\nGenerating image: 'a beautiful red rose in a garden, photorealistic'")
        gen_start = time.time()
        
        image, error = service.generate_image(
            prompt="a beautiful red rose in a garden, photorealistic",
            steps=10,
            width=512,
            height=512
        )
        
        gen_time = time.time() - gen_start
        
        if image:
            filename = "beautiful_rose_demo.png"
            image.save(filename)
            
            print(f"SUCCESS! Image generated in {gen_time:.1f}s")
            print(f"Image size: {image.size}")
            print(f"Saved as: {filename}")
            print(f"Memory after generation: {service.get_memory_info()['available_gb']:.1f}GB")
            
            return filename
        else:
            print(f"FAILED: {error}")
            return None
    else:
        print("Failed to load model")
        return None

if __name__ == "__main__":
    filename = main()
    if filename:
        print(f"\nYour AI-generated image is ready!")
        print(f"File location: {filename}")
        print("You can now open this image in any image viewer to see the beautiful rose!")