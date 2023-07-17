# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SolarPWCalculator
                                 A QGIS plugin
 pass
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2022-10-07
        git sha              : $Format:%H$
        copyright            : (C) 2022 by SABZ
        email                : yavuzdogan@gumushane.edu.tr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from multiprocessing import parent_process
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.core import *
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
import re
import pickle
from PyQt5.QtWidgets import*
import requests
from matplotlib.figure import Figure
from pyqtgraph import PlotWidget
import random
import json
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore
import glob
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QImage, QPainter
from qgis.core import QgsProject
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QInputDialog
from qgis.PyQt.QtCore import Qt
from qgis.gui import *
from selenium.webdriver.common.keys import Keys
from qgis.PyQt.QtWidgets import QAction, QMainWindow
from PyQt5.QtCore import pyqtSignal
from .maptool import PointTool
from PyQt5.QtCore import QUrl
from PyQt5.QtWebKitWidgets import *
from selenium.webdriver.support.select import Select
from .resources import *
from .Solar_PW_Calculator_dialog import SolarPWCalculatorDialog
import os.path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import numpy as np
from scipy import linalg
import math
import open3d as o3d
import laspy as lp
import os
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import sys 
from qgis.utils import iface
from qgis.core import QgsVectorFileWriter
from PyQt5.QtCore import QVariant
from pathlib import Path
import pandas as pd
from PyQt5.QtWidgets import QMessageBox


