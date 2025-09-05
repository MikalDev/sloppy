#!/usr/bin/env python3
"""Speed and size optimization demo for AI art generation"""

from app import StableDiffusionService
import time

def benchmark_settings():
    """Test different settings to show speed vs quality tradeoffs"""
    
    print("=== AI ART SPEED & SIZE OPTIMIZATION DEMO ===\n")
    
    # Initialize service
    service = StableDiffusionService()
    
    print("Loading model...")
    if not service.load_model():
        print("Failed to load model")
        return
    
    prompt = "a cute cat sitting on a windowsill"
    
    # Different configuration presets
    configs = [
        {
            "name": "FAST & SMALL",
            "width": 256,
            "height": 256,
            "steps": 5,
            "description": "Ultra-fast generation for quick previews"
        },
        {
            "name": "BALANCED",
            "width": 384,
            "height": 384,
            "steps": 8,
            "description": "Good balance of speed and quality"
        },
        {
            "name": "HIGH QUALITY",
            "width": 512,
            "height": 512,
            "steps": 15,
            "description": "Best quality but slower"
        }
    ]
    
    results = []
    
    for i, config in enumerate(configs):
        print(f"\n--- Test {i+1}: {config['name']} ---")
        print(f"Settings: {config['width']}x{config['height']}, {config['steps']} steps")
        print(f"Purpose: {config['description']}")
        
        start_time = time.time()
        
        image, error = service.generate_image(
            prompt=prompt,
            steps=config['steps'],
            width=config['width'],
            height=config['height']
        )
        
        generation_time = time.time() - start_time
        
        if image:
            filename = f"cat_{config['name'].lower().replace(' ', '_')}.png"
            image.save(filename)
            
            # Calculate file size
            import os
            file_size_kb = os.path.getsize(filename) / 1024
            
            result = {
                **config,
                'time': generation_time,
                'filename': filename,
                'file_size_kb': file_size_kb,
                'pixels': config['width'] * config['height']
            }
            results.append(result)
            
            print(f"✓ Generated in {generation_time:.1f}s")
            print(f"  File: {filename} ({file_size_kb:.1f}KB)")
            print(f"  Pixels: {result['pixels']:,}")
        else:
            print(f"✗ Failed: {error}")
    
    # Summary comparison
    print(f"\n{'='*60}")
    print("SPEED & SIZE COMPARISON SUMMARY")
    print(f"{'='*60}")
    print(f"{'Config':<15} {'Time':<8} {'Size':<10} {'File KB':<10} {'Pixels':<10}")
    print("-" * 60)
    
    for result in results:
        print(f"{result['name']:<15} {result['time']:.1f}s{'':<3} "
              f"{result['width']}x{result['height']:<4} "
              f"{result['file_size_kb']:.1f}KB{'':<4} "
              f"{result['pixels']:,}")
    
    if len(results) >= 2:
        fast_time = results[0]['time']
        slow_time = results[-1]['time'] 
        speedup = slow_time / fast_time
        
        print(f"\n🚀 SPEED IMPROVEMENT:")
        print(f"   {results[0]['name']} is {speedup:.1f}x FASTER than {results[-1]['name']}")
        print(f"   ({fast_time:.1f}s vs {slow_time:.1f}s)")

def show_optimization_tips():
    """Show specific optimization recommendations"""
    
    print(f"\n{'='*60}")
    print("🔧 OPTIMIZATION RECOMMENDATIONS")
    print(f"{'='*60}")
    
    tips = [
        {
            "category": "RESOLUTION",
            "tips": [
                "256x256: Ultra-fast (~5-8s), good for previews",
                "384x384: Balanced speed/quality (~12-18s)",
                "512x512: High quality (~25-35s)",
                "Lower resolution = 4x speed improvement"
            ]
        },
        {
            "category": "INFERENCE STEPS", 
            "tips": [
                "5 steps: Very fast, decent quality",
                "8-10 steps: Good balance (recommended)",
                "15+ steps: Diminishing returns on quality",
                "Each step adds ~2-3 seconds"
            ]
        },
        {
            "category": "MEMORY OPTIMIZATION",
            "tips": [
                "Current auto-reduction when <4GB available",
                "Manual reduction for consistent performance",
                "Smaller images use less VRAM/RAM",
                "Batch processing for multiple images"
            ]
        },
        {
            "category": "PRACTICAL USE CASES",
            "tips": [
                "Game previews: 256x256, 5 steps (~5s)",
                "Social media: 384x384, 8 steps (~15s)", 
                "High-res prints: 512x512, 15 steps (~30s)",
                "Real-time demos: 256x256, 3-5 steps"
            ]
        }
    ]
    
    for tip_group in tips:
        print(f"\n📋 {tip_group['category']}:")
        for tip in tip_group['tips']:
            print(f"   • {tip}")

if __name__ == "__main__":
    benchmark_settings()
    show_optimization_tips()
    
    print(f"\n{'='*60}")
    print("🎯 RECOMMENDATION FOR GAMES:")
    print("   Use 256x256 with 5-8 steps for fast, responsive gameplay")
    print("   This gives ~5-10 second generation times with good quality")
    print(f"{'='*60}")