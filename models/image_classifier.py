"""
Image Classification Model - Demonstrates Inheritance and Method Overriding

OOP Concepts Used:
1. Inheritance: Inherits from AIModelBase
2. Method Overriding: Overrides load_model() and predict()
3. Encapsulation: Uses private attributes
4. Polymorphism: Implements predict() differently than TextToVideoModel

This model uses Hugging Face's Transformers library for image classification
Model Source: google/vit-base-patch16-224 from Hugging Face Hub
"""

# Import base class for inheritance
from models.model_base import AIModelBase
# Hugging Face Transformers for pretrained models
from transformers import pipeline
# PIL for image processing
from PIL import Image


class ImageClassifierModel(AIModelBase):
    """
    Image Classification Model using Vision Transformer (ViT)

    DEMONSTRATES:
    - Inheritance: Extends AIModelBase parent class
    - Method Overriding: Provides custom implementations for load_model() and predict()
    - Polymorphism: predict() accepts images, unlike TextToVideoModel which accepts text
    - Encapsulation: Uses private attributes for configuration

    Implementation:
    - Uses Google's Vision Transformer (ViT) from Hugging Face
    - Classifies images into 1000+ categories (ImageNet classes)
    - Returns top-K most likely categories with confidence scores
    """

    def __init__(self):
        """
        Initialize image classification model

        DEMONSTRATES: Inheritance - calls parent class constructor with super()
        """
        # Call parent constructor to set basic model information
        super().__init__(
            model_name="Vision Transformer (ViT)",
            category="Computer Vision - Image Classification",
            description="Vision Transformer (ViT) is a neural network architecture that applies transformer mechanisms to image classification. It divides images into patches and processes them as sequences, achieving state-of-the-art performance on image recognition tasks."
        )

        # DEMONSTRATES: Encapsulation - private attribute for configuration
        self._top_k = 3  # Number of top predictions to return

    def load_model(self):
        """
        Load Vision Transformer model from Hugging Face

        DEMONSTRATES: Method Overriding - overrides AIModelBase.load_model()
        Each model type has different loading requirements

        Returns:
            Boolean indicating success/failure of model loading
        """
        try:
            print(f"Loading {self._model_name} model...")

            # Load pretrained ViT model using Hugging Face pipeline
            # Pipeline automatically handles preprocessing and postprocessing
            self._model = pipeline(
                "image-classification",              # Task type
                model="google/vit-base-patch16-224"  # Hugging Face model identifier
            )

            # Update model loaded status (from parent class)
            self._loaded = True
            print(f"{self._model_name} loaded successfully!")
            return True

        except Exception as e:
            print(f"Error loading model: {e}")
            self._loaded = False
            return False

    def predict(self, image_input):
        """
        Classify image into categories

        DEMONSTRATES:
        - Method Overriding: Overrides AIModelBase.predict()
        - Polymorphism: Same method name as TextToVideoModel, but different implementation
          * This version accepts IMAGE and returns LABELS
          * TextToVideoModel accepts TEXT and generates VIDEO

        Args:
            image_input: Can be a PIL Image object or file path string

        Returns:
            List of dictionaries with rank, label, and confidence for top predictions

        Raises:
            Exception: If model not loaded
            ValueError: If image input is invalid format
        """
        # Validate model is loaded before use
        if not self._loaded:
            raise Exception("Model not loaded. Call load_model() first.")

        try:
            # Handle different input types (polymorphic input handling)
            if isinstance(image_input, str):
                # If string, treat as file path and load image
                image = Image.open(image_input)
            elif isinstance(image_input, Image.Image):
                # Already a PIL Image object
                image = image_input
            else:
                raise ValueError("Input must be a file path (string) or PIL Image")

            # Perform classification using the loaded model
            # Model returns list of predictions sorted by confidence
            results = self._model(image)

            # Format results for display
            formatted_results = []
            for i, result in enumerate(results[:self._top_k]):  # Get top K results
                formatted_results.append({
                    'rank': i + 1,                              # Ranking (1, 2, 3...)
                    'label': result['label'],                   # Class name
                    'confidence': f"{result['score'] * 100:.2f}%"  # Confidence percentage
                })

            return formatted_results

        except Exception as e:
            raise Exception(f"Prediction failed: {e}")

    # ========================================================================
    # CONFIGURATION SETTER METHODS
    # ========================================================================

    def set_top_k(self, k):
        """
        Set number of top predictions to return

        DEMONSTRATES: Encapsulation - controlled modification of private attributes

        Args:
            k: Number of top predictions (e.g., 3 returns top 3 classes)
        """
        if k > 0:
            self._top_k = k

    def get_model_info(self):
        """
        Get detailed model information including classification-specific parameters

        DEMONSTRATES: Method Overriding - extends parent's get_model_info()
        Calls parent method with super(), then adds additional fields

        Returns:
            Dictionary with comprehensive model information
        """
        # Get base info from parent class
        info = super().get_model_info()

        # Add classification-specific information
        info["Top K Predictions"] = self._top_k
        info["Model Type"] = "Vision Transformer (Patch-based)"
        info["Input Size"] = "224x224 pixels"

        return info
