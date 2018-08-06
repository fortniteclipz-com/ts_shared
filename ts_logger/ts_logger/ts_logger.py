import ts_config

import os
import daiquiri
# import pythonjsonlogger
import logging
import sys

# format_str = '%(asctime)%(levelname)%(name)%(message)'
# formatter = pythonjsonlogger.jsonlogger.JsonFormatter(format_str)

# os.makedirs(os.path.dirname('./tmp/'), exist_ok=True)
daiquiri.setup(
    level=ts_config.get('log.level'),
    outputs=[
        daiquiri.output.Stream(
            sys.stdout,
            daiquiri.formatter.ColorExtrasFormatter(
                keywords=[],
                fmt=(
                    "%(asctime)s [%(process)d] %(color)s%(levelname)-8.8s "
                    "%(name)s | %(message)s%(color_stop)s %(extras)s"
                ),
            )
        )
        # daiquiri.output.File('./tmp/debug.log', formatter=formatter, level=logging.DEBUG),
        # daiquiri.output.File('./tmp/info.log', formatter=formatter, level=logging.INFO),
        # daiquiri.output.File('./tmp/errors.log', formatter=formatter, level=logging.ERROR)
    ],
    capture_warnings=False
)

class get:
    def __init__(self, name):
        self.logger = daiquiri.getLogger(name)
        self.args = ()
        self.kwargs = {}

    def set(self, *args, **kwargs):
        self.kwargs = {**self.kwargs, **kwargs}
        return self

    def info(self, *args, **kwargs):
        kwargs = {**self.kwargs, **kwargs}
        self.logger.info(*args, **kwargs)
        return self

    def warn(self, *args, **kwargs):
        kwargs = {**self.kwargs, **kwargs}
        self.logger.warn(*args, **kwargs)
        return self

    def error(self, *args, **kwargs):
        kwargs = {**self.kwargs, **kwargs}
        self.logger.error(*args, **kwargs)
        return self

__all__ = ['get']



