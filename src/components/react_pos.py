# -*- coding: utf-8 -*-
"""
components/react_pos.py — Streamlit custom component wrapper for the React POS UI.
"""
import os
import streamlit.components.v1 as components

# Determine the absolute path to the frontend build directory
_frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")

# If testing the React component locally (e.g., npm run dev on port 5173), set _RELEASE = False
_RELEASE = True

if not _RELEASE:
    # Use the local React dev server
    _component_func = components.declare_component(
        "react_pos",
        url="http://localhost:5173",
    )
else:
    # Use the compiled React static files
    _component_func = components.declare_component("react_pos", path=_frontend_dir)

def render_react_pos(inventory, customers, key=None):
    """
    Renders the custom React POS component.
    
    Args:
        inventory (list): List of dicts representing available inventory.
        customers (list): List of dicts representing customers.
        key (str): Optional key to prevent state loss.
        
    Returns:
        dict: The checkout payload from the React component when "Confirm Sale" is clicked.
              e.g., {"cart": [...], "customer": {...}, "finalPrice": ...}
    """
    component_value = _component_func(
        inventory=inventory,
        customers=customers,
        key=key,
        default=None
    )
    return component_value
