from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QCursor, QIcon
from qgis.PyQt.QtWidgets import QApplication

from qgis.gui import QgsMapToolEmitPoint, QgsMapMouseEvent
from qgis.core import (QgsCoordinateReferenceSystem,
                       QgsCoordinateTransform,
                       QgsProject
                       )
class PointTool(QgsMapToolEmitPoint):

    canvasClicked = pyqtSignal('QgsPointXY')

    def canvasReleaseEvent(self, event: QgsMapMouseEvent):
        # Get the click and emit a transformed point
        point_clicked = event.mapPoint()
        self.canvasClicked.emit(point_clicked)