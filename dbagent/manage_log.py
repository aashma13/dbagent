import logging
def get_logger(module_name):
    
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s - %(message)s')
    console_handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(console_handler)
    return logger
    
