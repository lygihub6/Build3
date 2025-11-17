"""
Service package initializer.

Having an ``__init__.py`` file makes this directory a proper
Python package so that modules like ``services.ai`` can be imported
reliably throughout the application. Without this file, some Python
environments may treat ``services`` as a namespace package and fail
to locate submodules.
"""
