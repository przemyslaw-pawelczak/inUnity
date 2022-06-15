import logging

class ParsingException(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
        logging.critical(message)

class StopException(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
        logging.critical(message)

class LLVMSyntaxErrorException(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
        logging.critical(message)

class NotImplementedException(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
        logging.critical(message)

class RegisterNotFoundException(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
        logging.critical(message)

class RegisterFileException(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
        logging.critical(message)

class MemoryException(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
        logging.critical(message)

class ConfigurationException(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
        logging.critical(message)

class InitializationException(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
        logging.critical(message)

class RuntimeException(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
        logging.critical(message)
        
class RegAllocException(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
        logging.critical(message)

class AnomalyException(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
        logging.critical(message)

class StopAnomalyFoundException(Exception):
    def __init__(self):
        super(Exception, self).__init__()
        logging.critical('Anomaly Found. Stop.')
