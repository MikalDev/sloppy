from app import StableDiffusionService
import time

# Generate BALANCED horse running animation frames at 256x256, 8 steps
service = StableDiffusionService()
service.load_model()

print('=== BALANCED HORSE RUNNING ANIMATION (256x256, 8 steps) ===')

# Balanced animation frames
frames = [
    ("balanced_horse_1_standing.png", "a majestic horse standing still, side view, detailed realistic style"),
    ("balanced_horse_2_lift.png", "a horse lifting front legs to start running, side view, detailed realistic style"), 
    ("balanced_horse_3_gallop1.png", "a horse in full gallop with front legs extended forward, side view, detailed realistic style"),
    ("balanced_horse_4_gallop2.png", "a horse in mid-gallop with all legs tucked under body, side view, detailed realistic style"),
    ("balanced_horse_5_gallop3.png", "a horse in full gallop with back legs extended, side view, detailed realistic style"),
    ("balanced_horse_6_landing.png", "a horse landing from gallop with front legs touching ground, side view, detailed realistic style")
]

total_start = time.time()

for i, (filename, prompt) in enumerate(frames, 1):
    print(f'\nFrame {i}/6: {filename}')
    
    start = time.time()
    # Balanced: 256x256 with 8 steps for better quality than 5 steps
    img, error = service.generate_image(prompt, 8, 256, 256)
    gen_time = time.time() - start
    
    if img:
        img.save(filename)
        print(f'SUCCESS: Generated in {gen_time:.1f}s')
    else:
        print(f'FAILED: {error}')

total_time = time.time() - total_start
print(f'\n=== BALANCED ANIMATION COMPLETE ===')
print(f'Total time: {total_time:.1f}s for 6 frames')
print(f'Average: {total_time/6:.1f}s per frame')
print(f'Quality: Better than 5 steps, faster than 512x512')
print('\nGenerated files:')
for filename, _ in frames:
    print(f'  - {filename}')