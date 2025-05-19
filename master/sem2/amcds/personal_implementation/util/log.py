import logging
import os
import sys
from logging.handlers import RotatingFileHandler

# Global logger instance
logger = None

def setup_logger(level=logging.INFO, log_file=None):
    """
    Setup logger with the specified level and optionally a log file.
    Returns the configured logger.
    """
    global logger
    
    if logger is not None:
        return logger
        
    # Create logger
    logger = logging.getLogger('amcds')
    logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s %(message)s', 
                                 '%H:%M:%S')
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if specified
    if log_file:
        file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def set_level(level_name):
    """Set the logging level based on the name"""
    global logger
    
    if not logger:
        setup_logger()
    
    level_map = {
        'trace': logging.DEBUG,
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARNING,
        'error': logging.ERROR,
        'fatal': logging.CRITICAL
    }
    
    level = level_map.get(level_name.lower(), logging.INFO)
    logger.setLevel(level)
    
    # Update all handlers to the new level
    for handler in logger.handlers:
        handler.setLevel(level)

def debug(message, *args):
    """Log a debug message"""
    global logger
    if not logger:
        setup_logger()
    logger.debug(message, *args)

def info(message, *args):
    """Log an info message"""
    global logger
    if not logger:
        setup_logger()
    logger.info(message, *args)

def warn(message, *args):
    """Log a warning message"""
    global logger
    if not logger:
        setup_logger()
    logger.warning(message, *args)

def error(message, *args):
    """Log an error message"""
    global logger
    if not logger:
        setup_logger()
    logger.error(message, *args)

def fatal(message, *args):
    """Log a critical message"""
    global logger
    if not logger:
        setup_logger()
    logger.critical(message, *args)
