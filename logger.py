import logging


def setup_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(),  # Output to the console
            logging.FileHandler('LOG.log')  # Output to a log file
        ]
    )

    logger = logging.getLogger(__name__)
    return logger


def log_parameters(logger, **kwargs):
    logger.info("Received the following parameters:")
    # Find the maximum length of the parameter names
    max_len = max(len(str(key)) for key in kwargs.keys())
    formatted_params = "\n" + "\n".join(
        f"{key.upper(): <{max_len}} : {value}" for key, value in kwargs.items())
    logger.info(formatted_params)
