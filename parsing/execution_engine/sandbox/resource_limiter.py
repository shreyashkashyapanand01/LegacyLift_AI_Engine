import signal


class TimeoutException(Exception):
    pass


def _handle_timeout(signum, frame):
    raise TimeoutException("Execution timed out")


def set_timeout(seconds=3):
    signal.signal(signal.SIGALRM, _handle_timeout)
    signal.alarm(seconds)


def clear_timeout():
    signal.alarm(0)