from flask import Flask, jsonify, request, send_from_directory, send_file, render_template_string
from flask_cors import CORS
import os
import time
import threading
import traceback
import psutil
import gc
import torch

VERSION = "1.7.0"

app = Flask(__name__)
CORS(app)

# Inline HTML template to avoid file path issues
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Art Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f0f0f0;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, textarea, select, button {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            box-sizing: border-box;
        }
        textarea {
            height: 80px;
            resize: vertical;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
            font-size: 16px;
            padding: 12px;
        }
        button:hover {
            background: #45a049;
        }
        button:disabled {
            background: #cccccc;
            cursor: not-allowed;
        }
        .status {
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
        }
        .status.loading {
            background: #e3f2fd;
            color: #1976d2;
        }
        .status.success {
            background: #e8f5e8;
            color: #2e7d32;
        }
        .status.error {
            background: #ffebee;
            color: #c62828;
        }
        .result {
            margin-top: 20px;
            text-align: center;
        }
        .result img {
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .preset-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }
        .preset-btn {
            flex: 1;
            padding: 8px 12px;
            background: #2196F3;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
        }
        .preset-btn:hover {
            background: #1976D2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 AI Art Generator</h1>
        <p style="text-align: center; color: #666;">Create amazing images with AI using your RTX 4070!</p>
        
        <form id="artForm">
            <div class="form-group">
                <label for="prompt">Prompt:</label>
                <div class="preset-buttons">
                    <button type="button" class="preset-btn" onclick="setPrompt('a majestic dragon soaring through clouds')">Dragon</button>
                    <button type="button" class="preset-btn" onclick="setPrompt('a cyberpunk cityscape with neon lights')">Cyberpunk</button>
                    <button type="button" class="preset-btn" onclick="setPrompt('a serene forest landscape with a waterfall')">Nature</button>
                    <button type="button" class="preset-btn" onclick="setPrompt('portrait of an elegant woman, professional lighting')">Portrait</button>
                </div>
                <textarea id="prompt" name="prompt" placeholder="Describe what you want to generate..." required>a beautiful sunset over mountains</textarea>
            </div>
            
            <div class="form-group">
                <label for="steps">Steps (5-50):</label>
                <select id="steps" name="steps">
                    <option value="5">5 - Ultra Fast (~0.3s)</option>
                    <option value="8" selected>8 - Balanced (~0.7s)</option>
                    <option value="15">15 - High Quality (~1.1s)</option>
                    <option value="30">30 - Maximum Quality (~2.0s)</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="size">Image Size:</label>
                <select id="size" name="size">
                    <option value="256">256x256 - Fastest</option>
                    <option value="384">384x384 - Balanced</option>
                    <option value="512" selected>512x512 - High Quality</option>
                </select>
            </div>
            
            <button type="submit" id="generateBtn">🚀 Generate Image</button>
        </form>
        
        <div id="status"></div>
        <div id="result" class="result"></div>
    </div>

    <script>
        document.getElementById('artForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const prompt = document.getElementById('prompt').value;
            const steps = parseInt(document.getElementById('steps').value);
            const size = parseInt(document.getElementById('size').value);
            
            const generateBtn = document.getElementById('generateBtn');
            const status = document.getElementById('status');
            const result = document.getElementById('result');
            
            generateBtn.disabled = true;
            generateBtn.textContent = '⏳ Generating...';
            status.innerHTML = '<div class="status loading">🎨 Creating your masterpiece with GPU acceleration...</div>';
            result.innerHTML = '';
            
            const startTime = Date.now();
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        prompt: prompt,
                        steps: steps,
                        width: size,
                        height: size
                    })
                });
                
                const data = await response.json();
                const endTime = Date.now();
                const duration = (endTime - startTime) / 1000;
                
                if (data.success) {
                    status.innerHTML = `<div class="status success">✅ Generated in ${duration.toFixed(1)}s using RTX 4070!</div>`;
                    result.innerHTML = `<img src="data:image/png;base64,${data.image}" alt="Generated image">`;
                } else {
                    status.innerHTML = `<div class="status error">❌ Error: ${data.error}</div>`;
                }
            } catch (error) {
                const endTime = Date.now();
                const duration = (endTime - startTime) / 1000;
                status.innerHTML = `<div class="status error">❌ Network error after ${duration.toFixed(1)}s: ${error.message}</div>`;
            }
            
            generateBtn.disabled = false;
            generateBtn.textContent = '🚀 Generate Image';
        });
        
        function setPrompt(text) {
            document.getElementById('prompt').value = text;
        }
    </script>
