"""modul gaya fetty."""
import importlib
from . import main_css
importlib.reload(main_css)
from .main_css import apply_custom_css

__all__ = ["apply_custom_css"]
