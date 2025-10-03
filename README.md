# HIT137 Assignment 3 - AI Studio GUI Application

## Project Overview
This project is a modern Tkinter-based GUI application that integrates two Hugging Face AI models and demonstrates all required Object-Oriented Programming (OOP) concepts. The application features a professional dark-themed interface with custom UI components.

## AI Models Used

### 1. Text-to-Video Generation
- **Model**: Stable Diffusion Tiny (segmind/tiny-sd)
- **Category**: Video Generation
- **Function**: Generates 2-3 second video clips from text descriptions
- **Model Size**: ~500MB (lightweight, CPU-optimized)
- **Source**: Hugging Face Hub
- **Implementation**: Generates base image using Stable Diffusion, then creates smooth animation with zoom and brightness effects
- **Output**: MP4 video file (512x512, 24 frames @ 8 fps)

### 2. Image Classification
- **Model**: Vision Transformer (google/vit-base-patch16-224)
- **Category**: Computer Vision - Image Recognition
- **Function**: Classifies images into 1000+ categories with confidence scores
- **Model Size**: ~350MB
- **Source**: Hugging Face Hub
- **Implementation**: Uses transformer architecture to classify images
- **Output**: Top 3 predictions with confidence percentages

## OOP Concepts Demonstrated

### 1. Multiple Inheritance ✓
- **Location**: `main.py:176`
- **Implementation**: `class AIGUIApplication(tk.Tk, ModelManagerMixin)`
- **Explanation**: The main application class inherits from both `tk.Tk` (for GUI window functionality) and `ModelManagerMixin` (for AI model management), combining features from multiple parent classes.

### 2. Multiple Decorators ✓
- **Location**: `main.py:161-162`, `main.py:489-490`, `utils/decorators.py`
- **Implementation**: `@timer` and `@log_execution` decorators stacked on methods like `load_model_async()` and `_load_selected_model()`
- **Explanation**: Multiple decorators are applied to functions to add logging, timing, and error handling capabilities without modifying the original function code.

### 3. Encapsulation ✓
- **Location**: Throughout `models/model_base.py`, `main.py`
- **Implementation**:
  - Private attributes: `_model_name`, `_window_title`, `_selected_image_path`, `_loaded`, `_num_frames`
  - Private methods: `_setup_window()`, `_create_widgets()`, `_display_image()`, `_create_animation_frames()`
  - Property decorators: `@property` for controlled read-only access
- **Explanation**: Internal data and implementation details are hidden from external access, with controlled access through public methods and properties.

### 4. Polymorphism ✓
- **Location**: `models/model_base.py:99`, `models/text_to_video.py:106`, `models/image_classifier.py:84`
- **Implementation**: Base class `AIModelBase` defines `predict()` method, which is overridden differently in `TextToVideoModel` and `ImageClassifierModel`
- **Explanation**: The same method name (`predict()`) behaves differently depending on the object type:
  - `TextToVideoModel.predict()` accepts TEXT and generates VIDEO
  - `ImageClassifierModel.predict()` accepts IMAGE and returns CLASSIFICATION LABELS

### 5. Method Overriding ✓
- **Location**: `models/text_to_video.py:63`, `models/image_classifier.py:54`
- **Implementation**: `load_model()`, `predict()`, and `get_model_info()` methods are overridden in subclasses
- **Explanation**: Subclasses provide their own specialized implementations of methods defined in the parent class:
  - `TextToVideoModel` loads Stable Diffusion model
  - `ImageClassifierModel` loads Vision Transformer model

## Project Structure
```
Assignment-3 Final/
│
├── main.py                          # Main application entry point (655 lines)
│
├── models/                          # AI model implementations
│   ├── __init__.py
│   ├── model_base.py               # Base model class (Polymorphism, Encapsulation)
│   ├── text_to_video.py            # Text-to-video model (Stable Diffusion)
│   └── image_classifier.py         # Image classification model (ViT)
│
├── gui/                            # GUI components
│   ├── __init__.py
│   └── base_window.py              # Base GUI classes (Encapsulation)
│
├── utils/                          # Utility functions
│   ├── __init__.py
│   └── decorators.py               # Custom decorators (Multiple Decorators)
│
└── README.md                       # This file
```

## Installation

### System Requirements
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB for models
- **Internet**: Required for first-time model download
- **OS**: Windows, macOS, or Linux

