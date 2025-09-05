from app import StableDiffusionService
import time
import torch

print("=== GPU ACCELERATION TEST ===")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")
print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f}GB" if torch.cuda.is_available() else "No GPU")

# Test GPU generation
service = StableDiffusionService()
print(f"\nDetected device: {service.device}")

if service.device == "cuda":
    print("GPU acceleration is ENABLED!")
    
    print("\nLoading model on GPU...")
    start = time.time()
    service.load_model()
    load_time = time.time() - start
    print(f"Model loaded in {load_time:.1f}s")
    
    print(f"\nGPU Memory after loading: {torch.cuda.memory_allocated(0) / 1024**3:.2f}GB")
    
    print("\nGenerating test image on GPU...")
    start = time.time()
    img, error = service.generate_image("a futuristic city skyline", 8, 512, 512)
    gen_time = time.time() - start
    
    if img:
        img.save("gpu_test_city.png")
        print(f"SUCCESS! GPU generation in {gen_time:.1f}s")
        print(f"Expected speedup: 3-5x faster than CPU ({38.0/gen_time:.1f}x)")
        print(f"GPU Memory used: {torch.cuda.memory_allocated(0) / 1024**3:.2f}GB")
        print("Saved as: gpu_test_city.png")
    else:
        print(f"FAILED: {error}")
        
else:
    print("WARNING: GPU acceleration is NOT enabled!")
    print("The service is still using CPU mode.")