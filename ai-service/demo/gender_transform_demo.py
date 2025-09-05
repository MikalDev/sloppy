from app import StableDiffusionService
import time
from PIL import Image

# Gender transformation demonstration using img2img
service = StableDiffusionService()
service.load_model()

print('=== GENDER TRANSFORMATION DEMO ===')

# Use one of the existing female portraits as input
input_image_path = "hq_portrait_1_forward.png"
try:
    input_image = Image.open(input_image_path)
    print(f"Using input image: {input_image_path} (female portrait)")
    print(f"Image size: {input_image.size}")
except FileNotFoundError:
    print(f"Input image {input_image_path} not found!")
    exit()

# Different transformation prompts with varying strength
transformations = [
    (0.4, "portrait of an elegant Asian man in his 50s with short black hair, looking directly forward, gentle smile, detailed realistic style, professional lighting"),
    (0.6, "portrait of a distinguished Asian businessman in his 50s with short black hair, confident expression, detailed realistic style, professional lighting"),
    (0.8, "portrait of a mature Asian man in his 50s with short black hair, warm smile, masculine features, detailed realistic style, professional lighting")
]

print(f"\nStarting transformation sequence...")
print(f"Original: Female Asian portrait")

for i, (strength, prompt) in enumerate(transformations, 1):
    print(f"\n--- Transformation {i}: Strength {strength} ---")
    print(f"Target: {prompt[:60]}...")
    
    start = time.time()
    result_image, error = service.img2img_generate(
        prompt=prompt,
        init_image=input_image,
        strength=strength,
        steps=10,
        width=512,  # Keep original resolution for better quality
        height=512
    )
    gen_time = time.time() - start
    
    if result_image:
        filename = f"gender_transform_step_{i}_strength_{strength}.png"
        result_image.save(filename)
        print(f"SUCCESS: Generated in {gen_time:.1f}s -> {filename}")
    else:
        print(f"FAILED: {error}")

# Also create a side-by-side comparison
print(f"\n--- Creating progressive sequence ---")
sequence_prompts = [
    (0.3, "portrait of an elegant person transitioning, androgynous features, detailed realistic style"),
    (0.5, "portrait of an elegant Asian person with masculine-leaning features, short black hair, detailed realistic style"), 
    (0.7, "portrait of an elegant Asian man in his 50s with short black hair, gentle masculine features, detailed realistic style")
]

for i, (strength, prompt) in enumerate(sequence_prompts, 4):
    print(f"\nSequence step {i-3}: Strength {strength}")
    
    start = time.time()
    result_image, error = service.img2img_generate(
        prompt=prompt,
        init_image=input_image,
        strength=strength,
        steps=10,
        width=512,
        height=512
    )
    gen_time = time.time() - start
    
    if result_image:
        filename = f"gender_sequence_step_{i-3}_strength_{strength}.png"
        result_image.save(filename)
        print(f"SUCCESS: Generated in {gen_time:.1f}s -> {filename}")
    else:
        print(f"FAILED: {error}")

print(f"\n=== GENDER TRANSFORMATION COMPLETE ===")
print("Generated transformation sequence:")
print("  Original -> hq_portrait_1_forward.png (female)")
print("  Step 1   -> gender_transform_step_1_strength_0.4.png")
print("  Step 2   -> gender_transform_step_2_strength_0.6.png") 
print("  Step 3   -> gender_transform_step_3_strength_0.8.png (male)")
print("\nProgressive sequence:")
print("  Step 1   -> gender_sequence_step_1_strength_0.3.png (androgynous)")
print("  Step 2   -> gender_sequence_step_2_strength_0.5.png (masculine-leaning)")
print("  Step 3   -> gender_sequence_step_3_strength_0.7.png (masculine)")
print("\nStrength guide for gender transformation:")
print("  0.3-0.4: Subtle androgynous features")
print("  0.5-0.6: Clear gender shift with blended features")
print("  0.7-0.8: Strong masculine/feminine characteristics")