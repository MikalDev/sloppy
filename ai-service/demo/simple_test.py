#!/usr/bin/env python3
"""Simple AI Art Service Test - ASCII only for Windows compatibility"""

import requests
import json
import time

def test_health():
    """Test health endpoint"""
    print("\n=== HEALTH CHECK ===")
    try:
        response = requests.get("http://localhost:8080/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("SUCCESS: Service is healthy!")
            print(f"  Version: {data.get('version', 'Unknown')}")
            print(f"  Status: {data.get('status', 'Unknown')}")
            print(f"  Model Loaded: {data.get('model_loaded', 'Unknown')}")
            return True
        else:
            print(f"ERROR: Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: Failed to connect - {e}")
        return False

def test_generation():
    """Test image generation endpoint"""
    print("\n=== IMAGE GENERATION TEST ===")
    try:
        payload = {
            "prompt": "a red apple",
            "steps": 5
        }
        
        print(f"Prompt: '{payload['prompt']}'")
        print(f"Steps: {payload['steps']}")
        print("Sending request... (this may take a while for first generation)")
        
        start_time = time.time()
        response = requests.post(
            "http://localhost:8080/generate",
            json=payload,
            timeout=120
        )
        end_time = time.time()
        
        print(f"Request completed in {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success"):
                print("SUCCESS: Image generated!")
                print(f"  Generation Time: {data.get('generation_time', 'Unknown')}s")
                print(f"  Model Type: {data.get('model_type', 'Unknown')}")
                print(f"  Image Size: {len(data.get('image', ''))} base64 characters")
                return True
            else:
                print(f"FAILED: Generation error - {data.get('error', 'Unknown')}")
                return False
        else:
            print(f"ERROR: Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out - model may still be loading")
        return False
    except Exception as e:
        print(f"ERROR: Request failed - {e}")
        return False

def main():
    """Main test function"""
    print("AI ART SERVICE - SIMPLE TEST")
    print("============================")
    
    # Test 1: Health check
    health_ok = test_health()
    if not health_ok:
        print("\nService not available. Please start the service first:")
        print("  cd ai-art-game/ai-service && uv run python app.py")
        return
    
    # Test 2: Generation
    generation_ok = test_generation()
    
    # Summary
    print("\n=== TEST SUMMARY ===")
    print(f"Health Check: {'PASS' if health_ok else 'FAIL'}")
    print(f"Image Generation: {'PASS' if generation_ok else 'FAIL'}")
    
    if health_ok and generation_ok:
        print("\nSUCCESS: All tests passed! The AI Art Service is working.")
    else:
        print("\nSome tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()