### Required Dependencies
```bash
# Core dependencies
pip install transformers torch pillow diffusers imageio imageio-ffmpeg
```

### Individual Package Purposes
- `transformers` - Hugging Face model loading (ViT)
- `torch` - PyTorch deep learning framework
- `pillow` - Image processing (PIL)
- `diffusers` - Stable Diffusion model loading
- `imageio` - Video file export
- `imageio-ffmpeg` - Video codec support

### Install All Dependencies at Once
```bash
pip install transformers torch pillow diffusers imageio imageio-ffmpeg
```

## Usage

### Running the Application
```bash
python main.py
```

### Using the GUI

#### For Text-to-Video Generation (Model 1):
1. **Select Model**: Choose "Text-to-Video" from the dropdown menu
2. **Load Model**: Click "Load Model" button
   - First time: Downloads ~500MB (1-5 minutes depending on internet speed)
   - Subsequent runs: Loads from cache (much faster)
3. **Enter Prompt**: Type a description in the text input area
   - Example: "A beautiful sunset over the ocean with waves"
4. **Generate**: Click "Run Model 1" button
5. **Wait**: Video generation takes 30-120 seconds
6. **View**: Generated video preview appears in output section
7. **Files**: Video saved as `generated_video.mp4` and preview as `generated_video_preview.png`

#### For Image Classification (Model 2):
1. **Select Model**: Choose "Image Classification" from the dropdown
2. **Load Model**: Click "Load Model" button
3. **Browse Image**: Click "Browse Image" button
4. **Select File**: Choose an image file (.jpg, .jpeg, .png, .bmp)
5. **Classify**: Click "Run Model 2" button
6. **View Results**: Top 3 predictions appear with confidence scores
   - Example output:
     ```
     1. golden retriever: 94.23%
     2. Labrador retriever: 3.45%
     3. cocker spaniel: 1.12%
     ```

### Clearing Outputs
- Click "Clear" button to reset all inputs and outputs

## Features

### User Interface
- **Modern Dark Theme**: Professional dark color scheme matching modern design standards
- **Custom UI Components**:
  - Rounded buttons with hover effects
  - Card-based layout for organized sections
  - Custom-styled widgets
- **Responsive Layout**: Grid-based layout adapts to window size
- **Progress Indicators**: Progress bar shows operation status
- **Real-time Updates**: Asynchronous operations keep UI responsive

### GUI Sections
1. **Header**: Title, subtitle, model selection dropdown, and load button
2. **User Input Panel** (Left):
   - Text prompt input area
   - Image file browser
   - Model execution buttons
3. **Model Output Panel** (Right):
   - Image/video preview display
   - Text output console
   - Progress bar with status
4. **Information Panels** (Bottom):
   - Model Information: Shows current model details
   - OOP Concepts: Lists all demonstrated concepts with line numbers

### Technical Features
- **Asynchronous Processing**: Threading prevents GUI freezing during model operations
- **Error Handling**: Comprehensive error messages and validation
- **Logging System**: Decorator-based logging for debugging
- **Memory Optimization**: CPU-optimized models for broad compatibility
- **File Management**: Automatic file saving and preview generation
- **Cross-platform**: Works on Windows, macOS, and Linux

## OOP Concepts Location Reference

| Concept | File | Line/Class | Description |
|---------|------|------------|-------------|
| **Multiple Inheritance** | main.py | Line 176 | `AIGUIApplication(tk.Tk, ModelManagerMixin)` |
| **Multiple Decorators** | main.py | Lines 161-162, 489-490 | `@timer` + `@log_execution` |
| **Encapsulation** | model_base.py | Lines 32-38 | Private attributes with `_` prefix |
| **Encapsulation** | main.py | Throughout | Private attributes and methods with `_` prefix |
| **Polymorphism** | model_base.py | Line 99 | `predict()` method - different behavior per model |
| **Method Overriding** | text_to_video.py | Line 63 | `load_model()` override |
| **Method Overriding** | image_classifier.py | Line 54 | `load_model()` override |

## Code Documentation

All Python files are comprehensively commented with:
- ✓ **OOP Concepts**: Each concept is marked with "DEMONSTRATES:"
- ✓ **Method Purposes**: Detailed docstrings for all methods
- ✓ **Parameters**: Args, Returns, and Raises documented
- ✓ **Implementation Details**: Inline comments explain how code works
- ✓ **Section Headers**: Code organized into logical sections

