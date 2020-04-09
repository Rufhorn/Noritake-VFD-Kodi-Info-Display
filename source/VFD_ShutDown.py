import signal

class ShutDownIndicator:
    """react on termination signal"""
    
    def __init__(self):
        self.exit_operation = False
        signal.signal(signal.SIGINT, self.shut_down)
        signal.signal(signal.SIGTERM, self.shut_down)

    def shut_down(self, signum, frame):
        self.exit_operation = True
