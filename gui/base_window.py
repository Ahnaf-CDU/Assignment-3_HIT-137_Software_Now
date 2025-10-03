"""
Base GUI Window - Demonstrates Encapsulation

OOP Concepts Used:
1. Encapsulation: Private attributes and methods
2. Property decorators: Controlled access to attributes
3. Base class for GUI components
"""

import tkinter as tk
from tkinter import ttk


class GUIBase:
    """
    Base class for GUI components
    Demonstrates encapsulation with private attributes
    """

    def __init__(self, parent):
        self._parent = parent
        self._frame = None
        self._widgets = {}

    @property
    def frame(self):
        """Getter for frame"""
        return self._frame

    @property
    def parent(self):
        """Getter for parent"""
        return self._parent

    def _create_label(self, text, **kwargs):
        """
        Protected method to create labels
        Demonstrates encapsulation
        """
        return tk.Label(self._frame, text=text, **kwargs)

    def _create_button(self, text, command, **kwargs):
        """
        Protected method to create buttons
        Demonstrates encapsulation
        """
        return tk.Button(self._frame, text=text, command=command, **kwargs)

    def _create_entry(self, **kwargs):
        """
        Protected method to create entry widgets
        Demonstrates encapsulation
        """
        return tk.Entry(self._frame, **kwargs)

    def _create_text(self, **kwargs):
        """
        Protected method to create text widgets
        Demonstrates encapsulation
        """
        return tk.Text(self._frame, **kwargs)

    def create_frame(self):
        """
        Create the main frame - to be called by subclasses
        """
        raise NotImplementedError("Subclasses must implement create_frame()")


class LabelFrameBase(GUIBase):
    """
    Base class for LabelFrame-based GUI components
    Demonstrates inheritance from GUIBase
    """

    def __init__(self, parent, title):
        super().__init__(parent)
        self._title = title

    def create_frame(self):
        """Override to create a LabelFrame"""
        self._frame = tk.LabelFrame(self._parent, text=self._title, padx=10, pady=10)
        return self._frame