</body>
</html>
'''

class StableDiffusionService:
    def __init__(self):
        self.pipeline = None
        self.img2img_pipeline = None
        self.model_loaded = False
        self.load_lock = threading.Lock()
        self.device = self._get_best_device()
        self.provider = self._get_onnx_provider()
        
    def _get_best_device(self):
        """Determine the best available device"""
        if torch.cuda.is_available():
            return "cuda"
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
            
    def _get_onnx_provider(self):
        """Get the best ONNX Runtime provider"""
        try:
            import onnxruntime as ort
            available_providers = ort.get_available_providers()
            print(f"Available ONNX providers: {available_providers}")
            
            if self.device == "cuda" and "CUDAExecutionProvider" in available_providers:
                return "CUDAExecutionProvider"
            elif "DmlExecutionProvider" in available_providers:
                # Use DirectML for better performance
                return "DmlExecutionProvider"
            else:
                # Default to CPU provider which should always be available
                return "CPUExecutionProvider"
        except ImportError:
            return "CPUExecutionProvider"
            
    def get_memory_info(self):
        """Get current memory usage information"""
        memory = psutil.virtual_memory()
        return {
            "total_gb": round(memory.total / (1024**3), 2),
            "available_gb": round(memory.available / (1024**3), 2),
            "used_gb": round(memory.used / (1024**3), 2),
            "percent": memory.percent
        }
    
    def load_model(self):
        """Load Stable Diffusion ONNX model using Hugging Face Optimum"""
        if self.model_loaded:
            return True
            
        try:
            with self.load_lock:
                if self.model_loaded:
                    return True
                
                print(f"Loading Stable Diffusion model with device: {self.device}")
                print(f"Available memory: {self.get_memory_info()['available_gb']:.1f}GB")
                
                # Use regular diffusers with a simple, compatible model
                from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
                
                # Try multiple models in order of preference (simplest first)
                models_to_try = [
                    "runwayml/stable-diffusion-v1-5",  # Most compatible
                    "CompVis/stable-diffusion-v1-4",   # Fallback 1  
                    "hf-internal-testing/tiny-stable-diffusion-torch"  # Fallback 2 (original)
                ]
                
                model_loaded = False
                for model_id in models_to_try:
                    try:
                        print(f"Attempting to load model: {model_id}")
                        
                        self.pipeline = StableDiffusionPipeline.from_pretrained(
                            model_id,
                            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                            safety_checker=None,
                            requires_safety_checker=False,
                            use_safetensors=True if "runwayml" in model_id or "CompVis" in model_id else False
                        )
                        self.pipeline = self.pipeline.to(self.device)
                        
                        # Enable memory efficient attention if available
                        if hasattr(self.pipeline.unet, 'set_attn_slice'):
                            self.pipeline.unet.set_attn_slice("auto")
                        
                        print(f"OK: StableDiffusionPipeline loaded successfully")
                        print(f"  Model: {model_id}")
                        print(f"  Device: {self.device}")
                        print(f"  Memory efficient attention: {hasattr(self.pipeline.unet, 'set_attn_slice')}")
                        
                        model_loaded = True
                        break
                        
                    except Exception as model_error:
                        print(f"Failed to load {model_id}: {model_error}")
                        continue
                
                if not model_loaded:
                    raise Exception("Failed to load any compatible model")
                
                # Load img2img pipeline using the same components
                print("Loading img2img pipeline...")
                self.img2img_pipeline = StableDiffusionImg2ImgPipeline(
                    vae=self.pipeline.vae,
                    text_encoder=self.pipeline.text_encoder,
                    tokenizer=self.pipeline.tokenizer,
                    unet=self.pipeline.unet,
                    scheduler=self.pipeline.scheduler,
                    safety_checker=None,
                    requires_safety_checker=False,
                    feature_extractor=getattr(self.pipeline, 'feature_extractor', None),
                )
                print("OK: Img2img pipeline loaded successfully")
                
                self.model_loaded = True
                
                # Force garbage collection after loading
                gc.collect()
                if self.device == "cuda":
                    torch.cuda.empty_cache()
                    
                print(f"Memory after loading: {self.get_memory_info()['available_gb']:.1f}GB available")
                return True
                
        except Exception as e:
            print(f"ERROR: Failed to load model: {e}")
            traceback.print_exc()
            return False
    
    def generate_image(self, prompt, steps=20, width=512, height=512):
        """Generate image from text prompt with memory management"""
        if not self.model_loaded:
            if not self.load_model():
                return None, "Model failed to load"
        
        # Check available memory before generation
        memory_info = self.get_memory_info()
        if memory_info["available_gb"] < 2.0:  # Require at least 2GB free
            gc.collect()
            if self.device == "cuda":
                torch.cuda.empty_cache()
            memory_info = self.get_memory_info()
            if memory_info["available_gb"] < 1.5:  # Still not enough after cleanup
                return None, f"Insufficient memory: {memory_info['available_gb']:.1f}GB available, need at least 1.5GB"
        
        try:
            print(f"Generating image for: {prompt}")
            print(f"Settings: {steps} steps, {width}x{height}, device: {self.device}")
            print(f"Memory before generation: {memory_info['available_gb']:.1f}GB available")
            
            # Reduce dimensions if memory is tight
            if memory_info["available_gb"] < 4.0:
                width = min(width, 256)
                height = min(height, 256)
                steps = min(steps, 10)
                print(f"Reduced settings due to memory: {steps} steps, {width}x{height}")
            
            generation_kwargs = {
                "prompt": prompt,
                "num_inference_steps": steps,
                "guidance_scale": 7.5,
                "width": width,
                "height": height
            }
            
            # Memory efficient attention is already enabled in load_model()
            # No need to set it again here as it persists
            
            image = self.pipeline(**generation_kwargs).images[0]
            
            # Clean up after generation
            gc.collect()
            if self.device == "cuda":
                torch.cuda.empty_cache()
                
            return image, None
            
        except Exception as e:
            error_msg = str(e)
            print(f"Generation failed: {error_msg}")
            traceback.print_exc()
            
            # Clean up on error
            gc.collect()
            if self.device == "cuda":
                torch.cuda.empty_cache()
                
            # Provide more specific error messages
            if "memory" in error_msg.lower() or "allocation" in error_msg.lower():
                return None, f"Out of memory error. Try reducing image size or inference steps. Available: {self.get_memory_info()['available_gb']:.1f}GB"
            elif "cuda" in error_msg.lower():
                return None, f"CUDA error: {error_msg}"
            else:
                return None, f"Generation error: {error_msg}"

    def img2img_generate(self, prompt, init_image, strength=0.75, steps=20, width=512, height=512):
        """Generate image from text prompt and initial image with memory management"""
        if not self.model_loaded:
            if not self.load_model():
                return None, "Model failed to load"
        
        # Check available memory before generation
        memory_info = self.get_memory_info()
        if memory_info["available_gb"] < 2.0:  # Require at least 2GB free
            gc.collect()
            if self.device == "cuda":
                torch.cuda.empty_cache()
            memory_info = self.get_memory_info()
            if memory_info["available_gb"] < 1.5:  # Still not enough after cleanup
                return None, f"Insufficient memory: {memory_info['available_gb']:.1f}GB available, need at least 1.5GB"
        
        try:
            print(f"Generating img2img for: {prompt}")
            print(f"Settings: {steps} steps, {width}x{height}, strength: {strength}, device: {self.device}")
            print(f"Memory before generation: {memory_info['available_gb']:.1f}GB available")
            
            # Reduce dimensions if memory is tight
            if memory_info["available_gb"] < 4.0:
                width = min(width, 256)
                height = min(height, 256)
                steps = min(steps, 10)
                print(f"Reduced settings due to memory: {steps} steps, {width}x{height}")
            
            # Resize input image to match target dimensions
            from PIL import Image
            if isinstance(init_image, str):
                init_image = Image.open(init_image)
            init_image = init_image.resize((width, height))
            
            generation_kwargs = {
                "prompt": prompt,
                "image": init_image,
                "strength": strength,
                "num_inference_steps": steps,
                "width": width,
                "height": height,
                "generator": torch.Generator(device=self.device).manual_seed(42)
            }
            
            # Generate the image
            with torch.inference_mode():
                result = self.img2img_pipeline(**generation_kwargs)
                
                if hasattr(result, 'images') and result.images:
                    image = result.images[0]
                    
                    # Force cleanup after generation
                    gc.collect()
                    if self.device == "cuda":
                        torch.cuda.empty_cache()
                    
                    return image, None
                else:
                    return None, "No image generated"
                    
        except Exception as e:
            error_msg = str(e)
            print(f"Img2img generation failed: {error_msg}")
            traceback.print_exc()
            
            # Clean up on error
            gc.collect()
            if self.device == "cuda":
                torch.cuda.empty_cache()
                
            # Provide more specific error messages
            if "memory" in error_msg.lower() or "allocation" in error_msg.lower():
                return None, f"Out of memory error. Try reducing image size or inference steps. Available: {self.get_memory_info()['available_gb']:.1f}GB"
            elif "cuda" in error_msg.lower():
                return None, f"CUDA error: {error_msg}"
            else:
                return None, f"Img2img generation error: {error_msg}"

sd_service = StableDiffusionService()

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    memory_info = sd_service.get_memory_info()
    gpu_info = {}
    
    # Add GPU information if available
    if sd_service.device == "cuda" and torch.cuda.is_available():
        gpu_info = {
            "gpu_available": True,
            "gpu_name": torch.cuda.get_device_name(0),
            "gpu_memory_allocated_gb": round(torch.cuda.memory_allocated(0) / (1024**3), 2),
            "gpu_memory_cached_gb": round(torch.cuda.memory_reserved(0) / (1024**3), 2)
        }
    else:
        gpu_info = {"gpu_available": False}
    
    return jsonify({
        "status": "ok",
        "version": VERSION,
        "timestamp": time.time(),
        "service": "ai-art-service",
        "model_loaded": sd_service.model_loaded,
        "device": sd_service.device,
        "onnx_provider": sd_service.provider,
        "memory": memory_info,
        **gpu_info
    })

@app.route('/generate', methods=['POST'])
def generate():
    """Generate image from text prompt"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON data provided"}), 400
        
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({"success": False, "error": "No prompt provided"}), 400
        
        steps = data.get('steps', 10)  # Use fewer steps for faster generation
        width = data.get('width', 512)
        height = data.get('height', 512)
        
        # Validate parameters
        steps = max(1, min(steps, 50))  # Limit steps to reasonable range
        width = max(128, min(width, 1024))  # Limit width
        height = max(128, min(height, 1024))  # Limit height
        
        print(f"Generating image for prompt: '{prompt}' with {steps} steps, {width}x{height}")
        start_time = time.time()
        
        image, error_msg = sd_service.generate_image(prompt, steps, width, height)
        generation_time = time.time() - start_time
        
        if image:
            # Convert PIL image to base64
            import io
            import base64
            
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            image_b64 = base64.b64encode(buffer.getvalue()).decode()
            
            return jsonify({
                "success": True,
                "image": image_b64,
                "prompt": prompt,
                "steps": steps,
                "width": width,
                "height": height,
                "generation_time": round(generation_time, 3),
                "device": sd_service.device,
                "model_type": "StableDiffusionPipeline",
                "memory_after": sd_service.get_memory_info()
            })
        else:
            return jsonify({
                "success": False, 
                "error": error_msg or "Image generation failed",
                "generation_time": round(generation_time, 3),
                "memory_info": sd_service.get_memory_info()
            }), 500
            
    except Exception as e:
        print(f"Generation endpoint error: {e}")
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print(f"Starting AI Art Service v{VERSION}")
    print("Service available at http://localhost:8080")
    app.run(host='localhost', port=8080, debug=False)