class SolarPWCalculator:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SolarPWCalculator_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Solar PW Calculator')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SolarPWCalculator', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Solar_PW_Calculator/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'SolarPWCalculator'),
            callback=self.run,
            parent=self.iface.mainWindow())
        

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Solar PW Calculator'),
                action)
            self.iface.removeToolBarIcon(action)

    # def surfnet(self,address):
    #     # options = Options()
    #     # options.headless = True
    #     # # prefs = {"download.default_directory" : QgsApplication.qgisSettingsDirPath()}
    #     # # options.add_experimental_option("prefs",prefs)
    #     # web = webdriver.Chrome(options=options)
            
    #     # web.maximize_window()
    #     # web.set_window_size(1920, 1080)
    #     # web.get(address)
    #     if not os.path.exists(str(Path.home() / "Downloads" / "Temp")):
    #         os.mkdir(str(Path.home() / "Downloads" / "Temp"))
    #     download_path = str(Path.home() / "Downloads"  / "Temp")
    #     chrome_options = Options()
    #     chrome_options.add_experimental_option("prefs", {
    #     "download.default_directory": download_path,
    #     "download.prompt_for_download": False,
    #     })

    #     chrome_options.add_argument("--headless")
    #     driver = webdriver.Chrome(chrome_options=chrome_options)

    #     driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    #     params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_path}}
    #     command_result = driver.execute("send_command", params)
    #     driver.maximize_window()
    #     driver.set_window_size(1920, 1080)
    #     driver.get(address)
    #     return driver 
    
    def main (self):
        global df
        if 'df' in globals():
            del df
        if 'buildingNames' in globals():
            del buildingNames
        progressbar = QProgressBar()
        progressbar.setMaximum(100)
        myprogressbar=self.my_msg_bar.createMessage("Building roof surfaces are calculating...")
        progressbar.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        myprogressbar.layout().addWidget(progressbar)
        self.my_msg_bar.pushWidget(myprogressbar,Qgis.Info,duration=1)
        progressVal=0
        if 'transformedCenterPoints' in globals():
            def surfacenormals(PC):
                PC = np.vstack((PC,np.mean(PC,axis=0)))
                pcd = o3d.geometry.PointCloud()
                pcd.points = o3d.utility.Vector3dVector(PC)
                pcd.estimate_normals()
                pcd.orient_normals_to_align_with_direction( orientation_reference=[0.0, 0.0, 1.0])
                normals = np.asarray(pcd.normals)
                return normals[-1]  

            def Azimuth(normalVec):
                angle = math.degrees(math.atan(normalVec[0]/normalVec[1]))
                if normalVec[0]>=0 and normalVec[1]>=0:
                    angle += 180
                elif normalVec[0]<0 and normalVec[1]>=0:
                    angle += 180
                elif normalVec[0]<0 and normalVec[1]<0:
                    angle = angle
                elif normalVec[0]>=0 and normalVec[1]<0:
                    angle += 360
                    if angle > 360:
                        angle -= 360
                if angle>180:
                    angle=angle-360
                return angle

            def Tilt(normalVec):
                compoundXY = np.sqrt(np.sum([normalVec[0]**2,  normalVec[1]**2]))
                tilt = math.degrees(math.atan(compoundXY/normalVec[2]))
                if np.isnan(tilt):
                    tilt=0
                return tilt
            
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(PC)
            buildingLabels = np.array(pcd.cluster_dbscan(eps=2, min_points=10))
            max_label = buildingLabels.max()+1 
            # dataframe oluştur ve çatı yüzeylerini bul
            df = pd.DataFrame(columns = ['BUILDINGBOUNDS','BUILDINGAREA','BUILDINGCENTER','XYZ','NUMROOFSURF','SURFXYZ','SURFAREA','SURFBOUNDS','SURFORIENTATION','SURFTILT','PVYEAR','PVMONTH','JSONFILES'])
            pd.set_option('mode.chained_assignment', None)
            segment_models = {}
            segments = {}
            d_threshold = float(self.dlg.lineEdit_5.text())
            dbscanEPS = int(self.dlg.lineEdit_3.text())
            for j in (range(max_label)):
                
                indices = np.where(buildingLabels==j)
                rest = pcd.select_by_index(indices[0])
                sizePC = len(indices[0])
                CHull = ConvexHull(np.asarray(rest.points)[:,:2])
                df.loc[j] = [np.asarray(rest.points)[CHull.vertices,:], np.round(CHull.volume,decimals=2),np.mean(np.asarray(rest.points),axis=0), np.asarray(rest.points, dtype=object),0,0,0,0,0,0,0,0,0]
                i = 0
                roofPlaneArea = []
                segmentBounds = []
                Razimuth = []
                Rtilt = []
                Rseg = []
                while True:
                    colors = plt.get_cmap("tab20c")(i)
                    try:     
                        segment_models[i], inliers = rest.segment_plane(distance_threshold=d_threshold,ransac_n=int(self.dlg.lineEdit_7.text()),num_iterations=int(self.dlg.lineEdit_6.text()))
                        segments[i] = rest.select_by_index(inliers)
                        labels = np.array(segments[i].cluster_dbscan(eps=dbscanEPS, min_points=int(self.dlg.lineEdit_4.text())))
                        candidates = [len(np.where(labels==j)[0]) for j in np.unique(labels)]
                        best_candidate = int(np.unique(labels)[np.where(candidates==np.max(candidates))[0]])
                        rest = rest.select_by_index(inliers, invert=True)+segments[i].select_by_index(list(np.where(labels!=best_candidate)[0]))
                        segments[i] = segments[i].select_by_index(list(np.where(labels==best_candidate)[0]))
                        segments[i].paint_uniform_color(list(colors[:3]))
                        remainingPC = np.asarray(rest.points).shape[0]
                        points = np.asarray(segments[i].points)
                        try:
                            CHull = ConvexHull(points[:,:2])
                        except:
                            rest=rest+segments[i]
                        else:
                            roofPlaneArea.append(np.round(CHull.volume,decimals=2))
                            segmentBounds.append(points[CHull.vertices,:])
                            Rnormals = surfacenormals(points)
                            Razimuth.append(np.round(Azimuth(Rnormals),decimals=2))
                            Rtilt.append(np.round(Tilt(Rnormals),decimals=2))
                            Rseg.append(np.asarray(segments[i].points))
                            df['NUMROOFSURF'][j] = i+1
                            i+=1
                            
                    except:
                        pass    

                    df['SURFAREA'][j] = [roofPlaneArea]
                    df['SURFBOUNDS'][j] = segmentBounds
                    df['SURFORIENTATION'][j] = [Razimuth]
                    df['SURFTILT'][j] = [Rtilt]
                    df['SURFXYZ'][j] = Rseg
                    if remainingPC<10:
                        break
                progressVal+=1
                percent = (progressVal/max_label) * 100
                progressbar.setValue(percent)
                            
            progressbar = QProgressBar()
            progressbar.setMaximum(100)
            myprogressbar=self.my_msg_bar.createMessage("Retrieving data from the PVGIS database...")
            progressbar.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
            myprogressbar.layout().addWidget(progressbar)
            self.my_msg_bar.pushWidget(myprogressbar,Qgis.Info,duration=1)
            progressVal=0
            for i in range(max_label):
                temp=[]
                temp2=[]
                temp3=[]
                for j in range(df['NUMROOFSURF'][i]):
                    if max_label!=0:
                        lat=transformedCenterPoints[i][1]
                        lon=transformedCenterPoints[i][0]
                    else:
                        self.my_msg_bar.pushMessage("Error", "No buildings found in the dataset.", level=Qgis.Critical, duration=4)
                    PVdata=str(self.dlg.PVDatabase.currentText())
                    PVtec=str(self.dlg.PVTech.currentText())
                    PeakPower=str(self.dlg.PeakPower.text())
                    SystemLoss=str(self.dlg.SystemLoss.text())
                    mount="Roof added / Building integrated"
                    tilt=df['SURFTILT'][i][0][j]
                    orientation=df['SURFORIENTATION'][i][0][j]
                    if self.dlg.PVPrice.isChecked():
                        PVCost=str(self.dlg.PVCost.text())
                        Interest=str(self.dlg.Interest.text())
                        LifeTime=self.dlg.Lifetime.text()
                    def toURL(lat,lon,PVtec,PeakPower,SystemLoss,tilt,orientation,PVCost=0,Interest=0,LifeTime=0):
                        baseURL="https://re.jrc.ec.europa.eu/api/PVcalc?"
                        if PVtec=="Crystalline silicon":
                            PVtec="crystSi"
                        URL=baseURL+"lat="+str(lat)+"&lon="+str(lon)+"&pvtechchoice="+str(PVtec)+"&peakpower="+str(PeakPower)+"&loss="+str(SystemLoss)+"&mountingplace=building"+"&angle="+str(tilt)+"&aspect="+str(orientation)+"&systemcost="+str(PVCost)+"&interest="+str(Interest)+"&lifetime="+str(LifeTime)+"&outputformat=json"
                        response_API = requests.get(URL)
                        ceyson = response_API.json()
                        return ceyson, response_API.status_code
                                        
                    if self.dlg.PVPrice.isChecked():
                        ceyson,statusCode=toURL(lat,lon,PVtec,PeakPower,SystemLoss,tilt,orientation,PVCost,Interest,LifeTime)
                        if statusCode!=200:
                            while True:
                                time.sleep(2)
                                ceyson,statusCode=toURL(lat,lon,PVtec,PeakPower,SystemLoss,tilt,orientation,PVCost,Interest,LifeTime)
                                if statusCode==200:
                                    break
                    else:
                        ceyson,statusCode=toURL(lat,lon,PVtec,PeakPower,SystemLoss,tilt,orientation)
                        if statusCode!=200:
                            while True:
                                time.sleep(2)
                                ceyson,statusCode=toURL(lat,lon,PVtec,PeakPower,SystemLoss,tilt,orientation)
                                if statusCode==200:
                                    break
                    temp.append([ceyson])
                
                df["JSONFILES"][i]=temp
                for jsonData in df["JSONFILES"][i][0]:
                    temp2.append([jsonData["outputs"]["totals"]['fixed']['E_y']])
                    temp3.append([jsonData["outputs"]["monthly"]["fixed"]])
                df["PVYEAR"][i]=temp2
                df["PVMONTH"][i]=temp3
                progressVal+=1
                percent = (progressVal/max_label) * 100
                progressbar.setValue(percent)
                time.sleep(0.2)
            
            # infile = open('C:\\Users\\samwm\\Desktop\\PYTHON_SAM\\SOLAR\\82_bina.pickle','rb')
            # new_dict = pickle.load(infile)
            # infile.close()
            # file = open('dataframe.pickle', 'wb')
            # pickle.dump(df, file)
            # file.close()
            BuildingNames=[]
            for i in range(len(df)):
                tempds=df.iloc[i]
                BuildingNames.append("Building "+str(i+1))

            self.dlg.comboBox.clear()
            for i in BuildingNames:
                self.dlg.comboBox.addItem(i)
            self.my_msg_bar.pushMessage("Completed", "Process completed.", level=Qgis.Success, duration=4)
        else:
            self.my_msg_bar.pushMessage("Important", "First, you need to determine the approximate coordinates of the roof.", level=Qgis.Critical, duration=4)                
    def open_map(self):
        global map
        import logging
        class WebPage(QWebPage):
            
            """
            Makes it possible to use a Python logger to print javascript console messages
            """
            def __init__(self, logger=None, parent=self.dlg):
                super(WebPage, self).__init__(parent)
                if not logger:
                    logger = logging
                self.logger = logger
            # def javaScriptConsoleMessage(self, msg, lineNumber, sourceID):
            #     # self.logger.warning("JsConsole(%s:%d): %s" % (sourceID, lineNumber, msg))
            #     # print(msg)
            #     global lat_map, lon_map
            #     if len(msg.split(",")) > 1:
            #         lat_map=msg.split(",")[0]
            #         lon_map=msg.split(",")[1]
            #         # print(f"lat:{lat_map}\nlon:{lon_map}")
            #         self.parent().lineEdit.setText(lat_map)
            #         self.parent().lineEdit_2.setText(lon_map)
           
        dir=str(QgsApplication.qgisSettingsDirPath())
        ext="python/plugins/solar_pw_calculator/index2.html"
        path=dir+ext
        map=self.dlg.webView
        map.setPage(WebPage())
        map.load(QUrl.fromLocalFile(path))
        map.resize(520, 310)
        
    def coordinateTransform(self):
        global transformedCenterPoints,selectedEPSG, destCrs, tr
        selectedEPSG=self.dlg.coordinateSelection.crs()
        destCrs = QgsCoordinateReferenceSystem(4326)
        tr = QgsCoordinateTransform(selectedEPSG, destCrs, QgsProject.instance())
        frame = map.page().currentFrame()
        transformedCenterPoints=[]
        if 'max_label2' in globals():
            for i in range(max_label2):    
                transformedCoordinates=tr.transform(QgsPointXY(Center[i][0],Center[i][1]))
                transformedX=transformedCoordinates.x()
                transformedY=transformedCoordinates.y()
                transformedCenterPoints.append([transformedX, transformedY])
                JScode="""addMarker('{latitude}','{longitude}');"""
                JScodeFormat = JScode.format(latitude=transformedY, longitude=transformedX)
                frame.evaluateJavaScript(JScodeFormat)
            self.my_msg_bar.pushMessage("Coordinate transformation completed.", level=Qgis.Success)
        else:
            self.my_msg_bar.pushMessage("Error","Please load point cloud file.", level=Qgis.Critical)
    def savexlsx(self):
        file_path, _filter = QFileDialog.getSaveFileName(self.dlg, "Save File", "SPAN_Output","Excel Files (*.xlsx)")
        self.dlg.saveFile_2.setText(file_path)
        columnHeaders = []
        rowHeaders = []

        # create column header list
        for j in range(self.dlg.tableWidget.model().columnCount()):
            columnHeaders.append(self.dlg.tableWidget.horizontalHeaderItem(j).text())
        for j in range(self.dlg.tableWidget.model().rowCount()):
            rowHeaders.append(self.dlg.tableWidget.verticalHeaderItem(j).text())

        df = pd.DataFrame(columns=columnHeaders,index=rowHeaders)
        # create dataframe object recordset
        for row in range(self.dlg.tableWidget.rowCount()):
            for col in range(self.dlg.tableWidget.columnCount()):
                try:
                    df.at[rowHeaders[row], columnHeaders[col]] = self.dlg.tableWidget.item(row, col).text()
                except AttributeError:
                     df.at[rowHeaders[row], columnHeaders[col]] = 0                   
        
        
        writer = pd.ExcelWriter(file_path)         
        df.to_excel(writer, index=True, startcol=6, sheet_name='Sheet1')
        writer.sheets['Sheet1'].set_column('G:G', 40)
        writer.save()
        image = QImage(map2.page().viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        frame2.render(painter)
        painter.end()
        head, _=os.path.split(file_path)
        tail="surface_map.png"
        impath=os.path.join(head,tail)
        image.save(impath)
        img1 = Image(impath)
        wb = load_workbook(file_path)
        ws = wb.active
        ws.add_image(img1, 'A1')
        wb.save(file_path)
        os.remove(impath)
        self.my_msg_bar.pushMessage("File Saved", "Excel file exported.", level=Qgis.Success, duration=3)
        # print('Excel file exported')
        pass
    def savejson(self):
        file_path, _filter = QFileDialog.getSaveFileName(self.dlg, "Save File", "SPAN_Output","JSON Files (*.json)")
        self.dlg.saveFile_3.setText(file_path)
        df.to_json(file_path)
        self.my_msg_bar.pushMessage("File Saved", "JSON file exported.", level=Qgis.Success, duration=3)
        
    def select_PC_file(self):
        global Center, PC ,max_label2
        def CenterPoint():
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(PC)
            buildingLabels = np.array(pcd.cluster_dbscan(eps=2, min_points=10))
            max_label = buildingLabels.max()+1
            # df = pd.DataFrame(columns = ["CenterPoints"])
            Center=[]
            for j in (range(max_label)):
                indices = np.where(buildingLabels==j)
                rest = pcd.select_by_index(indices[0])
                Center.append(np.mean(np.asarray(rest.points),axis=0))
            return max_label, Center
        file_path, _filter = QFileDialog.getOpenFileName(self.dlg, "Open File", "")
        self.dlg.saveFile.setText(file_path)
        if self.dlg.saveFile.text()!="":
            extension = os.path.splitext(file_path)[1]
            fileName = os.path.splitext(os.path.basename(file_path))[0]
            if extension == ".txt":
                inFile = np.loadtxt(file_path)
                PC = inFile[:,0:3]
                if inFile.shape[1]>3:
                    color = inFile[:,3:6]
                max_label2, Center=CenterPoint()
                if max_label2>0:
                    self.my_msg_bar.pushMessage("Success", "{} buildings loaded.".format(max_label2), level=Qgis.Success, duration=3)
                else:
                    self.my_msg_bar.pushMessage("Error", "The uploaded point cloud contains no buildings. Please upload another point cloud.", level=Qgis.Critical, duration=3)
            elif extension == ".las" or extension =="laz":
                inFile = lp.read(file_path)
                # liste = list(inFile.point_format.dimension_names) # get colunm names. Can be used for selective loading
                PC = np.vstack((inFile['x'], inFile['y'], inFile['z'])).transpose()
                labels = inFile['classification']
                max_label2, Center=CenterPoint()    
                if max_label2>0:
                    self.my_msg_bar.pushMessage("Success", "{} buildings loaded.".format(max_label2), level=Qgis.Success, duration=3)
                else:
                    self.my_msg_bar.pushMessage("Error", "The uploaded point cloud contains no buildings. Please upload another point cloud.", level=Qgis.Critical, duration=3)
            elif extension == ".ply":
                pcd = o3d.io.read_point_cloud(file_path)
                PC = np.asarray(pcd.points)
                max_label2, Center=CenterPoint() 
                if max_label2>0:
                    self.my_msg_bar.pushMessage("Success", "{} buildings loaded.".format(max_label2), level=Qgis.Success, duration=3)
                else:
                    self.my_msg_bar.pushMessage("Error", "The uploaded point cloud contains no buildings. Please upload another point cloud.", level=Qgis.Critical, duration=3)
            else:
                self.dlg.saveFile.setText("")
                self.my_msg_bar.pushMessage("Error", "File type not recognized. Please use one of the extensions '.txt', '.ply', '.las' or '.laz'", level=Qgis.Critical, duration=4)

    def loadHTMLMap(self):
        global map2, frame2
        dir2=str(QgsApplication.qgisSettingsDirPath())
        ext2="python/plugins/solar_pw_calculator/index2.html"
        path2=dir2+ext2
        map2=self.dlg.webView_2
        map2.load(QUrl.fromLocalFile(path2))
        map2.resize(340, 360)
        frame2 = map2.page().currentFrame()
        
    def drawPoly(self,points,transformedCenterPoints,surfaceNumber,color):
        lon_center, lat_center=transformedCenterPoints
        lon_center_surf, lat_center_surf=np.mean(points,axis=0)
        lat_center=str(lat_center)
        lon_center=str(lon_center)
        JSPoints="addPoly('{points}','{lat_center}','{lon_center}','{color}')"
        JSPointFormat = JSPoints.format(points=points, lat_center=lat_center, lon_center=lon_center,color=color)
        frame2.evaluateJavaScript(JSPointFormat)
        JSMarker="""addMarkerFrame2('{longitude}','{latitude}','{message}');"""
        JSMarkerFormat = JSMarker.format(latitude=lat_center_surf, longitude=lon_center_surf,message='Surface '+str(surfaceNumber))
        frame2.evaluateJavaScript(JSMarkerFormat)
    
    def create_graph(self,GraphicsObject,y,sn,color):
        x=range(1,13)
        xlab = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        xval = list(range(1,len(xlab)+1))
        ticks=[]
        for i, item in enumerate(xlab):
            ticks.append( (xval[i], item) )
        ticks = [ticks]
        bargraph1 = pg.BarGraphItem(x = xval, height = y, width = 0.6, brush =color)
        
        GraphicsObject.clear()
        title="Surface {sn} Photovoltaic Energy Production".format(sn=sn)
        # GraphicsObject.setWindowTitle(title)
        GraphicsObject.addItem(bargraph1)
        ax_bottom = GraphicsObject.getAxis('bottom')
        ax_bottom.setTicks(ticks)
        ax_bottom.setLabel(title)
        # ax_bottom.setLabel('Months')
        ax_left = GraphicsObject.getAxis('left')
        ax_left.setLabel('PV Out (kWh)')
        ax_left.setStyle(showValues=True)
        # bargraph1.showGrid(x = False, y = True, alpha = 0.5)
        
    def updatePoly(self):
        selectedString=self.dlg.comboBox.currentText()
        bn=re.findall(r"[-+]?(?:\d*\.\d+|\d+)",selectedString)
        bn=int(bn[0])
        tempds=df.iloc[bn-1]        
        self.dlg.graphicsView_1.clear()
        self.dlg.graphicsView_2.clear()
        self.dlg.graphicsView_3.clear()
        self.dlg.graphicsView_4.clear()
        self.dlg.graphicsView_5.clear()
        self.dlg.graphicsView_6.clear()
        self.dlg.graphicsView_7.clear()
        self.dlg.graphicsView_8.clear()
        for sn in range(tempds["NUMROOFSURF"]):
            r = lambda: random.randint(0,255)
            color = '#{:02x}{:02x}{:02x}'.format(r(), r(), r())
            surfBound=tempds["SURFBOUNDS"][sn]
            surfBoundList=surfBound.tolist()
            transformedBounds=[]
            for i in surfBoundList:    
                transformedBoundPoint=tr.transform(QgsPointXY(i[0],i[1]))
                transformedX=transformedBoundPoint.x()
                transformedY=transformedBoundPoint.y()
                transformedBounds.append([transformedY, transformedX])
            self.drawPoly(transformedBounds,transformedCenterPoints[bn-1],sn+1,color)
            monthly_data=pd.DataFrame(tempds["JSONFILES"][sn][0]["outputs"]["monthly"]["fixed"])
            monthlyEnergy=(monthly_data["E_m"].values.T*tempds["SURFAREA"][0][sn]).tolist()
            exec("self.create_graph(self.dlg.graphicsView_{sn},monthlyEnergy,{sn},color)".format(sn=sn+1))          
        self.my_msg_bar.pushMessage("Completed", "Surfaces were loaded.", level=Qgis.Success, duration=3)
    
    def getInfo(self):
        selectedString=self.dlg.comboBox.currentText()
        bn=re.findall(r"[-+]?(?:\d*\.\d+|\d+)",selectedString)
        bn=int(bn[0])
        tempds=df.iloc[bn-1]
        table=self.dlg.tableWidget
        table.setColumnCount(tempds["NUMROOFSURF"])
        table.setRowCount(13)
        # table.setMinimumWidth(200)
        # table.setMinimumHeight(500)
        labels=[]
        for surfNum in range(1,tempds["NUMROOFSURF"]+1):
            temp="Surface-{surfNum}".format(surfNum=surfNum)
            labels.append(temp)
        table.setHorizontalHeaderLabels(labels)
        table.setVerticalHeaderLabels(["Surface Area (m\u00b2)","Surface Azimuth (Degree)","Tilt Angle (Degree)","Average daily photovoltaic output (kWh)","Average monthly photovoltaic output (kWh)","Average yearly photovoltaic output (kWh)","Average daily global irradiation (kWh/m\u00b2)","Angle of incidence loss (%)","Temperature and irradiance loss (%)","Total loss (%)","Total daily PV output of the building (kWh)","Total monthly PV output of the building (kWh)","Total yearly PV output of the building (kWh)"])
        for j in range(tempds["NUMROOFSURF"]):
            table.setItem(0, j, QTableWidgetItem(str(tempds["SURFAREA"][0][j])))
            table.setItem(1, j, QTableWidgetItem(str(tempds["SURFORIENTATION"][0][j])))
            table.setItem(2, j, QTableWidgetItem(str(tempds["SURFTILT"][0][j])))
            table.setItem(3, j, QTableWidgetItem(str(np.round(tempds["JSONFILES"][j][0]["outputs"]["totals"]["fixed"]["E_d"]*tempds["SURFAREA"][0][j],2))))
            table.setItem(4, j, QTableWidgetItem(str(np.round(tempds["JSONFILES"][j][0]["outputs"]["totals"]["fixed"]["E_m"]*tempds["SURFAREA"][0][j],2))))
            table.setItem(5, j, QTableWidgetItem(str(np.round(tempds["JSONFILES"][j][0]["outputs"]["totals"]["fixed"]["E_y"]*tempds["SURFAREA"][0][j],2))))
            table.setItem(6, j, QTableWidgetItem(str(tempds["JSONFILES"][j][0]["outputs"]["totals"]["fixed"]["H(i)_d"])))
            table.setItem(7, j, QTableWidgetItem(str(tempds["JSONFILES"][j][0]["outputs"]["totals"]["fixed"]["l_aoi"])))
            table.setItem(8, j, QTableWidgetItem(str(tempds["JSONFILES"][j][0]["outputs"]["totals"]["fixed"]["l_tg"])))
            table.setItem(9, j, QTableWidgetItem(str(tempds["JSONFILES"][j][0]["outputs"]["totals"]["fixed"]["l_total"])))
        totalDaily=0
        totalMonthly=0
        totalYearly=0
        for i in range(tempds["NUMROOFSURF"]):
            totalDaily+=float(table.item(3, i).text())
            totalMonthly+=float(table.item(4, i).text())
            totalYearly+=float(table.item(5, i).text())
        
        table.setSpan(10,0,1,tempds["NUMROOFSURF"])
        table.setSpan(11,0,1,tempds["NUMROOFSURF"])
        table.setSpan(12,0,1,tempds["NUMROOFSURF"])
        table.setItem(10, 0, QTableWidgetItem(str(np.round(totalDaily,decimals=2))))
        table.setItem(11, 0, QTableWidgetItem(str(np.round(totalMonthly,decimals=2))))
        table.setItem(12, 0, QTableWidgetItem(str(np.round(totalYearly,decimals=2))))
    
        header = table.horizontalHeader() 
        header2 = table.verticalHeader() 
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        header2.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    
    def forwardPage(self):
        page_num=self.dlg.stackedWidget.currentIndex()
        self.dlg.stackedWidget.setCurrentIndex(page_num+1)
        
    def backPage(self):
        page_num=self.dlg.stackedWidget.currentIndex()
        self.dlg.stackedWidget.setCurrentIndex(page_num-1)    
     
    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = SolarPWCalculatorDialog()
            self.dlg.setFixedSize(1089,842)
            self.open_map()
            self.loadHTMLMap()
            self.my_msg_bar = QgsMessageBar()
            self.dlg.verticalLayout.insertWidget(0, self.my_msg_bar)
            self.my_msg_bar.pushMessage("Welcome", "This plugin is ready at your service.", level=Qgis.Success, duration=3)
            self.dlg.graphicsView_1.setBackground('white')
            self.dlg.graphicsView_2.setBackground('white')
            self.dlg.graphicsView_3.setBackground('white')
            self.dlg.graphicsView_4.setBackground('white')
            self.dlg.graphicsView_5.setBackground('white')
            self.dlg.graphicsView_6.setBackground('white')
            self.dlg.graphicsView_7.setBackground('white')
            self.dlg.graphicsView_8.setBackground('white')
            self.dlg.graphicsView_9.setBackground('white')
            self.dlg.graphicsView_10.setBackground('white')
            self.dlg.graphicsView_11.setBackground('white')
            self.dlg.graphicsView_12.setBackground('white')
            self.dlg.graphicsView_13.setBackground('white')
            self.dlg.graphicsView_14.setBackground('white')
            self.dlg.graphicsView_15.setBackground('white')
            self.dlg.graphicsView_16.setBackground('white')
            self.dlg.graphicsView_17.setBackground('white')
            self.dlg.graphicsView_18.setBackground('white')
            self.dlg.graphicsView_19.setBackground('white')
            self.dlg.graphicsView_20.setBackground('white')
            self.dlg.graphicsView_21.setBackground('white')
            self.dlg.graphicsView_22.setBackground('white')
            self.dlg.graphicsView_23.setBackground('white')
            self.dlg.graphicsView_24.setBackground('white')
            onlyFloat = QDoubleValidator()
            self.dlg.lineEdit_3.setValidator(onlyFloat)
            onlyIntMinPts = QIntValidator()
            self.dlg.lineEdit_4.setValidator(onlyIntMinPts)
            onlyFloatDt = QDoubleValidator()
            self.dlg.lineEdit_5.setValidator(onlyFloatDt)
            onlyIntItN = QIntValidator()
            self.dlg.lineEdit_6.setValidator(onlyIntItN)
            onlyFloatSPP = QDoubleValidator()
            self.dlg.lineEdit_7.setValidator(onlyFloatSPP)            

        self.dlg.browse_1.clicked.connect(self.select_PC_file)
        self.dlg.browse_2.clicked.connect(self.savexlsx)
        self.dlg.browse_3.clicked.connect(self.savejson)

        self.dlg.pushButton.clicked.connect(self.coordinateTransform)
        self.dlg.calc_PW.clicked.connect(self.main)
        self.dlg.select.clicked.connect(self.updatePoly)
        self.dlg.select.clicked.connect(self.dlg.widget.setDisabled)
        self.dlg.backButton.clicked.connect(self.backPage)
        self.dlg.forwardButton.clicked.connect(self.forwardPage)
        self.dlg.select.clicked.connect(self.getInfo)
        self.dlg.PVPrice.toggled.connect(self.dlg.PVCost.setEnabled)
        self.dlg.PVPrice.toggled.connect(self.dlg.Interest.setEnabled)
        self.dlg.PVPrice.toggled.connect(self.dlg.Lifetime.setEnabled)
        self.dlg.PVPrice.toggled.connect(self.dlg.label_10.setEnabled)
        self.dlg.PVPrice.toggled.connect(self.dlg.label_11.setEnabled)
        self.dlg.PVPrice.toggled.connect(self.dlg.label_12.setEnabled)
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()