## Important Notes

### First-Time Setup
- **Internet Required**: Models download from Hugging Face Hub on first run
- **Download Sizes**:
  - Text-to-Video model: ~500MB
  - Image Classification model: ~350MB
  - Total: ~850MB
- **Download Time**: 1-5 minutes (depends on internet speed)
- **Cache Location**: Models cached in `~/.cache/huggingface/`
- **Subsequent Runs**: Models load instantly from cache

### Performance Expectations

#### Text-to-Video Generation:
- **CPU**: 30-120 seconds per video
- **GPU** (if available): 10-30 seconds per video
- **Output**: MP4 video (512x512, 24 frames, 3 seconds)

#### Image Classification:
- **CPU/GPU**: 1-3 seconds per image
- **Output**: Top 3 predictions with confidence scores

### Hardware Recommendations
- **Minimum**: 4GB RAM, CPU only
- **Recommended**: 8GB+ RAM, NVIDIA GPU (optional)
- **GPU Support**: CUDA-enabled GPU accelerates processing 3-5x

### Troubleshooting

#### Model Loading Issues:
- **Problem**: Model fails to download
- **Solution**: Check internet connection, try again
- **Alternative**: Download models manually to cache folder

#### Memory Errors:
- **Problem**: Out of memory during generation
- **Solution**:
  - Close other applications
  - Restart application
  - Use smaller image sizes (modify code if needed)

#### FFmpeg Errors (Video Export):
- **Problem**: Video export fails
- **Solution**: Ensure `imageio-ffmpeg` is installed
  ```bash
  pip install imageio-ffmpeg
  ```

#### Slow Performance:
- **Problem**: Video generation is very slow
- **Solution**:
  - This is normal on CPU (30-120 seconds)
  - Use GPU for faster processing
  - Reduce number of frames in `text_to_video.py` (line 60)

## Example Prompts for Text-to-Video

### Nature & Landscapes:
- "A beautiful sunset over the ocean with waves"
- "Mountain landscape with snow and pine trees"
- "Tropical beach with palm trees and clear water"
- "Northern lights dancing over a frozen lake"

### Urban & Architecture:
- "Futuristic cityscape at night with neon lights"
- "Ancient temple in a misty forest"
- "Victorian street with gas lamps"
- "Modern skyscraper reflecting sunset"

### Fantasy & Sci-Fi:
- "Dragon flying over a medieval castle"
- "Spaceship approaching an alien planet"
- "Magical forest with glowing mushrooms"
- "Cyberpunk street with holographic signs"

### Animals & Creatures:
- "Cute cat wearing a space helmet"
- "Majestic eagle soaring through clouds"
- "Colorful tropical fish in coral reef"
- "Wolf howling at full moon"

## Model Information

### Text-to-Video Model Details:
- **Base Model**: Stable Diffusion (segmind/tiny-sd)
- **Type**: Diffusion model for text-to-image
- **Animation**: Custom zoom and brightness effects
- **Parameters**:
  - Inference steps: 20
  - Number of frames: 24
  - FPS: 8
  - Duration: 3 seconds
  - Resolution: 512x512

### Image Classification Model Details:
- **Base Model**: Vision Transformer (google/vit-base-patch16-224)
- **Architecture**: Transformer-based image classification
- **Training Data**: ImageNet (1000 classes)
- **Input Size**: 224x224 pixels (auto-resized)
- **Output**: Top K predictions (default K=3)

## Development Notes

### Code Quality:
- **Total Lines**: ~1200+ lines of Python code
- **Comments**: Comprehensive documentation throughout
- **Structure**: Modular, object-oriented design
- **Standards**: Follows PEP 8 style guidelines

### Extensibility:
The application is designed to be easily extended:
- Add new models by creating new classes inheriting from `AIModelBase`
- Add new decorators in `utils/decorators.py`
- Customize UI in `main.py` GUI creation methods
- Modify animation effects in `text_to_video.py`

## License
Educational project for HIT137 Assignment 3

## Authors
HIT137 Students - Assignment 3 Final Submission

---

**Note**: This application demonstrates advanced OOP concepts and AI integration for educational purposes. All models are sourced from Hugging Face Hub and are used under their respective licenses.
