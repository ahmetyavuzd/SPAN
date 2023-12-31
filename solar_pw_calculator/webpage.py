import logging
from PyQt5.QtWebEngineWidgets import QWebPage
class WebPage(QWebPage):
    """
    Makes it possible to use a Python logger to print javascript console messages
    """
    def __init__(self, logger=None, parent=None):
        super(WebPage, self).__init__(parent)
        if not logger:
            logger = logging
        self.logger = logger

    def javaScriptConsoleMessage(self, msg, lineNumber, sourceID):
        self.logger.debug("JsConsole(%s:%d): %s" % (sourceID, lineNumber, msg))