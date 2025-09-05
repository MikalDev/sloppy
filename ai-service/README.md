# AI Art Game Service

This service provides AI-powered image generation capabilities for the AI Art Game using Stable Diffusion with GPU acceleration.

## Features

- **GPU Accelerated**: Uses CUDA for fast image generation on RTX 4070
- **Stable Diffusion v1.5**: High-quality text-to-image generation
- **Web Interface**: Simple web UI for testing and generation
- **Flask API**: RESTful endpoints for integration

## Quick Start

### First Time Setup

1. Run the setup script to create environment and install dependencies:
   ```cmd
   setup_env.bat
   ```

2. Start the server:
   ```cmd
   start_server.bat
   ```

3. Open your browser to `http://localhost:8081`

### Manual Setup (Alternative)

```cmd
# Create virtual environment
python -m venv venv

# Activate environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install CUDA PyTorch (for GPU acceleration)
pip uninstall torch torchvision -y
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# Start server
python test_web.py
```

## API Endpoints

- `GET /` - Web interface
- `POST /generate` - Generate image from text prompt
- `GET /health` - Service health check

## System Requirements

- **GPU**: NVIDIA RTX series with CUDA support
- **Python**: 3.10+
- **CUDA**: 12.1 compatible drivers
- **Memory**: 12GB+ RAM recommended

## Performance

With RTX 4070 GPU acceleration:
- **Loading**: ~2-3 seconds (first time)
- **Generation**: ~1-2 seconds (512x512, 12 steps)
- **Memory**: ~4GB VRAM usage

## Troubleshooting

### GPU Not Detected
If you see "device: cpu" instead of "device: cuda":
1. Ensure NVIDIA drivers are installed
2. Verify CUDA compatibility: `python -c "import torch; print(torch.cuda.is_available())"`
3. Reinstall CUDA PyTorch: `pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121`

## Legacy Documentation

### Version Control & Testing

Always increment version number in `app.py` after each change.

Current version: **1.1.0**

### Process Cleanup

#### Method 1: Kill all Python processes (DESTRUCTIVE)
```bash
wmic process where "name='python.exe'" delete
```

#### Method 2: Kill by port (TARGETED) 
```bash
# Find processes using port 8080
netstat -ano | findstr :8080

# Kill specific PID
taskkill /PID [PID_NUMBER] /F
```

#### Method 3: Use cleanup script
```bash
cd ai-service
cleanup.bat
```