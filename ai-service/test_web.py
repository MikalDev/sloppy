from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import os

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
                <label for="quality">Quality Preset:</label>
                <select id="quality" name="quality" onchange="updateQualitySettings()">
                    <option value="fast">Fast - 256x256, 5 steps (~0.3s)</option>
                    <option value="balanced" selected>Balanced - 384x384, 8 steps (~0.7s)</option>
                    <option value="quality">Quality - 512x512, 12 steps (~1.2s)</option>
                    <option value="max">Max Quality - 512x512, 20 steps (~2.0s)</option>
                    <option value="custom">Custom Settings</option>
                </select>
            </div>
            
            <div id="customSettings" style="display: none;">
                <div class="form-group">
                    <label for="steps">Steps (5-50):</label>
                    <select id="steps" name="steps">
                        <option value="5">5 - Ultra Fast</option>
                        <option value="8" selected>8 - Balanced</option>
                        <option value="12">12 - Good Quality</option>
                        <option value="15">15 - High Quality</option>
                        <option value="20">20 - Very High</option>
                        <option value="30">30 - Maximum</option>
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
            </div>
            
            <button type="submit" id="generateBtn">🚀 Generate Image</button>
        </form>
        
        <div id="status"></div>
        <div id="result" class="result"></div>
    </div>

    <script>
        // Quality preset configurations
        const qualityPresets = {
            fast: { steps: 5, size: 256 },
            balanced: { steps: 8, size: 384 },
            quality: { steps: 12, size: 512 },
            max: { steps: 20, size: 512 }
        };
        
        function updateQualitySettings() {
            const quality = document.getElementById('quality').value;
            const customSettings = document.getElementById('customSettings');
            
            if (quality === 'custom') {
                customSettings.style.display = 'block';
            } else {
                customSettings.style.display = 'none';
            }
        }
        
        function getGenerationSettings() {
            const quality = document.getElementById('quality').value;
            
            if (quality === 'custom') {
                return {
                    steps: parseInt(document.getElementById('steps').value),
                    size: parseInt(document.getElementById('size').value)
                };
            } else {
                return qualityPresets[quality];
            }
        }
        
        document.getElementById('artForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const prompt = document.getElementById('prompt').value;
            const settings = getGenerationSettings();
            const steps = settings.steps;
            const size = settings.size;
            
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

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template_string(HTML_TEMPLATE)

# Import the AI service from app.py
import sys
import os
sys.path.append(os.path.dirname(__file__))
from app import StableDiffusionService
import time
import traceback
import io
import base64

# Create AI service instance
sd_service = StableDiffusionService()

@app.route('/test')
def test():
    """Simple test endpoint"""
    return jsonify({"status": "Server is running!", "message": "Web interface test"})

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
    print("AI Art Web Interface with Generation")
    print("Access at: http://localhost:8081")
    app.run(host='localhost', port=8081, debug=False)