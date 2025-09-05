from app import StableDiffusionService
import time

# Generate ULTRA HIGH-END portrait animation frames at 512x512, 64 steps
service = StableDiffusionService()
service.load_model()

print('=== ULTRA HIGH-END PORTRAIT ANIMATION (512x512, 64 steps) ===')

# Ultra high-quality portrait animation frames
frames = [
    ("ultra_hq_portrait_1_forward.png", "portrait of an elegant Asian woman in her 50s with short black hair, looking directly forward, gentle smile, detailed realistic style, professional lighting"),
    ("ultra_hq_portrait_2_slight_turn.png", "portrait of an elegant Asian woman in her 50s with short black hair, head slightly turned left, beginning to smile, detailed realistic style, professional lighting"),
    ("ultra_hq_portrait_3_turn_smile.png", "portrait of an elegant Asian woman in her 50s with short black hair, head turned left, warm smile, detailed realistic style, professional lighting"),
    ("ultra_hq_portrait_4_full_smile.png", "portrait of an elegant Asian woman in her 50s with short black hair, head turned left, bright genuine smile, detailed realistic style, professional lighting"),
    ("ultra_hq_portrait_5_turn_back.png", "portrait of an elegant Asian woman in her 50s with short black hair, head turning back to center, maintaining smile, detailed realistic style, professional lighting"),
    ("ultra_hq_portrait_6_center_smile.png", "portrait of an elegant Asian woman in her 50s with short black hair, looking forward, radiating warmth with beautiful smile, detailed realistic style, professional lighting")
]

total_start = time.time()

for i, (filename, prompt) in enumerate(frames, 1):
    print(f'\nFrame {i}/6: {filename}')
    print(f'Generating: {prompt[:60]}...')
    
    start = time.time()
    # Ultra high-end: 512x512 with 64 steps for maximum possible quality
    img, error = service.generate_image(prompt, 64, 512, 512)
    gen_time = time.time() - start
    
    if img:
        img.save(filename)
        print(f'SUCCESS: Generated in {gen_time:.1f}s')
    else:
        print(f'FAILED: {error}')

total_time = time.time() - total_start
print(f'\n=== ULTRA HIGH-END PORTRAIT COMPLETE ===')
print(f'Total time: {total_time:.1f}s for 6 frames')
print(f'Average: {total_time/6:.1f}s per frame')
print(f'Quality: Ultra maximum detail and realism (64 steps)')
print('\nGenerated files:')
for filename, _ in frames:
    print(f'  - {filename}')