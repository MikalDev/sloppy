from app import StableDiffusionService
import time

# Quick speed test
service = StableDiffusionService()
service.load_model()

prompt = 'a small cute robot'

print('=== SPEED COMPARISON ===')

# Fast & Small
print('\n1. FAST (256x256, 5 steps):')
start = time.time()
img1, _ = service.generate_image(prompt, 5, 256, 256)
time1 = time.time() - start
if img1: 
    img1.save('fast_robot.png')
    print(f'   Time: {time1:.1f}s, Size: {img1.size}')

# Balanced
print('\n2. BALANCED (384x384, 8 steps):')
start = time.time()  
img2, _ = service.generate_image(prompt, 8, 384, 384)
time2 = time.time() - start
if img2:
    img2.save('balanced_robot.png') 
    print(f'   Time: {time2:.1f}s, Size: {img2.size}')

print(f'\nRESULTS:')
print(f'   Fast setting is {time2/time1:.1f}x FASTER')
print(f'   Time savings: {time2-time1:.1f} seconds')
print(f'\nFor games: Use 256x256 with 5-8 steps for responsive generation!')