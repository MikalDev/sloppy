from app import StableDiffusionService
import time
from PIL import Image

# Img2img demonstration using an existing image as seed
service = StableDiffusionService()
service.load_model()

print('=== IMG2IMG DEMONSTRATION ===')

# Use one of the existing generated images as input
input_image_path = "hq_portrait_1_forward.png"
try:
    input_image = Image.open(input_image_path)
    print(f"Using input image: {input_image_path} ({input_image.size})")
except FileNotFoundError:
    print(f"Input image {input_image_path} not found. Generating a simple one...")
    # Create a simple colored image as fallback
    input_image = Image.new('RGB', (512, 512), (100, 150, 200))
    input_image.save("simple_input.png")
    print("Created simple_input.png as seed image")

# Test different strength levels
tests = [
    (0.3, "Low change - mostly preserves original"),
    (0.5, "Moderate change - balanced transformation"), 
    (0.8, "High change - significant transformation")
]

prompt = "a cyberpunk portrait with neon lighting and digital effects"

print(f"\nBase prompt: {prompt}")
print(f"Input image size: {input_image.size}")

for strength, description in tests:
    print(f"\n--- Strength {strength}: {description} ---")
    
    start = time.time()
    result_image, error = service.img2img_generate(
        prompt=prompt,
        init_image=input_image,
        strength=strength,
        steps=8,
        width=256,  # Using smaller size for speed
        height=256
    )
    gen_time = time.time() - start
    
    if result_image:
        filename = f"img2img_strength_{strength}.png"
        result_image.save(filename)
        print(f"SUCCESS: Generated in {gen_time:.1f}s -> {filename}")
    else:
        print(f"FAILED: {error}")

print(f"\n=== IMG2IMG DEMO COMPLETE ===")
print("Generated files:")
print("  - img2img_strength_0.3.png (low change)")  
print("  - img2img_strength_0.5.png (moderate change)")
print("  - img2img_strength_0.8.png (high change)")
print("\nStrength values:")
print("  0.1-0.3: Minimal changes, preserves most details")
print("  0.4-0.6: Balanced transformation") 
print("  0.7-1.0: Major changes, uses image mainly for composition")