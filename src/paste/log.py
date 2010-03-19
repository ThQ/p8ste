import logging

class DebugHandler (logging.Handler):
    logs = []
    def emit (self, record):
        DebugHandler.logs.append(record)
        return 1
