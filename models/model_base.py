"""
Base Model Class - Demonstrates Polymorphism and Encapsulation

OOP Concepts Used:
1. Encapsulation: Private attributes (_model_name, _category, _loaded)
2. Polymorphism: Base class with predict() method to be overridden
3. Abstraction: Abstract interface for all AI models
4. Property Decorators: Controlled access to private attributes
"""

class AIModelBase:
    """
    Base class for all AI models

    DEMONSTRATES:
    - Encapsulation: Private attributes with property getters
    - Polymorphism: Abstract methods to be overridden by subclasses
    - Abstraction: Defines common interface for all AI model types

    This is the parent class for TextToVideoModel and ImageClassifierModel
    """

    def __init__(self, model_name, category, description):
        """
        Initialize the base AI model

        Args:
            model_name: Display name of the model
            category: Category/type of AI model
            description: Detailed description of model capabilities
        """
        # DEMONSTRATES: Encapsulation - Private attributes (prefix with _)
        # These attributes are not directly accessible from outside the class
        self._model_name = model_name      # Model's display name
        self._category = category          # Model category (e.g., "Video Generation")
        self._description = description    # Detailed model description
        self._loaded = False              # Track if model has been loaded
        self._model = None                # The actual ML model instance

    # ========================================================================
    # PROPERTY DECORATORS - Encapsulation with controlled access
    # ========================================================================

    @property
    def model_name(self):
        """
        Getter for model name

        DEMONSTRATES: Encapsulation - Read-only access to private attribute
        Users can read but not modify the model name
        """
        return self._model_name

    @property
    def category(self):
        """
        Getter for model category

        DEMONSTRATES: Encapsulation - Read-only access to private attribute
        """
        return self._category

    @property
    def description(self):
        """
        Getter for model description

        DEMONSTRATES: Encapsulation - Read-only access to private attribute
        """
        return self._description

    @property
    def is_loaded(self):
        """
        Getter for model loaded status

        DEMONSTRATES: Encapsulation - Read-only access to private attribute
        Returns: Boolean indicating if model is loaded and ready
        """
        return self._loaded

    # ========================================================================
    # ABSTRACT METHODS - To be overridden by subclasses
    # ========================================================================

    def load_model(self):
        """
        Load the AI model - MUST be implemented by subclasses

        DEMONSTRATES: Polymorphism - Each subclass provides its own implementation
        - TextToVideoModel loads Stable Diffusion model
        - ImageClassifierModel loads Vision Transformer model

        Raises:
            NotImplementedError: If subclass doesn't override this method
        """
        raise NotImplementedError("Subclasses must implement load_model()")

    def predict(self, input_data):
        """
        Make prediction - MUST be overridden by subclasses

        DEMONSTRATES:
        - Polymorphism: Same method name, different behavior for each model
        - Method Overriding: Subclasses override to provide specific functionality

        Args:
            input_data: Input can be text string (for video) or image path (for classification)

        Raises:
            NotImplementedError: If subclass doesn't override this method
        """
        raise NotImplementedError("Subclasses must implement predict()")

    # ========================================================================
    # COMMON METHODS - Can be inherited or overridden
    # ========================================================================

    def get_model_info(self):
        """
        Get model information as a dictionary

        DEMONSTRATES: Method Overriding - Subclasses can extend this method
        Base implementation provides common info, subclasses add specific details

        Returns:
            Dictionary containing model information
        """
        return {
            "Model Name": self._model_name,
            "Category": self._category,
            "Description": self._description,
            "Status": "Loaded" if self._loaded else "Not Loaded"
        }

    # ========================================================================
    # SPECIAL METHODS - Python magic methods
    # ========================================================================

    def __str__(self):
        """
        String representation for print() and str()

        DEMONSTRATES: Method Overriding of built-in Python methods
        """
        return f"{self._model_name} ({self._category})"

    def __repr__(self):
        """
        Developer-friendly representation for debugging

        DEMONSTRATES: Method Overriding of built-in Python methods
        """
        return f"AIModelBase(model_name='{self._model_name}', category='{self._category}')"
