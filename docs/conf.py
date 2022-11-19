# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath("../poly2pascal"))

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'poly2pascal'
copyright = '2022, Ruan Pretorius'
author = 'Ruan Pretorius'
release = '0.0.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']

# use the readthedocs theme
html_theme = 'sphinx_rtd_theme'

# some parameters to customise the looks of your docs
html_theme_options = {
    'logo_only': False,
    'display_version': False,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'style_nav_header_background': '#1a4a73',
    # Toc options
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'titles_only': False
}

html_context = {
    "display_github": True, # Integrate GitHub
    "github_user": "ruankie", # Username
    "github_repo": "poly2pascal", # Repo name
    "github_version": "main", # Version
    "conf_py_path": "/docs/", # Path in the checkout to the docs root
}

html_favicon = '../images/p2p.ico'

# a logo (delete line if you don't want to display one)
# html_logo = '../images/p2p_100_100.png'
