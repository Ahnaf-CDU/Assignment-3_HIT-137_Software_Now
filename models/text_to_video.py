"""
Text-to-Video Model - Demonstrates Inheritance and Method Overriding

OOP Concepts Used:
1. Inheritance: Inherits from AIModelBase
2. Method Overriding: Overrides load_model() and predict()
3. Encapsulation: Uses private attributes
4. Polymorphism: Implements predict() differently than ImageClassifierModel

This model uses Hugging Face's Diffusers library to generate videos from text prompts
Model Source: segmind/tiny-sd from Hugging Face Hub
"""

# Import base class for inheritance
from models.model_base import AIModelBase
# PyTorch for deep learning operations
import torch
# Hugging Face Diffusers for Stable Diffusion models
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
# Image processing
from PIL import Image
import numpy as np
# Video export
import imageio
import os


class TextToVideoModel(AIModelBase):
    """
    Text-to-Video Model using Text-to-Image + Animation

    DEMONSTRATES:
    - Inheritance: Extends AIModelBase parent class
    - Method Overriding: Provides custom implementations for load_model() and predict()
    - Polymorphism: predict() accepts text, unlike ImageClassifierModel which accepts images
    - Encapsulation: Uses private attributes for configuration

    Implementation:
    - Uses Stable Diffusion (segmind/tiny-sd) from Hugging Face
    - Generates base image from text, then creates animated frames
    - Exports as MP4 video file
    """

    def __init__(self):
        """
        Initialize text-to-video model

        DEMONSTRATES: Inheritance - calls parent class constructor with super()
        """
        # Call parent constructor to set basic model information
        super().__init__(
            model_name="Text-to-Video (Lightweight)",
            category="Video Generation",
            description="Generates 2-3 second video clips from text. Uses lightweight text-to-image generation with smooth animation effects. Optimized for CPU."
        )

        # DEMONSTRATES: Encapsulation - private attributes for model configuration
        self._num_inference_steps = 20  # Number of diffusion steps (quality vs speed)
        self._num_frames = 24          # 24 frames for 3 seconds at 8 fps
        self._fps = 8                  # Frames per second for output video

    def load_model(self):
        """
        Load Stable Diffusion model from Hugging Face

        DEMONSTRATES: Method Overriding - overrides AIModelBase.load_model()
        Each model type has different loading requirements

        Returns:
            Boolean indicating success/failure of model loading
        """
        try:
            print(f"Loading {self._model_name} model...")
            print("This may take a few minutes on first run (downloading ~1.5GB)...")

            # Detect available hardware (CUDA GPU or CPU)
            device = "cuda" if torch.cuda.is_available() else "cpu"

            # Load lightweight Stable Diffusion model from Hugging Face
            # Model: segmind/tiny-sd (only 500MB, optimized for speed)
            self._model = DiffusionPipeline.from_pretrained(
                "segmind/tiny-sd",  # Hugging Face model identifier
                torch_dtype=torch.float32  # Use float32 for CPU compatibility
            )

            # Move model to appropriate device (GPU or CPU)
            self._model = self._model.to(device)

            # Inform user about execution environment
            if device == "cpu":
                print("Using CPU - lightweight model optimized for 16GB RAM")
            else:
                print("Using GPU - will be faster")

            # Update model loaded status (from parent class)
            self._loaded = True
            print(f"{self._model_name} loaded successfully on {device}!")
            return True

        except Exception as e:
            print(f"Error loading model: {e}")
            self._loaded = False
            return False

    def predict(self, text_prompt):
        """
        Generate video from text prompt

        DEMONSTRATES:
        - Method Overriding: Overrides AIModelBase.predict()
        - Polymorphism: Same method name as ImageClassifierModel, but different implementation
          * This version accepts TEXT and generates VIDEO
          * ImageClassifierModel accepts IMAGE and returns LABELS

        Args:
            text_prompt: String describing the video to generate

        Returns:
            Dictionary containing video file path, metadata, and preview image

        Raises:
            Exception: If model not loaded
            ValueError: If text prompt is invalid
        """
        # Validate model is loaded before use
        if not self._loaded:
            raise Exception("Model not loaded. Call load_model() first.")

        # Validate input is valid text string
        if not isinstance(text_prompt, str) or not text_prompt.strip():
            raise ValueError("Input must be a non-empty text prompt")

        try:
            print(f"Generating 3-second video from text prompt...")
            print(f"Prompt: {text_prompt}")
            print(f"Step 1/2: Generating base image...")

            # Step 1: Generate a single high-quality image from text using Stable Diffusion
            base_image = self._model(
                prompt=text_prompt,
                num_inference_steps=self._num_inference_steps,  # Quality vs speed tradeoff
                height=512,
                width=512,
                guidance_scale=7.5  # How closely to follow prompt
            ).images[0]

            print(f"Step 2/2: Creating animation from image...")
            import sys
            sys.stdout.flush()

            # Step 2: Create animated frames from the base image
            frames = self._create_animation_frames(base_image)

            # Define output file paths
            output_file = "generated_video.mp4"
            preview_file = "generated_video_preview.png"

            print(f"Exporting video to {output_file}...")
            sys.stdout.flush()

            # Convert PIL images to numpy arrays for imageio compatibility
            frame_arrays = [np.array(frame) for frame in frames]

            # Step 3: Export frames as MP4 video using imageio + ffmpeg
            imageio.mimsave(
                output_file,
                frame_arrays,
                fps=self._fps,                      # Frames per second
                codec='libx264',                    # H.264 video codec
                quality=8,                          # Quality setting (1-10)
                pixelformat='yuv420p',              # Color format for compatibility
                output_params=['-loglevel', 'error']  # Suppress verbose ffmpeg output
            )

            print(f"Video export complete!")
            sys.stdout.flush()

            # Save first frame as preview image for GUI display
            frames[0].save(preview_file)

            # Calculate video duration
            duration = len(frames) / self._fps

            # Return comprehensive metadata dictionary
            result_info = {
                "status": "success",
                "message": f"Video generated successfully!",
                "file": output_file,                      # Output video file path
                "preview": preview_file,                  # Preview image path
                "frames": len(frames),                    # Total frame count
                "fps": self._fps,                         # Frames per second
                "duration": f"{duration:.1f} seconds",   # Video length
                "format": "MP4 video file",               # File format
                "resolution": "512x512"                   # Video resolution
            }

            return result_info

        except Exception as e:
            raise Exception(f"Video generation failed: {e}")

    def _create_animation_frames(self, base_image):
        """
        Create smooth animation frames from a single image

        DEMONSTRATES: Encapsulation - private helper method (prefix with _)
        This method is internal implementation detail not exposed to users

        Applies zoom and brightness effects to create animated video frames

        Args:
            base_image: PIL Image to animate

        Returns:
            List of PIL Images representing animation frames
        """
        from PIL import ImageEnhance, ImageFilter

        frames = []
        width, height = base_image.size

        # Create smooth zoom + pan animation effect
        for i in range(self._num_frames):
            # Calculate progress through animation (0.0 to 1.0)
            progress = i / (self._num_frames - 1)

            # Apply smooth easing function for natural motion
            # This creates smoother acceleration/deceleration
            ease = progress * progress * (3.0 - 2.0 * progress)

            # Gradually zoom from 1.0x to 1.2x scale
            scale = 1.0 + (ease * 0.2)
            new_width = int(width * scale)
            new_height = int(height * scale)

            # Resize image with high-quality LANCZOS resampling
            zoomed = base_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Calculate pan offset to keep image centered
            pan_x = int((new_width - width) * 0.5)
            pan_y = int((new_height - height) * 0.5)

            # Crop back to original size (creates zoom effect)
            frame = zoomed.crop((pan_x, pan_y, pan_x + width, pan_y + height))

            # Add subtle brightness variation for visual interest
            # Uses sine wave for smooth variation
            brightness_factor = 1.0 + (np.sin(progress * np.pi) * 0.05)
            enhancer = ImageEnhance.Brightness(frame)
            frame = enhancer.enhance(brightness_factor)

            # Add frame to animation sequence
            frames.append(frame)

        return frames

    # ========================================================================
    # CONFIGURATION SETTER METHODS
    # ========================================================================

    def set_inference_steps(self, steps):
        """
        Set number of inference steps for image generation

        DEMONSTRATES: Encapsulation - controlled modification of private attributes

        Args:
            steps: Number of diffusion steps (higher = better quality, slower)
        """
        if steps > 0:
            self._num_inference_steps = steps

    def set_num_frames(self, frames):
        """
        Set number of frames to generate for video

        DEMONSTRATES: Encapsulation - controlled modification of private attributes

        Args:
            frames: Total number of frames in output video
        """
        if frames > 0:
            self._num_frames = frames

    def set_fps(self, fps):
        """
        Set frames per second for output video

        DEMONSTRATES: Encapsulation - controlled modification of private attributes

        Args:
            fps: Frames per second (affects video duration)
        """
        if fps > 0:
            self._fps = fps

    def get_model_info(self):
        """
        Get detailed model information including video-specific parameters

        DEMONSTRATES: Method Overriding - extends parent's get_model_info()
        Calls parent method with super(), then adds additional fields

        Returns:
            Dictionary with comprehensive model information
        """
        # Get base info from parent class
        info = super().get_model_info()

        # Add video-specific information
        info["Model Type"] = "Text-to-Image + Animation"
        info["Inference Steps"] = self._num_inference_steps
        info["Number of Frames"] = self._num_frames
        info["FPS"] = self._fps
        info["Duration"] = f"{self._num_frames / self._fps:.1f}s"
        info["Output Format"] = "MP4 Video (512x512)"
        info["Memory Usage"] = "Low (CPU optimized)"

        return info
