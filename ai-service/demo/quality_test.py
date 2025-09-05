from app import StableDiffusionService
import time

# Quality comparison test
service = StableDiffusionService()
service.load_model()

prompt = 'a small cute robot with glowing blue eyes, detailed metallic surface'

print('=== QUALITY COMPARISON TEST ===')
print('Generating HIGH QUALITY version (512x512, 15 steps)...')

start = time.time()
img_hq, _ = service.generate_image(prompt, 15, 512, 512)
time_hq = time.time() - start

if img_hq:
    img_hq.save('high_quality_robot.png')
    print(f'HIGH QUALITY: {time_hq:.1f}s, Size: {img_hq.size}')
    print('Saved as: high_quality_robot.png')
    
    print(f'\nCOMPARISON:')
    print(f'  Fast (256x256, 5 steps):    ~5.2s')
    print(f'  High Quality (512x512, 15 steps): {time_hq:.1f}s')
    print(f'  Quality improvement comes at {time_hq/5.2:.1f}x time cost')
else:
    print('Failed to generate high quality image')