
import sys, csv, struct
import os 
import numpy as np
import gdal
from qgis.PyQt.QtCore import * #QSettings, QTranslator, qVersion, QCoreApplication, QFileInfo
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import * #QAction, QFileDialog, QSizePolicy, QPushButton, QDialog, QGridLayout, QDialogButtonBox
from qgis.core import *
from qgis.gui import * #QgsMessageBar

import matplotlib as plt
from matplotlib import pyplot as pllt

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .test_plugin_dialog import test_pluginDialog
import os.path



class test_plugin:
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
            'test_plugin_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&test_plugin')

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
        return QCoreApplication.translate('test_plugin', message)


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
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/test_plugin/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&test_plugin'),
                action)
            self.iface.removeToolBarIcon(action)

    def select_output_file(self):
        filename, _filter = QFileDialog.getSaveFileName(self.dlg, "Select output file ","", '*.csv')
        self.dlg.lineEdit.setText(filename)
        
    def select_input_file1(self):
        filename1, _filter = QFileDialog.getOpenFileName(self.dlg, "Select an input file ","", '*.txt')
        self.dlg.lineEdit_7.setText(filename1)    

    def select_input_file2(self):
        filename2, _filter = QFileDialog.getOpenFileName(self.dlg, "Select an input file ","", '*.txt')
        self.dlg.lineEdit_8.setText(filename2)   

    def select_input_file3(self):
        filename3, _filter = QFileDialog.getOpenFileName(self.dlg, "Select an input file ","", '*.txt')
        self.dlg.lineEdit_9.setText(filename3)
        
    def select_input_file1_restoration(self):
        filename1, _filter = QFileDialog.getOpenFileName(self.dlg, "Select an input file ","", '*.txt')
        self.dlg.lineEdit_164.setText(filename1)    

    def select_input_file2_restoration(self):
        filename2, _filter = QFileDialog.getOpenFileName(self.dlg, "Select an input file ","", '*.txt')
        self.dlg.lineEdit_174.setText(filename2)   

    def select_input_file3_restoration(self):
        filename3, _filter = QFileDialog.getOpenFileName(self.dlg, "Select an input file ","", '*.txt')
        self.dlg.lineEdit_171.setText(filename3)
        
        Qmax_input = 0;
    def import1(self):
        global Qmax_input
        path = self.dlg.lineEdit_7.text()
        print("Qmax Input imported from: ", path)
        self.dlg.lineEdit_7.setText("Imported")
        Qmax_input = np.loadtxt(path, delimiter = " ")
        
        Qmax_input_restoration = 0;
    def import1_restoration(self):
        global Qmax_input_restoration
        path = self.dlg.lineEdit_164.text()
        print("Qmax Input imported from: ", path)
        self.dlg.lineEdit_164.setText("Imported")
        Qmax_input_restoration = np.loadtxt(path, delimiter = " ")
        
        Qmax_outputFP = 0;
    def import2(self):
        global Qmax_outputFP
        path = self.dlg.lineEdit_8.text()
        print("Qmax OutputFP imported from: ", path)
        self.dlg.lineEdit_8.setText("Imported")
        Qmax_outputFP = np.loadtxt(path, delimiter = " ")
        
        Qmax_outputFP_restoration = 0;
    def import2_restoration(self):
        global Qmax_outputFP_restoration
        path = self.dlg.lineEdit_174.text()
        print("Qmax OutputFP imported from: ", path)
        self.dlg.lineEdit_174.setText("Imported")
        Qmax_outputFP_restoration = np.loadtxt(path, delimiter = " ")

        Qmax_outputNoFP = 0;
    def import3(self):
        global Qmax_outputNoFP
        path = self.dlg.lineEdit_9.text()
        print("Qmax OutputNoFP imported from: ", path)
        Qmax_outputNoFP = np.loadtxt(path, delimiter = " ")
        self.dlg.lineEdit_9.setText("Imported")
        
        Qmax_outputNoFP_restoration = 0;
    def import3_restoration(self):
        global Qmax_outputNoFP_restoration
        path = self.dlg.lineEdit_171.text()
        print("Qmax OutputNoFP imported from: ", path)
        Qmax_outputNoFP_restoration = np.loadtxt(path, delimiter = " ")
        self.dlg.lineEdit_171.setText("Imported")

        Qbankfull = 0;
    def import4(self):
        global Qbankfull
        path = self.dlg.lineEdit_2.text()
        Qbankfull = np.asarray(path, dtype='float64')#float(input(path))
        self.dlg.lineEdit_2.setText("Imported")
        print("Qbankfull imported: ", Qbankfull)
        
        Qbankfull_restoration = 0;
    def import4_restoration(self):
        global Qbankfull_restoration
        path = self.dlg.lineEdit_173.text()
        Qbankfull_restoration = np.asarray(path, dtype='float64')#float(input(path))
        self.dlg.lineEdit_173.setText("Imported")
        print("Qbankfull imported: ", Qbankfull_restoration)

        Delta_Qtot = 0;
    def substract1(self):
        global Delta_Qtot
        Delta_Qtot = abs(max(Qmax_input[:,1])-max(Qmax_outputFP[:,1]))
        self.dlg.lineEdit_10.setText(str("{:.4f}".format(Delta_Qtot)))
        
        Delta_Qtot_restoration = 0;
    def substract1_restoration(self):
        global Delta_Qtot_restoration
        Delta_Qtot_restoration = abs(max(Qmax_input_restoration[:,1])-max(Qmax_outputFP_restoration[:,1]))
        self.dlg.lineEdit_166.setText(str("{:.4f}".format(Delta_Qtot_restoration)))

        Delta_Qrc = 0;
    def substract2(self):
        global Delta_Qrc
        Delta_Qrc = abs(max(Qmax_input[:,1])-max(Qmax_outputNoFP[:,1]))
        self.dlg.lineEdit_11.setText(str("{:.4f}".format(Delta_Qrc)))
        
        Delta_Qrc_restoration = 0;
    def substract2_restoration(self):
        global Delta_Qrc_restoration
        Delta_Qrc_restoration = abs(max(Qmax_input_restoration[:,1])-max(Qmax_outputNoFP_restoration[:,1]))
        self.dlg.lineEdit_172.setText(str("{:.4f}".format(Delta_Qrc_restoration)))

        Delta_Q = 0;
    def substract3(self):
        global Delta_Q
        Delta_Q = abs(Delta_Qtot - Delta_Qrc)
        self.dlg.lineEdit_12.setText(str("{:.4f}".format(Delta_Q)))
        
        Delta_Q_restoration = 0;
    def substract3_restoration(self):
        global Delta_Q_restoration
        Delta_Q_restoration = abs(Delta_Qtot_restoration - Delta_Qrc_restoration)
        self.dlg.lineEdit_165.setText(str("{:.4f}".format(Delta_Q_restoration)))

        Delta_Qrelative = 0;
    def substract4(self):
        global Delta_Qrelative
        Delta_Qrelative = (Delta_Q / (max(Qmax_input[:,1]) - Qbankfull))*100
        Delta_Qrelative = "{:.2f}".format(Delta_Qrelative)
        self.dlg.lineEdit_13.setText(str(Delta_Qrelative))
        Delta_Qrelative = np.asarray(Delta_Qrelative, dtype='float64')
        
        Delta_Qrelative_restoration = 0;
    def substract4_restoration(self):
        global Delta_Qrelative_restoration
        Delta_Qrelative_restoration = (Delta_Q_restoration / (max(Qmax_input_restoration[:,1]) - Qbankfull_restoration))*100
        Delta_Qrelative_restoration = "{:.2f}".format(Delta_Qrelative_restoration)
        self.dlg.lineEdit_167.setText(str(Delta_Qrelative_restoration))
        Delta_Qrelative_restoration = np.asarray(Delta_Qrelative_restoration, dtype='float64')
        
        Delta_Ttot = 0;
    def substract5(self):
        global Delta_Ttot
        Qmaximum = max(Qmax_input[:,1])
        Qmaximum_position = np.where(Qmax_input == Qmaximum)
        Delta_Tqmax = Qmax_input[Qmaximum_position[0],0]
        Qmaximum_FP = max(Qmax_outputFP[:,1])
        Qmaximum_position_FP = np.where(Qmax_outputFP == Qmaximum_FP)
        Delta_Tqmax_FP = Qmax_outputFP[Qmaximum_position_FP[0],0]
        Delta_Ttot = abs(float(Delta_Tqmax - Delta_Tqmax_FP))
        self.dlg.lineEdit_14.setText(str(Delta_Ttot))
        
        Delta_Ttot_restoration = 0;
    def substract5_restoration(self):
        global Delta_Ttot_restoration
        Qmaximum_restoration = max(Qmax_input_restoration[:,1])
        Qmaximum_position_restoration = np.where(Qmax_input_restoration == Qmaximum_restoration)
        Delta_Tqmax_restoration = Qmax_input_restoration[Qmaximum_position_restoration[0],0]
        Qmaximum_FP_restoration = max(Qmax_outputFP_restoration[:,1])
        Qmaximum_position_FP_restoration = np.where(Qmax_outputFP_restoration == Qmaximum_FP_restoration)
        Delta_Tqmax_FP_restoration = Qmax_outputFP_restoration[Qmaximum_position_FP_restoration[0],0]
        Delta_Ttot_restoration = abs(float(Delta_Tqmax_restoration - Delta_Tqmax_FP_restoration))
        self.dlg.lineEdit_168.setText(str(Delta_Ttot_restoration))
        
        Delta_Trc = 0;
    def substract6(self):
        global Delta_Trc
        Qmaximum = max(Qmax_input[:,1])
        Qmaximum_position = np.where(Qmax_input == Qmaximum)
        Delta_Tqmax = Qmax_input[Qmaximum_position[0],0]
        Qmaximum_noFP = max(Qmax_outputNoFP[:,1])
        Qmaximum_position_noFP = np.where(Qmax_outputNoFP == Qmaximum_noFP)
        Delta_Tqmax_noFP = Qmax_outputNoFP[Qmaximum_position_noFP[0],0]
        Delta_Trc = abs(float(Delta_Tqmax - Delta_Tqmax_noFP))
        self.dlg.lineEdit_15.setText(str(Delta_Trc))
        
        Delta_Trc_restoration = 0;
    def substract6_restoration(self):
        global Delta_Trc_restoration
        Qmaximum_restoration = max(Qmax_input_restoration[:,1])
        Qmaximum_position_restoration = np.where(Qmax_input_restoration == Qmaximum_restoration)
        Delta_Tqmax_restoration = Qmax_input_restoration[Qmaximum_position_restoration[0],0]
        Qmaximum_noFP_restoration = max(Qmax_outputNoFP_restoration[:,1])
        Qmaximum_position_noFP_restoration = np.where(Qmax_outputNoFP_restoration == Qmaximum_noFP_restoration)
        Delta_Tqmax_noFP_restoration = Qmax_outputNoFP_restoration[Qmaximum_position_noFP_restoration[0],0]
        Delta_Trc_restoration = abs(float(Delta_Tqmax_restoration - Delta_Tqmax_noFP_restoration))
        self.dlg.lineEdit_169.setText(str(Delta_Trc_restoration))
        
        Delta_T = 0;
    def substract7(self):
        global Delta_T
        Delta_T = abs(float(Delta_Ttot - Delta_Trc))
        Delta_T = "{:.2f}".format(Delta_T)
        self.dlg.lineEdit_16.setText(str(Delta_T))
        Delta_T = np.asarray(Delta_T, dtype='float64')
        
        Delta_T_restoration = 0;
    def substract7_restoration(self):
        global Delta_T_restoration
        Delta_T_restoration = abs(float(Delta_Ttot_restoration - Delta_Trc_restoration))
        Delta_T_restoration = "{:.2f}".format(Delta_T_restoration)
        self.dlg.lineEdit_170.setText(str(Delta_T_restoration))
        Delta_T_restoration = np.asarray(Delta_T_restoration, dtype='float64')
        
        Delta_h = 0;
    def substract8(self):
        global Delta_h
        Delta_h = abs(float(h_tot - h_RC))
        Delta_h = "{:.2f}".format(Delta_h)
        self.dlg.lineEdit_19.setText(str(Delta_h))
        Delta_h = np.asarray(Delta_h, dtype='float64')
        
        Delta_h_restoration = 0;
    def substract8_restoration(self):
        global Delta_h_restoration
        Delta_h_restoration = abs(float(h_tot_restoration - h_RC_restoration))
        Delta_h_restoration = "{:.2f}".format(Delta_h_restoration)
        self.dlg.lineEdit_187.setText(str(Delta_h_restoration))
        Delta_h_restoration = np.asarray(Delta_h_restoration, dtype='float64')
        
        Delta_v = 0;
    def substract9(self):
        global Delta_v
        Delta_v = abs(float(v_tot - v_RC))
        Delta_v = "{:.2f}".format(Delta_v)
        self.dlg.lineEdit_45.setText(str(Delta_v))
        Delta_v = np.asarray(Delta_v, dtype='float64')
        
        Delta_v_restoration = 0;
    def substract9_restoration(self):
        global Delta_v_restoration
        Delta_v_restoration = abs(float(v_tot_restoration - v_RC_restoration))
        Delta_v_restoration = "{:.2f}".format(Delta_v_restoration)
        self.dlg.lineEdit_192.setText(str(Delta_v_restoration))
        Delta_v_restoration = np.asarray(Delta_v_restoration, dtype='float64')
        
        Delta_tau = 0;
    def substract10(self):
        global Delta_tau
        Delta_tau = abs(float(tau_tot - tau_RC))
        Delta_tau = "{:.2f}".format(Delta_tau)
        self.dlg.lineEdit_47.setText(str(Delta_tau))
        Delta_tau = np.asarray(Delta_tau, dtype='float64')
        
        Delta_tau_restoration = 0;
    def substract10_restoration(self):
        global Delta_tau_restoration
        Delta_tau_restoration = abs(float(tau_tot_restoration - tau_RC_restoration))
        Delta_tau_restoration = "{:.2f}".format(Delta_tau_restoration)
        self.dlg.lineEdit_195.setText(str(Delta_tau_restoration))
        Delta_tau_restoration = np.asarray(Delta_tau_restoration, dtype='float64')
        
        protected_habitat = 0;
    def substract11(self):
        global protected_habitat
        protected_habitat = abs(float(area_protected/area_floodplain))*100
        protected_habitat = "{:.2f}".format(protected_habitat)
        self.dlg.lineEdit_52.setText(str(protected_habitat))     
        protected_habitat = np.asarray(protected_habitat, dtype='float64')
        
        protected_habitat_restoration = 0;
    def substract11_restoration(self):
        global protected_habitat_restoration
        protected_habitat_restoration = abs(float(area_protected_restoration/area_floodplain))*100
        protected_habitat_restoration = "{:.2f}".format(protected_habitat_restoration)
        self.dlg.lineEdit_206.setText(str(protected_habitat_restoration))     
        protected_habitat_restoration = np.asarray(protected_habitat_restoration, dtype='float64')   
        
    def import_flood(self):
        layer_selected = self.dlg.mMapLayerComboBox.currentLayer()
        self.dlg.lineEdit_31.setText("Layer imported: " + str(layer_selected))
        features_selected = layer_selected.getFeatures()
        for feature in features_selected:
            geom_selected = feature.geometry()
            self.dlg.lineEdit_32.setText(str("{:.2f}".format(float(geom_selected.area()*float(0.000001))))) 
            self.dlg.lineEdit_177.setText(str("{:.2f}".format(float(geom_selected.area()))))
            
#%% Floodplain Areas ###################################################### 

# Automatic Floodplain    
        riverCenterlineVectorLayer = 0
    def select_input_file5(self):
        #global riverVectorLayer
        filename5, _filter = QFileDialog.getOpenFileName(self.dlg, "Select an input file ",r"", "Shapefiles(*.shp)")
        fileInfo = QFileInfo(filename5)
        baseName = fileInfo.baseName()
        global riverCenterlineVectorLayer
        riverCenterlineVectorLayer = QgsVectorLayer(filename5, baseName, "ogr")
        #QgsProject.instance().addMapLayer(riverCenterlineVectorLayer);
        self.dlg.lineEdit_27.setText("'"+str(baseName)+"'" + " " + "imported")

        riverVectorLayer = 0
    def select_input_file6(self):
        #global riverVectorLayer
        filename6, _filter = QFileDialog.getOpenFileName(self.dlg, "Select an input file ",r"", "Shapefiles(*.shp)")
        fileInfo = QFileInfo(filename6)
        baseName = fileInfo.baseName()
        riverVectorLayer = QgsVectorLayer(filename6, baseName, "ogr")
        #QgsProject.instance().addMapLayer(riverVectorLayer);
        self.dlg.lineEdit_25.setText("'"+str(baseName)+"'" + " " + "imported")
        
        floodVectorLayer = 0
    def select_input_file7(self):
        #global riverVectorLayer
        filename7, _filter = QFileDialog.getOpenFileName(self.dlg, "Select an input file ",r"", "Shapefiles(*.shp)")
        fileInfo = QFileInfo(filename7)
        baseName = fileInfo.baseName()
        global floodVectorLayer
        floodVectorLayer = QgsVectorLayer(filename7, baseName, "ogr")
        #QgsProject.instance().addMapLayer(floodVectorLayer);
        self.dlg.lineEdit_26.setText("'"+str(baseName)+"'" + " " + "imported")

        single_floodVectorLayer = 0
    def select_input_file8(self):
        #global riverVectorLayer
        filename8, _filter = QFileDialog.getOpenFileName(self.dlg, "Select an input file ",r"", "Shapefiles(*.shp)")
        fileInfo = QFileInfo(filename8)
        baseName = fileInfo.baseName()
        global single_floodVectorLayer
        single_floodVectorLayer = QgsVectorLayer(filename8, baseName, "ogr")
        QgsProject.instance().addMapLayer(single_floodVectorLayer)
        #QgsProject.instance().addMapLayer(floodVectorLayer);
        self.dlg.lineEdit_28.setText("'"+str(baseName)+"'" + " " + "imported")
        
        river_width = 0;
    def import5(self):
        global river_width
        path = self.dlg.lineEdit_29.text()
        river_width = np.asarray(path, dtype='float64')#float(input(path))
        
        self.dlg.lineEdit_29.setText("Imported: " + str(river_width))
        print("River width imported: ", river_width)

        no_of_points = 0;
    def import6(self):
        global no_of_points
        path = self.dlg.lineEdit_24.text()
        no_of_points = np.asarray(path, dtype='i')#float(input(path))
        self.dlg.lineEdit_24.setText("Imported: " + str(no_of_points))
        print("no_of_points imported: ", no_of_points)
        
        distance_flood = 0;
    def import7(self):
        global distance_flood
        path = self.dlg.lineEdit_30.text()
        distance_flood = np.asarray(path, dtype='i')
        self.dlg.lineEdit_30.setText("Imported: " + str(distance_flood))
        print("distance_flood imported: ", distance_flood)
        
        ratio_factor = 0;
    def import8(self):
        global ratio_factor
        path = self.dlg.lineEdit_33.text()
        ratio_factor = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_33.setText("Imported: " + str(ratio_factor))
        print("ratio_factor imported: ", ratio_factor)
        
        h_tot = 0;
    def import9(self):
        global h_tot
        path = self.dlg.lineEdit_17.text()
        h_tot = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_17.setText("Imported: " + str(h_tot))
        print("h_tot imported: ", h_tot)
        
        h_tot_restoration = 0;
    def import9_restoration(self):
        global h_tot_restoration
        path = self.dlg.lineEdit_188.text()
        h_tot_restoration = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_188.setText("Imported: " + str(h_tot_restoration))
        print("h_tot imported: ", h_tot_restoration)
        
        h_RC = 0;
    def import10(self):
        global h_RC
        path = self.dlg.lineEdit_18.text()
        h_RC = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_18.setText("Imported: " + str(h_RC))
        print("h_RC imported: ", h_RC)
        
        h_RC_restoration = 0;
    def import10_restoration(self):
        global h_RC_restoration
        path = self.dlg.lineEdit_189.text()
        h_RC_restoration = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_189.setText("Imported: " + str(h_RC_restoration))
        print("h_RC imported: ", h_RC_restoration)
        
        protected_species = 0;
    def import11(self):
        global protected_species
        path = self.dlg.lineEdit_20.text()
        protected_species = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_20.setText("Imported: " + str(protected_species))
        print("p. species imported: ", protected_species)
        protected_species = np.asarray(protected_species, dtype='float64')
        
        protected_species_restoration = 0;
    def import11_restoration(self):
        global protected_species_restoration
        path = self.dlg.lineEdit_198.text()
        protected_species_restoration = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_198.setText("Imported: " + str(protected_species_restoration))
        print("p. species imported: ", protected_species_restoration)
        protected_species_restoration = np.asarray(protected_species_restoration, dtype='float64')
        
        c_fwb = 0;
    def import12(self):
        global c_fwb
        path = self.dlg.lineEdit_21.text()
        c_fwb = np.asarray(path, dtype='float64')#float(input(path))
        self.dlg.lineEdit_21.setText("Imported: " + str(c_fwb))
        print("p. species imported: ", c_fwb)
        c_fwb = np.asarray(c_fwb, dtype='float64')
        
        c_fwb_restoration = 0;
    def import12_restoration(self):
        global c_fwb_restoration
        path = self.dlg.lineEdit_200.text()
        c_fwb_restoration = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_200.setText("Imported: " + str(c_fwb_restoration))
        print("p. species imported: ", c_fwb_restoration)
        c_fwb_restoration = np.asarray(c_fwb_restoration, dtype='float64')
        
        buildings = 0;
    def import13(self):
        global buildings
        path = self.dlg.lineEdit_22.text()
        buildings = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_22.setText("Imported: " + str(buildings))
        print("affected b. imported: ", buildings)
        buildings = np.asarray(buildings, dtype='float64')
        
        buildings_restoration = 0;
    def import13_restoration(self):
        global buildings_restoration
        path = self.dlg.lineEdit_209.text()
        buildings_restoration = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_209.setText("Imported: " + str(buildings_restoration))
        print("affected b. imported: ", buildings_restoration)
        buildings_restoration = np.asarray(buildings_restoration, dtype='float64')
        
        land_use = 0;
    def import14(self):
        global land_use
        path = self.dlg.lineEdit_23.text()
        land_use = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_23.setText("Imported: " + str(land_use))
        print("land use imported: ", land_use)  
        land_use = np.asarray(land_use, dtype='float64')
        
        land_use_restoration = 0;
    def import14_restoration(self):
        global land_use_restoration
        path = self.dlg.lineEdit_211.text()
        land_use_restoration = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_211.setText("Imported: " + str(land_use_restoration))
        print("land use imported: ", land_use_restoration)  
        land_use_restoration = np.asarray(land_use_restoration, dtype='float64')
        
        v_tot = 0;
    def import16(self):
        global v_tot
        path = self.dlg.lineEdit_40.text()
        v_tot = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_40.setText("Imported: " + str(v_tot))
        print("v_tot imported: ", v_tot)
        
        v_tot_restoration = 0;
    def import16_restoration(self):
        global v_tot_restoration
        path = self.dlg.lineEdit_196.text()
        v_tot_restoration = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_196.setText("Imported: " + str(v_tot_restoration))
        print("v_tot imported: ", v_tot_restoration)
        
        v_RC = 0;
    def import17(self):
        global v_RC
        path = self.dlg.lineEdit_46.text()
        v_RC = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_46.setText("Imported: " + str(v_RC))
        print("v_RC imported: ", v_RC)
        
        v_RC_restoration = 0;
    def import17_restoration(self):
        global v_RC_restoration
        path = self.dlg.lineEdit_191.text()
        v_RC_restoration = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_191.setText("Imported: " + str(v_RC_restoration))
        print("v_RC imported: ", v_RC_restoration)
        
        tau_tot = 0;
    def import18(self):
        global tau_tot
        path = self.dlg.lineEdit_48.text()
        tau_tot = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_48.setText("Imported: " + str(tau_tot))
        print("tau_tot imported: ", tau_tot)
        
        tau_tot_restoration = 0;
    def import18_restoration(self):
        global tau_tot_restoration
        path = self.dlg.lineEdit_194.text()
        tau_tot_restoration = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_194.setText("Imported: " + str(tau_tot_restoration))
        print("tau_tot imported: ", tau_tot_restoration)
        
        tau_RC = 0;
    def import19(self):
        global tau_RC
        path = self.dlg.lineEdit_50.text()
        tau_RC = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_50.setText("Imported: " + str(tau_RC))
        print("tau_RC imported: ", tau_RC)
        
        tau_RC_restoration = 0;
    def import19_restoration(self):
        global tau_RC_restoration
        path = self.dlg.lineEdit_197.text()
        tau_RC_restoration = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_197.setText("Imported: " + str(tau_RC_restoration))
        print("tau_RC imported: ", tau_RC_restoration)

        area_protected = 0;
    def import20(self):
        global area_protected
        path = self.dlg.lineEdit_51.text()
        area_protected = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_51.setText("Imported: " + str(area_protected))
        print("Area_protected imported: ", area_protected)
        
        area_protected_restoration = 0;
    def import20_restoration(self):
        global area_protected_restoration
        path = self.dlg.lineEdit_205.text()
        area_protected_restoration = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_205.setText("Imported: " + str(area_protected_restoration))
        print("Area_protected imported: ", area_protected_restoration)

        vegetation_naturalness = 0;
    def import21(self):
        global vegetation_naturalness
        path = self.dlg.lineEdit_53.text()
        vegetation_naturalness = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_53.setText("Imported: " + str(vegetation_naturalness))
        print("Vegetation_naturalness imported: ", vegetation_naturalness)
        
        vegetation_naturalness_restoration = 0;
    def import21_restoration(self):
        global vegetation_naturalness_restoration
        path = self.dlg.lineEdit_207.text()
        vegetation_naturalness_restoration = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_207.setText("Imported: " + str(vegetation_naturalness_restoration))
        print("Vegetation_naturalness imported: ", vegetation_naturalness_restoration)

        water_level_dynamics = 0;
    def import22(self):
        global water_level_dynamics
        path = self.dlg.lineEdit_54.text()
        water_level_dynamics = np.asarray(path, dtype='float64')#float(input(path))
        self.dlg.lineEdit_54.setText("Imported: " + str(water_level_dynamics))
        print("Water_level_dynamics imported: ", water_level_dynamics)
        
        water_level_dynamics_restoration = 0;
    def import22_restoration(self):
        global water_level_dynamics_restoration
        path = self.dlg.lineEdit_202.text()
        water_level_dynamics_restoration = np.asarray(path, dtype='float64')#float(input(path))
        self.dlg.lineEdit_202.setText("Imported: " + str(water_level_dynamics_restoration))
        print("Water_level_dynamics imported: ", water_level_dynamics_restoration)
        
        potential_for_typical_habitats = 0;
    def import23(self):
        global potential_for_typical_habitats
        path = self.dlg.lineEdit_55.text()
        potential_for_typical_habitats = np.asarray(path, dtype='float64')#float(input(path))
        self.dlg.lineEdit_55.setText("Imported: " + str(potential_for_typical_habitats))
        print("Potential_for_typical_habitats imported: ", potential_for_typical_habitats)
        
        potential_for_typical_habitats_restoration = 0;
    def import23_restoration(self):
        global potential_for_typical_habitats_restoration
        path = self.dlg.lineEdit_204.text()
        potential_for_typical_habitats_restoration = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_204.setText("Imported: " + str(potential_for_typical_habitats_restoration))
        print("Potential_for_typical_habitats imported: ", potential_for_typical_habitats_restoration)
        
        area_floodplain = 0;
    def import24(self):
        global area_floodplain
        path = self.dlg.lineEdit_32.text()
        area_floodplain = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_32.setText("Imported: " + str(area_floodplain))
        print("Area_floodplain imported: ", area_floodplain)

        ecological_water_body_status = 0;
    def import25(self):
        global ecological_water_body_status
        path = self.dlg.lineEdit_49.text()
        ecological_water_body_status = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_49.setText("Imported: " + str(ecological_water_body_status))
        print("Ecological_water_body_status imported: ", ecological_water_body_status)
        
        ecological_water_body_status_restoration = 0;
    def import25_restoration(self):
        global ecological_water_body_status_restoration
        path = self.dlg.lineEdit_203.text()
        ecological_water_body_status_restoration = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_203.setText("Imported: " + str(ecological_water_body_status_restoration))
        print("Ecological_water_body_status imported: ", ecological_water_body_status_restoration)
        
        presence_of_documented_planning_interests = 0;
    def import26(self):
        global presence_of_documented_planning_interests
        path = self.dlg.lineEdit_58.text()
        presence_of_documented_planning_interests = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_58.setText("Imported: " + str(presence_of_documented_planning_interests))
        print("Presence_of_documented_planning_interests imported: ", presence_of_documented_planning_interests)
        
        presence_of_documented_planning_interests_restoration = 0;
    def import26_restoration(self):
        global presence_of_documented_planning_interests_restoration
        path = self.dlg.lineEdit_213.text()
        presence_of_documented_planning_interests_restoration = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_213.setText("Imported: " + str(presence_of_documented_planning_interests_restoration))
        print("Presence_of_documented_planning_interests imported: ", presence_of_documented_planning_interests_restoration)
        
        #extended_cost_benefit_analysis = 0;
    #def import27(self):
        #global extended_cost_benefit_analysis
        #path = self.dlg.lineEdit_60.text()
        #extended_cost_benefit_analysis = np.asarray(path, dtype='float64')
        #self.dlg.lineEdit_60.setText("Imported: " + str(extended_cost_benefit_analysis))
        #print("Extended_cost_benefit_analysis imported: ", extended_cost_benefit_analysis)
        
        extended_cost_benefit_analysis_restoration = 0;
    def import27_restoration(self):
        global extended_cost_benefit_analysis_restoration
        path = self.dlg.lineEdit_214.text()
        extended_cost_benefit_analysis_restoration = np.asarray(path, dtype='float64')
        self.dlg.lineEdit_214.setText("Imported: " + str(extended_cost_benefit_analysis_restoration))
        print("Extended_cost_benefit_analysis imported: ", extended_cost_benefit_analysis_restoration)
        
        parameter_invasive_species = 0;
    def import28(self):
        global parameter_invasive_species
        path = self.dlg.lineEdit_57.text()
        parameter_invasive_species = np.asarray(path, dtype='float64')#float(input(path))
        self.dlg.lineEdit_57.setText("Imported: " + str(parameter_invasive_species))
        print("Parameter_invasive_species imported: ", parameter_invasive_species)
        
        parameter_invasive_species_restoration = 0;
    def import28_restoration(self):
        global parameter_invasive_species_restoration
        path = self.dlg.lineEdit_208.text()
        parameter_invasive_species_restoration = np.asarray(path, dtype='float64')#float(input(path))
        self.dlg.lineEdit_208.setText("Imported: " + str(parameter_invasive_species_restoration))
        print("Parameter_invasive_species imported: ", parameter_invasive_species_restoration)
        
    #    number_of_identified_fp = 0;
    #def select_fp(self):
    #    global number_of_identified_fp
    #    path = self.dlg.lineEdit_44.text()
    #    #number_of_identified_fp = np.asarray(path, dtype='i')
    #    #self.dlg.lineEdit_41.setText("Nr of identified fp: " + str(number_of_identified_fp))
    #    floodplain_index = self.dlg.comboBox.currentIndex()
    #    floodplain_index = np.array((floodplain_index+1))
    #    print(floodplain_index)
        
    def confirm_values(self):
        self.dlg.lineEdit_122.setText(str(Delta_Qrelative))
        self.dlg.lineEdit_134.setText(str(Delta_T))
        self.dlg.lineEdit_142.setText(str(Delta_h))
        self.dlg.lineEdit_136.setText(str(c_fwb))
        self.dlg.lineEdit_129.setText(str(protected_species))
        self.dlg.lineEdit_145.setText(str(buildings))
        self.dlg.lineEdit_121.setText(str(land_use))
        
    def confirm_values_restoration(self):
        self.dlg.lineEdit_597.setText(str(Delta_Qrelative_restoration))
        self.dlg.lineEdit_601.setText(str(Delta_T_restoration))
        self.dlg.lineEdit_604.setText(str(Delta_h_restoration))
        self.dlg.lineEdit_609.setText(str(c_fwb_restoration))
        self.dlg.lineEdit_599.setText(str(protected_species_restoration))
        self.dlg.lineEdit_613.setText(str(buildings_restoration))
        self.dlg.lineEdit_600.setText(str(land_use_restoration))
        
    def confirm_extra_values(self):
        self.dlg.lineEdit_137.setText(str(Delta_v))
        self.dlg.lineEdit_150.setText(str(Delta_tau))
        self.dlg.lineEdit_157.setText(str(protected_habitat))
        self.dlg.lineEdit_149.setText(str(vegetation_naturalness))
        self.dlg.lineEdit_143.setText(str(water_level_dynamics))
        self.dlg.lineEdit_152.setText(str(potential_for_typical_habitats))
        self.dlg.lineEdit_138.setText(str(ecological_water_body_status))   
        self.dlg.lineEdit_158.setText(str(parameter_invasive_species)) 
        self.dlg.lineEdit_160.setText(str(presence_of_documented_planning_interests)) 
        #self.dlg.lineEdit_162.setText(str(extended_cost_benefit_analysis))
        
    def confirm_extra_values_restoration(self):
        self.dlg.lineEdit_619.setText(str(Delta_v_restoration))
        self.dlg.lineEdit_628.setText(str(Delta_tau_restoration))
        self.dlg.lineEdit_620.setText(str(protected_habitat_restoration))
        self.dlg.lineEdit_627.setText(str(vegetation_naturalness_restoration))
        self.dlg.lineEdit_616.setText(str(water_level_dynamics_restoration))
        self.dlg.lineEdit_632.setText(str(potential_for_typical_habitats_restoration))
        self.dlg.lineEdit_631.setText(str(ecological_water_body_status_restoration))   
        self.dlg.lineEdit_634.setText(str(parameter_invasive_species_restoration)) 
        self.dlg.lineEdit_635.setText(str(presence_of_documented_planning_interests_restoration)) 
        self.dlg.lineEdit_636.setText(str(extended_cost_benefit_analysis_restoration))
        
    def restoration_decision(self):
        path_Delta_Qrelative = self.dlg.lineEdit_131.text()
        FEM_Delta_Qrelative = np.asarray(path_Delta_Qrelative, dtype='float64')
        self.dlg.lineEdit_361.setText(str(FEM_Delta_Qrelative))
        path_Delta_T = self.dlg.lineEdit_128.text()
        FEM_Delta_T = np.asarray(path_Delta_T, dtype='float64')
        self.dlg.lineEdit_358.setText(str(FEM_Delta_T))
        path_Delta_h = self.dlg.lineEdit_140.text()
        FEM_Delta_h = np.asarray(path_Delta_h, dtype='float64')
        self.dlg.lineEdit_347.setText(str(FEM_Delta_h))
        path_Delta_c_fwb = self.dlg.lineEdit_139.text()
        FEM_Delta_c_fwb = np.asarray(path_Delta_c_fwb, dtype='float64')
        self.dlg.lineEdit_360.setText(str(FEM_Delta_c_fwb))
        path_Delta_protected_species = self.dlg.lineEdit_119.text()
        FEM_Delta_protected_species = np.asarray(path_Delta_protected_species, dtype='float64')
        self.dlg.lineEdit_353.setText(str(FEM_Delta_protected_species))
        path_Delta_buildings = self.dlg.lineEdit_124.text()
        FEM_Delta_buildings = np.asarray(path_Delta_buildings, dtype='float64')
        self.dlg.lineEdit_351.setText(str(FEM_Delta_buildings))
        path_Delta_land_use = self.dlg.lineEdit_147.text()
        FEM_Delta_land_use = np.asarray(path_Delta_land_use, dtype='float64')
        self.dlg.lineEdit_346.setText(str(FEM_Delta_land_use))

        path_Delta_Qrelative_restoration = self.dlg.lineEdit_605.text()
        FEM_Delta_Qrelative_restoration = np.asarray(path_Delta_Qrelative_restoration, dtype='float64')
        self.dlg.lineEdit_216.setText(str(FEM_Delta_Qrelative_restoration))
        path_Delta_T_restoration = self.dlg.lineEdit_598.text()
        FEM_Delta_T_restoration = np.asarray(path_Delta_T_restoration, dtype='float64')
        self.dlg.lineEdit_217.setText(str(FEM_Delta_T_restoration))
        path_Delta_h_restoration = self.dlg.lineEdit_611.text()
        FEM_Delta_h_restoration = np.asarray(path_Delta_h_restoration, dtype='float64')
        self.dlg.lineEdit_218.setText(str(FEM_Delta_h_restoration))
        path_Delta_c_fwb_restoration = self.dlg.lineEdit_608.text()
        FEM_Delta_c_fwb_restoration = np.asarray(path_Delta_c_fwb_restoration, dtype='float64')
        self.dlg.lineEdit_219.setText(str(FEM_Delta_c_fwb_restoration))
        path_Delta_protected_species_restoration = self.dlg.lineEdit_606.text()
        FEM_Delta_protected_species_restoration = np.asarray(path_Delta_protected_species_restoration, dtype='float64')
        self.dlg.lineEdit_220.setText(str(FEM_Delta_protected_species_restoration))
        path_Delta_buildings_restoration = self.dlg.lineEdit_602.text()
        FEM_Delta_buildings_restoration = np.asarray(path_Delta_buildings_restoration, dtype='float64')
        self.dlg.lineEdit_221.setText(str(FEM_Delta_buildings_restoration))
        path_Delta_land_use_restoration = self.dlg.lineEdit_612.text()
        FEM_Delta_land_use_restoration = np.asarray(path_Delta_land_use_restoration, dtype='float64')
        self.dlg.lineEdit_222.setText(str(FEM_Delta_land_use_restoration))
        if FEM_Delta_Qrelative < FEM_Delta_Qrelative_restoration or FEM_Delta_T < FEM_Delta_T_restoration or FEM_Delta_h < FEM_Delta_h_restoration or FEM_Delta_c_fwb < FEM_Delta_c_fwb_restoration or FEM_Delta_protected_species < FEM_Delta_protected_species_restoration or FEM_Delta_buildings < FEM_Delta_buildings_restoration or FEM_Delta_land_use < FEM_Delta_land_use_restoration:
        	self.dlg.lineEdit_224.setText("Yes")
        	print("Yes")
        else:
        	self.dlg.lineEdit_224.setText("No")
        	print("No")


    def load_AFP_defaults(self):
        dist_b_fp = 5000;
        river_width = 1100;
        no_points = 5;
        ratio_f = 1;        
        self.dlg.lineEdit_30.setText(str(dist_b_fp))
        self.dlg.lineEdit_29.setText(str(river_width))
        self.dlg.lineEdit_24.setText(str(no_points))
        self.dlg.lineEdit_33.setText(str(ratio_f))
        self.dlg.lineEdit_76.setText("Default Values Loaded")     
    
    def load_treshold_defaults(self):
        threshold_delta_q_relative_low = 1;
        threshold_delta_q_relative_medium = 2;
        threshold_delta_q_relative_high = 2;
        treshold_f_w_t_deltaT_low = 1;
        treshold_f_w_t_deltaT_medium = 5;
        treshold_f_w_t_deltaT_high = 5;
        treshold_water_level_change_low = 0.1;
        treshold_water_level_change_medium = 0.5;
        treshold_water_level_change_high = 0.5;
        treshold_c_fp_w_b_low = 1;
        treshold_c_fp_w_b_medium = 3;
        treshold_c_fp_w_b_high = 5;
        treshold_existence_p_s_low = 1;
        treshold_existence_p_s_medium = 40;
        treshold_existence_p_s_high = 40;
        treshold_potentially_a_b_low = 1;
        treshold_potentially_a_b_medium = 5;
        treshold_potentially_a_b_high = 5;
        treshold_land_use_low = 2;
        treshold_land_use_medium = 4;
        treshold_land_use_high = 4;
        treshold_sediment_balance_low = 0.33;
        treshold_sediment_balance_medium = 0.66;
        treshold_sediment_balance_high = 0.66;
        #treshold_con_fp_w_b_low = 15;
        #treshold_con_fp_w_b_medium = 50;
        #treshold_con_fp_w_b_high = 50;
        #treshold_con_fp_w_b_detailed_low = 5;
        #treshold_con_fp_w_b_detailed_medium = 30;
        #treshold_con_fp_w_b_detailed_high = 30;
        treshold_w_l_d_low = 1;
        treshold_w_l_d_medium = 3;
        treshold_w_l_d_high = 5;
        #treshold_c_b_r_low = 0.5;
        #treshold_c_b_r_medium = 1;
        #treshold_c_b_r_high = 1;
        FEM_Delta_Qrelative = 0;
        FEM_Delta_T = 0;
        FEM_Delta_h = 0;
        FEM_c_fwb = 0;
        FEM_protected_species = 0;
        FEM_buildings = 0;
        FEM_land_use = 0;
        
        self.dlg.lineEdit_92.setText(str(threshold_delta_q_relative_low))
        self.dlg.lineEdit_90.setText(str(threshold_delta_q_relative_medium))
        self.dlg.lineEdit_110.setText(str(threshold_delta_q_relative_high))
        self.dlg.lineEdit_95.setText(str(treshold_f_w_t_deltaT_low))
        self.dlg.lineEdit_106.setText(str(treshold_f_w_t_deltaT_medium))
        self.dlg.lineEdit_89.setText(str(treshold_f_w_t_deltaT_high))
        self.dlg.lineEdit_105.setText(str(treshold_water_level_change_low))
        self.dlg.lineEdit_88.setText(str(treshold_water_level_change_medium))
        self.dlg.lineEdit_109.setText(str(treshold_water_level_change_high))
        self.dlg.lineEdit_78.setText(str(treshold_c_fp_w_b_low))
        self.dlg.lineEdit_93.setText(str(treshold_c_fp_w_b_medium))
        self.dlg.lineEdit_104.setText(str(treshold_c_fp_w_b_high))
        self.dlg.lineEdit_86.setText(str(treshold_existence_p_s_low))
        self.dlg.lineEdit_100.setText(str(treshold_existence_p_s_medium))
        self.dlg.lineEdit_81.setText(str(treshold_existence_p_s_high))
        self.dlg.lineEdit_97.setText(str(treshold_potentially_a_b_low))
        self.dlg.lineEdit_107.setText(str(treshold_potentially_a_b_medium))
        self.dlg.lineEdit_103.setText(str(treshold_potentially_a_b_high))   
        self.dlg.lineEdit_91.setText(str(treshold_land_use_low))
        self.dlg.lineEdit_85.setText(str(treshold_land_use_medium))
        self.dlg.lineEdit_82.setText(str(treshold_land_use_high))     
        self.dlg.lineEdit_84.setText(str(treshold_sediment_balance_low))
        self.dlg.lineEdit_102.setText(str(treshold_sediment_balance_medium))
        self.dlg.lineEdit_79.setText(str(treshold_sediment_balance_high))    
        #self.dlg.lineEdit_108.setText(str(treshold_con_fp_w_b_low))
        #self.dlg.lineEdit_80.setText(str(treshold_con_fp_w_b_medium))
        #self.dlg.lineEdit_101.setText(str(treshold_con_fp_w_b_high))      
        #self.dlg.lineEdit_96.setText(str(treshold_con_fp_w_b_detailed_low))
        #self.dlg.lineEdit_83.setText(str(treshold_con_fp_w_b_detailed_medium))
        #self.dlg.lineEdit_99.setText(str(treshold_con_fp_w_b_detailed_high))  
        self.dlg.lineEdit_98.setText(str(treshold_w_l_d_low))
        self.dlg.lineEdit_87.setText(str(treshold_w_l_d_medium))
        self.dlg.lineEdit_94.setText(str(treshold_w_l_d_high))
        #self.dlg.lineEdit_111.setText(str(treshold_c_b_r_low))
        #self.dlg.lineEdit_112.setText(str(treshold_c_b_r_medium))
        #self.dlg.lineEdit_113.setText(str(treshold_c_b_r_high))
        
    def load_extra_treshold_defaults(self):
        threshold_delta_v_low = 0.1;
        threshold_delta_v_medium = 0.2;
        threshold_delta_v_high = 0.2;
        threshold_delta_tau_low = 1.5;
        threshold_delta_tau_medium = 3;
        threshold_delta_tau_high = 3;
        threshold_protected_habitat_low = 33;
        threshold_protected_habitat_medium = 66;
        threshold_protected_habitat_high = 66;
        threshold_vegetation_naturalness_low = 3.7;
        threshold_vegetation_naturalness_medium = 6.01;
        threshold_vegetation_naturalness_high = 6.01;
        threshold_water_level_dynamics_low = 1;
        threshold_water_level_dynamics_medium = 3;
        threshold_water_level_dynamics_high = 5;
        threshold_p_t_habitat_low = 5;
        threshold_p_t_habitat_medium = 10;
        threshold_p_t_habitat_high = 10;
        threshold_water_b_status_low = 1;
        threshold_water_b_status_medium = 3;
        threshold_water_b_status_high = 5;
        threshold_invasive_species_low = 1;
        threshold_invasive_species_medium = 3;
        threshold_invasive_species_high = 5;
        threshold_doc_interests_low = 2;
        threshold_doc_interests_medium = 4;
        threshold_doc_interests_high = 4;
        threshold_cost_ben_fac_low = 1;
        threshold_cost_ben_fac_medium = 3;
        threshold_cost_ben_fac_high = 5;

        self.dlg.lineEdit_114.setText(str(threshold_delta_v_low))
        self.dlg.lineEdit_115.setText(str(threshold_delta_v_medium))
        self.dlg.lineEdit_116.setText(str(threshold_delta_v_high))
        self.dlg.lineEdit_41.setText(str(threshold_delta_tau_low))
        self.dlg.lineEdit_42.setText(str(threshold_delta_tau_medium))
        self.dlg.lineEdit_43.setText(str(threshold_delta_tau_high))
        self.dlg.lineEdit_44.setText(str(threshold_protected_habitat_low))
        self.dlg.lineEdit_61.setText(str(threshold_protected_habitat_medium))
        self.dlg.lineEdit_62.setText(str(threshold_protected_habitat_high))
        self.dlg.lineEdit_63.setText(str(threshold_vegetation_naturalness_low))
        self.dlg.lineEdit_64.setText(str(threshold_vegetation_naturalness_medium))
        self.dlg.lineEdit_65.setText(str(threshold_vegetation_naturalness_high))
        self.dlg.lineEdit_66.setText(str(threshold_water_level_dynamics_low))
        self.dlg.lineEdit_67.setText(str(threshold_water_level_dynamics_medium))
        self.dlg.lineEdit_68.setText(str(threshold_water_level_dynamics_high))
        self.dlg.lineEdit_69.setText(str(threshold_p_t_habitat_low))
        self.dlg.lineEdit_70.setText(str(threshold_p_t_habitat_medium))
        self.dlg.lineEdit_71.setText(str(threshold_p_t_habitat_high))
        self.dlg.lineEdit_72.setText(str(threshold_water_b_status_low))
        self.dlg.lineEdit_73.setText(str(threshold_water_b_status_medium))
        self.dlg.lineEdit_74.setText(str(threshold_water_b_status_high))
        self.dlg.lineEdit_117.setText(str(threshold_invasive_species_low))
        self.dlg.lineEdit_118.setText(str(threshold_invasive_species_medium))
        self.dlg.lineEdit_120.setText(str(threshold_invasive_species_high))
        self.dlg.lineEdit_123.setText(str(threshold_doc_interests_low))
        self.dlg.lineEdit_125.setText(str(threshold_doc_interests_medium))
        self.dlg.lineEdit_126.setText(str(threshold_doc_interests_high))
        self.dlg.lineEdit_127.setText(str(threshold_cost_ben_fac_low))
        self.dlg.lineEdit_130.setText(str(threshold_cost_ben_fac_medium))
        self.dlg.lineEdit_132.setText(str(threshold_cost_ben_fac_high))

    def calculate_FEM(self):
        path_threshold_delta_q_relative_low = self.dlg.lineEdit_92.text()
        threshold_delta_q_relative_low = np.asarray(path_threshold_delta_q_relative_low, dtype='float64')#float(input(path))
        path_threshold_delta_q_relative_medium = self.dlg.lineEdit_90.text()
        threshold_delta_q_relative_medium = np.asarray(path_threshold_delta_q_relative_medium, dtype='float64')#float(input(path))
        path_threshold_delta_q_relative_high = self.dlg.lineEdit_110.text()
        threshold_delta_q_relative_high = np.asarray(path_threshold_delta_q_relative_high, dtype='float64')#float(input(path))
        if Delta_Qrelative < threshold_delta_q_relative_low:
        	self.dlg.lineEdit_131.setText("1")
        	FEM_Delta_Qrelative = 1
        	print(FEM_Delta_Qrelative)
        elif Delta_Qrelative > threshold_delta_q_relative_high:
        	self.dlg.lineEdit_131.setText("5")
        	FEM_Delta_Qrelative = 5
        	print(FEM_Delta_Qrelative)
        else: #Delta_Qrelative >= threshold_delta_q_relative_low and Delta_Qrelative < threshold_delta_q_relative_medium:
        	self.dlg.lineEdit_131.setText("3")
        	FEM_Delta_Qrelative = 3
        	print(FEM_Delta_Qrelative)
        path_treshold_f_w_t_deltaT_low = self.dlg.lineEdit_95.text()
        treshold_f_w_t_deltaT_low = np.asarray(path_treshold_f_w_t_deltaT_low, dtype='float64')#float(input(path))
        path_treshold_f_w_t_deltaT_medium = self.dlg.lineEdit_106.text()
        treshold_f_w_t_deltaT_medium = np.asarray(path_treshold_f_w_t_deltaT_medium, dtype='float64')#float(input(path))
        path_treshold_f_w_t_deltaT_high = self.dlg.lineEdit_89.text()
        treshold_f_w_t_deltaT_high = np.asarray(path_treshold_f_w_t_deltaT_high, dtype='float64')#float(input(path))
        if Delta_T < treshold_f_w_t_deltaT_low:
        	self.dlg.lineEdit_128.setText("1")
        	FEM_Delta_T = 1
        	print(FEM_Delta_T)
        elif Delta_T > treshold_f_w_t_deltaT_high:
        	self.dlg.lineEdit_128.setText("5")
        	FEM_Delta_T = 5
        	print(FEM_Delta_T)
        else:
        	self.dlg.lineEdit_128.setText("3")
        	FEM_Delta_T = 3
        	print(FEM_Delta_T)
        path_treshold_water_level_change_low = self.dlg.lineEdit_105.text()
        treshold_water_level_change_low = np.asarray(path_treshold_water_level_change_low, dtype='float64')#float(input(path))
        path_treshold_water_level_change_medium = self.dlg.lineEdit_88.text()
        treshold_water_level_change_medium = np.asarray(path_treshold_water_level_change_medium, dtype='float64')#float(input(path))
        path_treshold_water_level_change_high = self.dlg.lineEdit_109.text()
        treshold_water_level_change_high = np.asarray(path_treshold_water_level_change_high, dtype='float64')#float(input(path))
        if Delta_h < treshold_f_w_t_deltaT_low:
        	self.dlg.lineEdit_140.setText("1")
        	FEM_Delta_h = 1
        	print(FEM_Delta_h)
        elif Delta_h > treshold_f_w_t_deltaT_high:
        	self.dlg.lineEdit_140.setText("5")
        	FEM_Delta_h = 5
        	print(FEM_Delta_h)
        else:
        	self.dlg.lineEdit_140.setText("3")
        	FEM_Delta_h = 3
        	print(FEM_Delta_h)
        path_treshold_c_fp_w_b_low = self.dlg.lineEdit_78.text()
        treshold_c_fp_w_b_low = np.asarray(path_treshold_c_fp_w_b_low, dtype='float64')#float(input(path))
        path_treshold_c_fp_w_b_medium = self.dlg.lineEdit_93.text()
        treshold_c_fp_w_b_medium = np.asarray(path_treshold_c_fp_w_b_medium, dtype='float64')#float(input(path))
        path_treshold_c_fp_w_b_high = self.dlg.lineEdit_104.text()
        treshold_c_fp_w_b_high = np.asarray(path_treshold_c_fp_w_b_high, dtype='float64')#float(input(path))
        if c_fwb < treshold_c_fp_w_b_low:
        	self.dlg.lineEdit_139.setText("1")
        	FEM_c_fwb = 1
        	print(FEM_c_fwb)
        elif c_fwb > treshold_c_fp_w_b_high:
        	self.dlg.lineEdit_139.setText("5")
        	FEM_c_fwb = 5
        	print(FEM_c_fwb)
        else:
        	self.dlg.lineEdit_139.setText("3")
        	FEM_c_fwb = 3
        	print(FEM_c_fwb)
        path_treshold_existence_p_s_low = self.dlg.lineEdit_86.text()
        treshold_existence_p_s_low = np.asarray(path_treshold_existence_p_s_low, dtype='float64')#float(input(path))
        path_treshold_existence_p_s_medium = self.dlg.lineEdit_100.text()
        treshold_existence_p_s_medium = np.asarray(path_treshold_existence_p_s_medium, dtype='float64')#float(input(path))
        path_treshold_existence_p_s_high = self.dlg.lineEdit_81.text()
        treshold_existence_p_s_high = np.asarray(path_treshold_existence_p_s_high, dtype='float64')#float(input(path))
        if protected_species < treshold_existence_p_s_low:
        	self.dlg.lineEdit_119.setText("1")
        	FEM_protected_species = 1
        	print(FEM_protected_species)
        elif protected_species > treshold_existence_p_s_high:
        	self.dlg.lineEdit_119.setText("5")
        	FEM_protected_species = 5
        	print(FEM_protected_species)
        else:
        	self.dlg.lineEdit_119.setText("3")
        	FEM_protected_species = 3
        	print(FEM_protected_species)
        path_treshold_potentially_a_b_low = self.dlg.lineEdit_97.text()
        treshold_potentially_a_b_low = np.asarray(path_treshold_potentially_a_b_low, dtype='float64')#float(input(path))
        path_treshold_potentially_a_b_medium = self.dlg.lineEdit_107.text()
        treshold_potentially_a_b_medium = np.asarray(path_treshold_potentially_a_b_medium, dtype='float64')#float(input(path))
        path_treshold_potentially_a_b_high = self.dlg.lineEdit_103.text()
        treshold_potentially_a_b_high = np.asarray(path_treshold_potentially_a_b_high, dtype='float64')#float(input(path))
        if buildings > treshold_potentially_a_b_high:
        	self.dlg.lineEdit_124.setText("1")
        	FEM_buildings = 1
        	print(FEM_buildings)
        elif buildings < treshold_potentially_a_b_low:
        	self.dlg.lineEdit_124.setText("5")
        	FEM_buildings = 5
        	print(FEM_buildings)
        else:
        	self.dlg.lineEdit_124.setText("3")
        	FEM_buildings = 3
        	print(FEM_buildings)
        path_treshold_land_use_low = self.dlg.lineEdit_91.text()
        treshold_land_use_low = np.asarray(path_treshold_land_use_low, dtype='float64')#float(input(path))
        path_treshold_land_use_medium = self.dlg.lineEdit_85.text()
        treshold_land_use_medium = np.asarray(path_treshold_land_use_medium, dtype='float64')#float(input(path))
        path_treshold_land_use_high = self.dlg.lineEdit_82.text()
        treshold_land_use_high = np.asarray(path_treshold_land_use_high, dtype='float64')#float(input(path))
        if land_use < treshold_land_use_low:
        	self.dlg.lineEdit_147.setText("1")
        	FEM_land_use = 1
        	print(FEM_land_use)
        elif land_use > treshold_land_use_high:
        	self.dlg.lineEdit_147.setText("5")
        	FEM_land_use = 5
        	print(FEM_land_use)
        else:
        	self.dlg.lineEdit_147.setText("3")
        	FEM_land_use = 3
        	print(FEM_land_use)
        	
        FEM_sum = FEM_Delta_Qrelative + FEM_Delta_T + FEM_Delta_h + FEM_c_fwb + FEM_protected_species + FEM_buildings + FEM_land_use
        print(FEM_sum)
        self.dlg.lineEdit_133.setText(str(FEM_sum))
        if FEM_sum >= 27:
        	self.dlg.lineEdit_135.setText("Low Demand")
        	print("Low Demand")
        elif FEM_sum < 23:
        	self.dlg.lineEdit_135.setText("High Demand")
        	print("High Demand")
        else:
        	self.dlg.lineEdit_135.setText("Medium Demand")
        	print("Medium Demand")
        path_treshold_sediment_balance_low = self.dlg.lineEdit_84.text()
        treshold_sediment_balance_low = np.asarray(path_treshold_sediment_balance_low, dtype='float64')#float(input(path))
        path_treshold_sediment_balance_medium = self.dlg.lineEdit_102.text()
        treshold_sediment_balance_medium = np.asarray(path_treshold_sediment_balance_medium, dtype='float64')#float(input(path))
        path_treshold_sediment_balance_high = self.dlg.lineEdit_79.text()
        treshold_sediment_balance_high = np.asarray(path_treshold_sediment_balance_high, dtype='float64')#float(input(path))
        #path_treshold_con_fp_w_b_low = self.dlg.lineEdit_108.text()
        #treshold_con_fp_w_b_low = np.asarray(path_treshold_con_fp_w_b_low, dtype='float64')#float(input(path))
        #path_treshold_con_fp_w_b_medium = self.dlg.lineEdit_80.text()
        #treshold_con_fp_w_b_medium = np.asarray(path_treshold_con_fp_w_b_medium, dtype='float64')#float(input(path))
        #path_treshold_con_fp_w_b_high = self.dlg.lineEdit_101.text()
        #treshold_con_fp_w_b_high = np.asarray(path_treshold_con_fp_w_b_high, dtype='float64')#float(input(path))
        #path_treshold_con_fp_w_b_detailed_low = self.dlg.lineEdit_96.text()
        #treshold_con_fp_w_b_detailed_low = np.asarray(path_treshold_con_fp_w_b_detailed_low, dtype='float64')#float(input(path))
        #path_treshold_con_fp_w_b_detailed_medium = self.dlg.lineEdit_83.text()
        #treshold_con_fp_w_b_detailed_medium = np.asarray(path_treshold_con_fp_w_b_detailed_medium, dtype='float64')#float(input(path))
        #path_treshold_con_fp_w_b_detailed_high = self.dlg.lineEdit_99.text()
        #treshold_con_fp_w_b_detailed_high = np.asarray(path_treshold_con_fp_w_b_detailed_high, dtype='float64')#float(input(path))
        path_treshold_w_l_d_low = self.dlg.lineEdit_98.text()
        treshold_w_l_d_low = np.asarray(path_treshold_w_l_d_low, dtype='float64')#float(input(path))
        path_treshold_w_l_d_medium = self.dlg.lineEdit_87.text()
        treshold_w_l_d_medium = np.asarray(path_treshold_w_l_d_medium, dtype='float64')#float(input(path))
        path_treshold_w_l_d_high = self.dlg.lineEdit_94.text()
        treshold_w_l_d_high = np.asarray(path_treshold_w_l_d_high, dtype='float64')#float(input(path))
        #path_treshold_c_b_r_low = self.dlg.lineEdit_111.text()
        #treshold_c_b_r_low = np.asarray(path_treshold_c_b_r_low, dtype='float64')#float(input(path))
        #path_treshold_c_b_r_medium = self.dlg.lineEdit_112.text()
        #treshold_c_b_r_medium = np.asarray(path_treshold_c_b_r_medium, dtype='float64')#float(input(path))
        #path_treshold_c_b_r_high = self.dlg.lineEdit_113.text()
        #treshold_c_b_r_high = np.asarray(path_treshold_c_b_r_high, dtype='float64')#float(input(path))
        if FEM_Delta_Qrelative == 5 or FEM_Delta_T == 5 or FEM_Delta_h == 5 or FEM_c_fwb == 5 or FEM_protected_species == 5 or FEM_buildings == 5 or FEM_land_use == 5:
        	self.dlg.lineEdit_175.setText("Yes")
        	print("Need for Restoration:  Yes")
        else:
        	self.dlg.lineEdit_175.setText("No")
        	print("Need for Restoration:  No")
        
    def calculate_FEM_restoration(self):
        path_threshold_delta_q_relative_low = self.dlg.lineEdit_92.text()
        threshold_delta_q_relative_low = np.asarray(path_threshold_delta_q_relative_low, dtype='float64')#float(input(path))
        path_threshold_delta_q_relative_medium = self.dlg.lineEdit_90.text()
        threshold_delta_q_relative_medium = np.asarray(path_threshold_delta_q_relative_medium, dtype='float64')#float(input(path))
        path_threshold_delta_q_relative_high = self.dlg.lineEdit_110.text()
        threshold_delta_q_relative_high = np.asarray(path_threshold_delta_q_relative_high, dtype='float64')#float(input(path))
        if Delta_Qrelative_restoration < threshold_delta_q_relative_low:
        	self.dlg.lineEdit_605.setText("1")
        	FEM_Delta_Qrelative_restoration = 1
        	print(FEM_Delta_Qrelative_restoration)
        elif Delta_Qrelative_restoration > threshold_delta_q_relative_high:
        	self.dlg.lineEdit_605.setText("5")
        	FEM_Delta_Qrelative_restoration = 5
        	print(FEM_Delta_Qrelative_restoration)
        else: #Delta_Qrelative >= threshold_delta_q_relative_low and Delta_Qrelative < threshold_delta_q_relative_medium:
        	self.dlg.lineEdit_605.setText("3")
        	FEM_Delta_Qrelative_restoration = 3
        	print(FEM_Delta_Qrelative_restoration)
        path_treshold_f_w_t_deltaT_low = self.dlg.lineEdit_95.text()
        treshold_f_w_t_deltaT_low = np.asarray(path_treshold_f_w_t_deltaT_low, dtype='float64')#float(input(path))
        path_treshold_f_w_t_deltaT_medium = self.dlg.lineEdit_106.text()
        treshold_f_w_t_deltaT_medium = np.asarray(path_treshold_f_w_t_deltaT_medium, dtype='float64')#float(input(path))
        path_treshold_f_w_t_deltaT_high = self.dlg.lineEdit_89.text()
        treshold_f_w_t_deltaT_high = np.asarray(path_treshold_f_w_t_deltaT_high, dtype='float64')#float(input(path))
        if Delta_T_restoration < treshold_f_w_t_deltaT_low:
        	self.dlg.lineEdit_598.setText("1")
        	FEM_Delta_T_restoration = 1
        	print(FEM_Delta_T_restoration)
        elif Delta_T_restoration > treshold_f_w_t_deltaT_high:
        	self.dlg.lineEdit_598.setText("5")
        	FEM_Delta_T_restoration = 5
        	print(FEM_Delta_T_restoration)
        else:
        	self.dlg.lineEdit_598.setText("3")
        	FEM_Delta_T_restoration = 3
        	print(FEM_Delta_T_restoration)
        path_treshold_water_level_change_low = self.dlg.lineEdit_105.text()
        treshold_water_level_change_low = np.asarray(path_treshold_water_level_change_low, dtype='float64')#float(input(path))
        path_treshold_water_level_change_medium = self.dlg.lineEdit_88.text()
        treshold_water_level_change_medium = np.asarray(path_treshold_water_level_change_medium, dtype='float64')#float(input(path))
        path_treshold_water_level_change_high = self.dlg.lineEdit_109.text()
        treshold_water_level_change_high = np.asarray(path_treshold_water_level_change_high, dtype='float64')#float(input(path))
        if Delta_h_restoration < treshold_f_w_t_deltaT_low:
        	self.dlg.lineEdit_611.setText("1")
        	FEM_Delta_h_restoration = 1
        	print(FEM_Delta_h_restoration)
        elif Delta_h_restoration > treshold_f_w_t_deltaT_high:
        	self.dlg.lineEdit_611.setText("5")
        	FEM_Delta_h_restoration = 5
        	print(FEM_Delta_h_restoration)
        else:
        	self.dlg.lineEdit_611.setText("3")
        	FEM_Delta_h_restoration = 3
        	print(FEM_Delta_h_restoration)
        path_treshold_c_fp_w_b_low = self.dlg.lineEdit_78.text()
        treshold_c_fp_w_b_low = np.asarray(path_treshold_c_fp_w_b_low, dtype='float64')#float(input(path))
        path_treshold_c_fp_w_b_medium = self.dlg.lineEdit_93.text()
        treshold_c_fp_w_b_medium = np.asarray(path_treshold_c_fp_w_b_medium, dtype='float64')#float(input(path))
        path_treshold_c_fp_w_b_high = self.dlg.lineEdit_104.text()
        treshold_c_fp_w_b_high = np.asarray(path_treshold_c_fp_w_b_high, dtype='float64')#float(input(path))
        if c_fwb_restoration < treshold_c_fp_w_b_low:
        	self.dlg.lineEdit_608.setText("1")
        	FEM_c_fwb_restoration = 1
        	print(FEM_c_fwb_restoration)
        elif c_fwb_restoration > treshold_c_fp_w_b_high:
        	self.dlg.lineEdit_608.setText("5")
        	FEM_c_fwb_restoration = 5
        	print(FEM_c_fwb_restoration)
        else:
        	self.dlg.lineEdit_608.setText("3")
        	FEM_c_fwb_restoration = 3
        	print(FEM_c_fwb_restoration)
        path_treshold_existence_p_s_low = self.dlg.lineEdit_86.text()
        treshold_existence_p_s_low = np.asarray(path_treshold_existence_p_s_low, dtype='float64')#float(input(path))
        path_treshold_existence_p_s_medium = self.dlg.lineEdit_100.text()
        treshold_existence_p_s_medium = np.asarray(path_treshold_existence_p_s_medium, dtype='float64')#float(input(path))
        path_treshold_existence_p_s_high = self.dlg.lineEdit_81.text()
        treshold_existence_p_s_high = np.asarray(path_treshold_existence_p_s_high, dtype='float64')#float(input(path))
        if protected_species_restoration < treshold_existence_p_s_low:
        	self.dlg.lineEdit_606.setText("1")
        	FEM_protected_species_restoration = 1
        	print(FEM_protected_species_restoration)
        elif protected_species_restoration > treshold_existence_p_s_high:
        	self.dlg.lineEdit_606.setText("5")
        	FEM_protected_species_restoration = 5
        	print(FEM_protected_species_restoration)
        else:
        	self.dlg.lineEdit_606.setText("3")
        	FEM_protected_species_restoration = 3
        	print(FEM_protected_species_restoration)
        path_treshold_potentially_a_b_low = self.dlg.lineEdit_97.text()
        treshold_potentially_a_b_low = np.asarray(path_treshold_potentially_a_b_low, dtype='float64')#float(input(path))
        path_treshold_potentially_a_b_medium = self.dlg.lineEdit_107.text()
        treshold_potentially_a_b_medium = np.asarray(path_treshold_potentially_a_b_medium, dtype='float64')#float(input(path))
        path_treshold_potentially_a_b_high = self.dlg.lineEdit_103.text()
        treshold_potentially_a_b_high = np.asarray(path_treshold_potentially_a_b_high, dtype='float64')#float(input(path))
        if buildings_restoration > treshold_potentially_a_b_low:
        	self.dlg.lineEdit_602.setText("1")
        	FEM_buildings_restoration = 1
        	print(FEM_buildings_restoration)
        elif buildings_restoration < treshold_potentially_a_b_high:
        	self.dlg.lineEdit_602.setText("5")
        	FEM_buildings_restoration = 5
        	print(FEM_buildings_restoration)
        else:
        	self.dlg.lineEdit_602.setText("3")
        	FEM_buildings_restoration = 3
        	print(FEM_buildings_restoration)
        path_treshold_land_use_low = self.dlg.lineEdit_91.text()
        treshold_land_use_low = np.asarray(path_treshold_land_use_low, dtype='float64')#float(input(path))
        path_treshold_land_use_medium = self.dlg.lineEdit_85.text()
        treshold_land_use_medium = np.asarray(path_treshold_land_use_medium, dtype='float64')#float(input(path))
        path_treshold_land_use_high = self.dlg.lineEdit_82.text()
        treshold_land_use_high = np.asarray(path_treshold_land_use_high, dtype='float64')#float(input(path))
        if land_use_restoration < treshold_land_use_low:
        	self.dlg.lineEdit_612.setText("1")
        	FEM_land_use_restoration = 1
        	print(FEM_land_use_restoration)
        elif land_use_restoration > treshold_land_use_high:
        	self.dlg.lineEdit_612.setText("5")
        	FEM_land_use_restoration = 5
        	print(FEM_land_use_restoration)
        else:
        	self.dlg.lineEdit_612.setText("3")
        	FEM_land_use_restoration = 3
        	print(FEM_land_use_restoration)
        	
        FEM_sum_restoration = FEM_Delta_Qrelative_restoration + FEM_Delta_T_restoration + FEM_Delta_h_restoration + FEM_c_fwb_restoration + FEM_protected_species_restoration + FEM_buildings_restoration + FEM_land_use_restoration
        print(FEM_sum_restoration)
        self.dlg.lineEdit_607.setText(str(FEM_sum_restoration))
        if FEM_sum_restoration >= 27:
        	self.dlg.lineEdit_610.setText("Low Demand")
        	print("Low Demand")
        elif FEM_sum_restoration < 23:
        	self.dlg.lineEdit_610.setText("High Demand")
        	print("High Demand")
        else:
        	self.dlg.lineEdit_610.setText("Medium Demand")
        	print("Medium Demand")

        
    def calculate_extra_FEM(self):
        path_threshold_delta_v_low = self.dlg.lineEdit_114.text()
        threshold_delta_v_low = np.asarray(path_threshold_delta_v_low, dtype='float64')#float(input(path))
        path_threshold_delta_v_medium = self.dlg.lineEdit_115.text()
        threshold_delta_v_medium = np.asarray(path_threshold_delta_v_medium, dtype='float64')#float(input(path))
        path_threshold_delta_v_high = self.dlg.lineEdit_116.text()
        threshold_delta_v_high = np.asarray(path_threshold_delta_v_high, dtype='float64')#float(input(path))
        if Delta_v < threshold_delta_v_low:
        	self.dlg.lineEdit_151.setText("1")
        	FEM_Delta_v = 1
        	print(FEM_Delta_v)
        elif Delta_v > threshold_delta_v_high:
        	self.dlg.lineEdit_151.setText("5")
        	FEM_Delta_v = 5
        	print(FEM_Delta_v)
        else:
        	self.dlg.lineEdit_151.setText("3")
        	FEM_Delta_v = 3
        	print(FEM_Delta_v)
        path_treshold_delta_tau_low = self.dlg.lineEdit_41.text()
        treshold_delta_tau_low = np.asarray(path_treshold_delta_tau_low, dtype='float64')#float(input(path))
        path_treshold_delta_tau_medium = self.dlg.lineEdit_42.text()
        treshold_delta_tau_medium = np.asarray(path_treshold_delta_tau_medium, dtype='float64')#float(input(path))
        path_treshold_delta_tau_high = self.dlg.lineEdit_43.text()
        treshold_delta_tau_high = np.asarray(path_treshold_delta_tau_high, dtype='float64')#float(input(path))
        if Delta_tau < treshold_delta_tau_low:
        	self.dlg.lineEdit_156.setText("1")
        	FEM_Delta_tau = 1
        	print(FEM_Delta_tau)
        elif Delta_tau > treshold_delta_tau_high:
        	self.dlg.lineEdit_156.setText("5")
        	FEM_Delta_tau = 5
        	print(FEM_Delta_tau)
        else:
        	self.dlg.lineEdit_156.setText("3")
        	FEM_Delta_tau = 3
        	print(FEM_Delta_tau)
        path_treshold_protected_habitat_low = self.dlg.lineEdit_44.text()
        treshold_protected_habitat_low = np.asarray(path_treshold_protected_habitat_low, dtype='float64')#float(input(path))
        path_treshold_protected_habitat_medium = self.dlg.lineEdit_61.text()
        treshold_protected_habitat_medium = np.asarray(path_treshold_protected_habitat_medium, dtype='float64')#float(input(path))
        path_treshold_protected_habitat_high = self.dlg.lineEdit_62.text()
        treshold_protected_habitat_high = np.asarray(path_treshold_protected_habitat_high, dtype='float64')#float(input(path))
        if protected_habitat < treshold_protected_habitat_low:
        	self.dlg.lineEdit_141.setText("1")
        	FEM_protected_habitat = 1
        	print(FEM_protected_habitat)
        elif protected_habitat > treshold_protected_habitat_high:
        	self.dlg.lineEdit_141.setText("5")
        	FEM_protected_habitat = 5
        	print(FEM_protected_habitat)
        else:
        	self.dlg.lineEdit_141.setText("3")
        	FEM_protected_habitat = 3
        	print(FEM_protected_habitat)
        path_treshold_vegetation_naturalness_low = self.dlg.lineEdit_63.text()
        treshold_vegetation_naturalness_low = np.asarray(path_treshold_vegetation_naturalness_low, dtype='float64')#float(input(path))
        path_treshold_vegetation_naturalness_medium = self.dlg.lineEdit_64.text()
        treshold_vegetation_naturalness_medium = np.asarray(path_treshold_vegetation_naturalness_medium, dtype='float64')#float(input(path))
        path_treshold_vegetation_naturalness_high = self.dlg.lineEdit_65.text()
        treshold_vegetation_naturalness_high = np.asarray(path_treshold_vegetation_naturalness_high, dtype='float64')#float(input(path))
        if vegetation_naturalness < treshold_vegetation_naturalness_low:
        	self.dlg.lineEdit_155.setText("1")
        	FEM_vegetation_naturalness = 1
        	print(FEM_vegetation_naturalness)
        elif vegetation_naturalness > treshold_vegetation_naturalness_high:
        	self.dlg.lineEdit_155.setText("5")
        	FEM_vegetation_naturalness = 5
        	print(FEM_vegetation_naturalness)
        else:
        	self.dlg.lineEdit_155.setText("3")
        	FEM_vegetation_naturalness = 3
        	print(FEM_vegetation_naturalness)
        path_treshold_water_level_dynamics_low = self.dlg.lineEdit_66.text()
        treshold_water_level_dynamics_low = np.asarray(path_treshold_water_level_dynamics_low, dtype='float64')#float(input(path))
        path_treshold_water_level_dynamics_medium = self.dlg.lineEdit_67.text()
        treshold_water_level_dynamics_medium = np.asarray(path_treshold_water_level_dynamics_medium, dtype='float64')#float(input(path))
        path_treshold_water_level_dynamics_high = self.dlg.lineEdit_68.text()
        treshold_water_level_dynamics_high = np.asarray(path_treshold_water_level_dynamics_high, dtype='float64')#float(input(path))
        if water_level_dynamics < treshold_water_level_dynamics_low:
        	self.dlg.lineEdit_146.setText("1")
        	FEM_water_level_dynamics = 1
        	print(FEM_water_level_dynamics)
        elif water_level_dynamics > treshold_water_level_dynamics_high:
        	self.dlg.lineEdit_146.setText("5")
        	FEM_water_level_dynamics = 5
        	print(FEM_water_level_dynamics)
        else:
        	self.dlg.lineEdit_146.setText("3")
        	FEM_water_level_dynamics = 3
        	print(FEM_water_level_dynamics)        
        path_treshold_potential_for_typical_habitats_low = self.dlg.lineEdit_69.text()
        treshold_potential_for_typical_habitats_low = np.asarray(path_treshold_potential_for_typical_habitats_low, dtype='float64')#float(input(path))
        path_treshold_potential_for_typical_habitats_medium = self.dlg.lineEdit_70.text()
        treshold_potential_for_typical_habitats_medium = np.asarray(path_treshold_potential_for_typical_habitats_medium, dtype='float64')#float(input(path))
        path_treshold_potential_for_typical_habitats_high = self.dlg.lineEdit_71.text()
        treshold_potential_for_typical_habitats_high = np.asarray(path_treshold_potential_for_typical_habitats_high, dtype='float64')#float(input(path))
        if potential_for_typical_habitats < treshold_potential_for_typical_habitats_low:
        	self.dlg.lineEdit_144.setText("1")
        	FEM_potential_for_typical_habitats = 1
        	print(FEM_potential_for_typical_habitats)
        elif potential_for_typical_habitats > treshold_potential_for_typical_habitats_high:
        	self.dlg.lineEdit_144.setText("5")
        	FEM_potential_for_typical_habitats = 5
        	print(FEM_potential_for_typical_habitats)
        else:
        	self.dlg.lineEdit_144.setText("3")
        	FEM_potential_for_typical_habitats = 3
        	print(FEM_potential_for_typical_habitats)       
        path_treshold_ecological_water_body_status_low = self.dlg.lineEdit_72.text()
        treshold_ecological_water_body_status_low = np.asarray(path_treshold_ecological_water_body_status_low, dtype='float64')#float(input(path))
        path_treshold_ecological_water_body_status_medium = self.dlg.lineEdit_73.text()
        treshold_ecological_water_body_status_medium = np.asarray(path_treshold_ecological_water_body_status_medium, dtype='float64')#float(input(path))
        path_treshold_ecological_water_body_status_high = self.dlg.lineEdit_74.text()
        treshold_ecological_water_body_status_high = np.asarray(path_treshold_ecological_water_body_status_high, dtype='float64')#float(input(path))
        if ecological_water_body_status < treshold_ecological_water_body_status_low:
        	self.dlg.lineEdit_148.setText("1")
        	FEM_ecological_water_body_status = 1
        	print(FEM_ecological_water_body_status)
        elif ecological_water_body_status > treshold_ecological_water_body_status_high:
        	self.dlg.lineEdit_148.setText("5")
        	FEM_ecological_water_body_status = 5
        	print(FEM_ecological_water_body_status)
        else:
        	self.dlg.lineEdit_148.setText("3")
        	FEM_ecological_water_body_status = 3
        	print(FEM_ecological_water_body_status)        
        path_treshold_parameter_invasive_species_low = self.dlg.lineEdit_117.text()
        treshold_parameter_invasive_species_low = np.asarray(path_treshold_parameter_invasive_species_low, dtype='float64')#float(input(path))
        path_treshold_parameter_invasive_species_medium = self.dlg.lineEdit_118.text()
        treshold_parameter_invasive_species_medium = np.asarray(path_treshold_parameter_invasive_species_medium, dtype='float64')#float(input(path))
        path_treshold_parameter_invasive_species_high = self.dlg.lineEdit_120.text()
        treshold_parameter_invasive_species_high = np.asarray(path_treshold_parameter_invasive_species_high, dtype='float64')#float(input(path))
        if parameter_invasive_species < treshold_parameter_invasive_species_low:
        	self.dlg.lineEdit_159.setText("1")
        	FEM_parameter_invasive_species = 1
        	print(FEM_parameter_invasive_species)
        elif parameter_invasive_species > treshold_parameter_invasive_species_high:
        	self.dlg.lineEdit_159.setText("5")
        	FEM_parameter_invasive_species = 5
        	print(FEM_parameter_invasive_species)
        else:
        	self.dlg.lineEdit_159.setText("3")
        	FEM_parameter_invasive_species = 3
        	print(FEM_parameter_invasive_species)        	
        path_treshold_presence_of_documented_planning_interests_low = self.dlg.lineEdit_123.text()
        treshold_presence_of_documented_planning_interests_low = np.asarray(path_treshold_presence_of_documented_planning_interests_low, dtype='float64')#float(input(path))
        path_treshold_presence_of_documented_planning_interests_medium = self.dlg.lineEdit_125.text()
        treshold_presence_of_documented_planning_interests_medium = np.asarray(path_treshold_presence_of_documented_planning_interests_medium, dtype='float64')#float(input(path))
        path_treshold_presence_of_documented_planning_interests_high = self.dlg.lineEdit_126.text()
        treshold_presence_of_documented_planning_interests_high = np.asarray(path_treshold_presence_of_documented_planning_interests_high, dtype='float64')#float(input(path))
        if presence_of_documented_planning_interests < treshold_presence_of_documented_planning_interests_low:
        	self.dlg.lineEdit_161.setText("1")
        	FEM_presence_of_documented_planning_interests = 1
        	print(FEM_presence_of_documented_planning_interests)
        elif presence_of_documented_planning_interests > treshold_presence_of_documented_planning_interests_high:
        	self.dlg.lineEdit_161.setText("5")
        	FEM_presence_of_documented_planning_interests = 5
        	print(FEM_presence_of_documented_planning_interests)
        else:
        	self.dlg.lineEdit_161.setText("3")
        	FEM_presence_of_documented_planning_interests = 3
        	print(FEM_presence_of_documented_planning_interests)
        path_treshold_extended_cost_benefit_analysis_low = self.dlg.lineEdit_127.text()
        treshold_extended_cost_benefit_analysis_low = np.asarray(path_treshold_extended_cost_benefit_analysis_low, dtype='float64')#float(input(path))
        path_treshold_extended_cost_benefit_analysis_medium = self.dlg.lineEdit_130.text()
        treshold_extended_cost_benefit_analysis_medium = np.asarray(path_treshold_extended_cost_benefit_analysis_medium, dtype='float64')#float(input(path))
        path_treshold_extended_cost_benefit_analysis_high = self.dlg.lineEdit_132.text()
        treshold_extended_cost_benefit_analysis_high = np.asarray(path_treshold_extended_cost_benefit_analysis_high, dtype='float64')#float(input(path))
        #if extended_cost_benefit_analysis < treshold_extended_cost_benefit_analysis_low:
        #	self.dlg.lineEdit_163.setText("1")
        #	FEM_extended_cost_benefit_analysis = 1
        #	print(FEM_extended_cost_benefit_analysis)
        #elif extended_cost_benefit_analysis > treshold_extended_cost_benefit_analysis_high:
        #	self.dlg.lineEdit_163.setText("5")
        #	FEM_extended_cost_benefit_analysis = 5
        #	print(FEM_extended_cost_benefit_analysis)
        #else:
        #	self.dlg.lineEdit_163.setText("3")
        #	FEM_extended_cost_benefit_analysis = 3
        #	print(FEM_extended_cost_benefit_analysis)

        FEM_sum = FEM_Delta_v + FEM_Delta_tau + FEM_protected_habitat + FEM_vegetation_naturalness + FEM_water_level_dynamics + FEM_potential_for_typical_habitats + FEM_ecological_water_body_status + FEM_parameter_invasive_species + FEM_presence_of_documented_planning_interests #+ FEM_extended_cost_benefit_analysis
        print(FEM_sum)
        self.dlg.lineEdit_153.setText(str(FEM_sum))
        if FEM_sum >= 27:
        	self.dlg.lineEdit_154.setText("Low Demand")
        	print("Low Demand")
        elif FEM_sum < 23:
        	self.dlg.lineEdit_154.setText("High Demand")
        	print("High Demand")
        else:
        	self.dlg.lineEdit_154.setText("Medium Demand")
        	print("Medium Demand")
        if FEM_Delta_v == 5 or FEM_Delta_tau == 5 or FEM_protected_habitat == 5 or FEM_vegetation_naturalness == 5 or FEM_water_level_dynamics == 5 or FEM_potential_for_typical_habitats == 5 or FEM_ecological_water_body_status == 5 or FEM_parameter_invasive_species == 5 or FEM_presence_of_documented_planning_interests == 5 or FEM_extended_cost_benefit_analysis == 5:
        	self.dlg.lineEdit_176.setText("Yes")
        	print("Need for Restoration:  Yes")
        else:
        	self.dlg.lineEdit_176.setText("No")
        	print("Need for Restoration:  No")
        	
    def calculate_extra_FEM_restoration(self):
        path_threshold_delta_v_low = self.dlg.lineEdit_114.text()
        threshold_delta_v_low = np.asarray(path_threshold_delta_v_low, dtype='float64')
        path_threshold_delta_v_medium = self.dlg.lineEdit_115.text()
        threshold_delta_v_medium = np.asarray(path_threshold_delta_v_medium, dtype='float64')
        path_threshold_delta_v_high = self.dlg.lineEdit_116.text()
        threshold_delta_v_high = np.asarray(path_threshold_delta_v_high, dtype='float64')
        if Delta_v_restoration < threshold_delta_v_low:
        	self.dlg.lineEdit_621.setText("1")
        	FEM_Delta_v_restoration = 1
        	print(FEM_Delta_v_restoration)
        elif Delta_v_restoration > threshold_delta_v_high:
        	self.dlg.lineEdit_621.setText("5")
        	FEM_Delta_v_restoration = 5
        	print(FEM_Delta_v_restoration)
        else:
        	self.dlg.lineEdit_621.setText("3")
        	FEM_Delta_v_restoration = 3
        	print(FEM_Delta_v_restoration)
        path_treshold_delta_tau_low = self.dlg.lineEdit_41.text()
        treshold_delta_tau_low = np.asarray(path_treshold_delta_tau_low, dtype='float64')
        path_treshold_delta_tau_medium = self.dlg.lineEdit_42.text()
        treshold_delta_tau_medium = np.asarray(path_treshold_delta_tau_medium, dtype='float64')#float(input(path))
        path_treshold_delta_tau_high = self.dlg.lineEdit_43.text()
        treshold_delta_tau_high = np.asarray(path_treshold_delta_tau_high, dtype='float64')
        if Delta_tau_restoration < treshold_delta_tau_low:
        	self.dlg.lineEdit_618.setText("1")
        	FEM_Delta_tau_restoration = 1
        	print(FEM_Delta_tau_restoration)
        elif Delta_tau_restoration > treshold_delta_tau_high:
        	self.dlg.lineEdit_618.setText("5")
        	FEM_Delta_tau_restoration = 5
        	print(FEM_Delta_tau_restoration)
        else:
        	self.dlg.lineEdit_618.setText("3")
        	FEM_Delta_tau_restoration = 3
        	print(FEM_Delta_tau_restoration)
        path_treshold_protected_habitat_low = self.dlg.lineEdit_44.text()
        treshold_protected_habitat_low = np.asarray(path_treshold_protected_habitat_low, dtype='float64')#float(input(path))
        path_treshold_protected_habitat_medium = self.dlg.lineEdit_61.text()
        treshold_protected_habitat_medium = np.asarray(path_treshold_protected_habitat_medium, dtype='float64')#float(input(path))
        path_treshold_protected_habitat_high = self.dlg.lineEdit_62.text()
        treshold_protected_habitat_high = np.asarray(path_treshold_protected_habitat_high, dtype='float64')#float(input(path))
        if protected_habitat_restoration < treshold_protected_habitat_low:
        	self.dlg.lineEdit_626.setText("1")
        	FEM_protected_habitat_restoration = 1
        	print(FEM_protected_habitat_restoration)
        elif protected_habitat_restoration > treshold_protected_habitat_high:
        	self.dlg.lineEdit_626.setText("5")
        	FEM_protected_habitat_restoration = 5
        	print(FEM_protected_habitat_restoration)
        else:
        	self.dlg.lineEdit_626.setText("3")
        	FEM_protected_habitat_restoration = 3
        	print(FEM_protected_habitat_restoration)
        path_treshold_vegetation_naturalness_low = self.dlg.lineEdit_63.text()
        treshold_vegetation_naturalness_low = np.asarray(path_treshold_vegetation_naturalness_low, dtype='float64')#float(input(path))
        path_treshold_vegetation_naturalness_medium = self.dlg.lineEdit_64.text()
        treshold_vegetation_naturalness_medium = np.asarray(path_treshold_vegetation_naturalness_medium, dtype='float64')#float(input(path))
        path_treshold_vegetation_naturalness_high = self.dlg.lineEdit_65.text()
        treshold_vegetation_naturalness_high = np.asarray(path_treshold_vegetation_naturalness_high, dtype='float64')#float(input(path))
        if vegetation_naturalness_restoration < treshold_vegetation_naturalness_low:
        	self.dlg.lineEdit_633.setText("1")
        	FEM_vegetation_naturalness_restoration = 1
        	print(FEM_vegetation_naturalness_restoration)
        elif vegetation_naturalness_restoration > treshold_vegetation_naturalness_high:
        	self.dlg.lineEdit_633.setText("5")
        	FEM_vegetation_naturalness_restoration = 5
        	print(FEM_vegetation_naturalness_restoration)
        else:
        	self.dlg.lineEdit_633.setText("3")
        	FEM_vegetation_naturalness_restoration = 3
        	print(FEM_vegetation_naturalness_restoration)
        path_treshold_water_level_dynamics_low = self.dlg.lineEdit_66.text()
        treshold_water_level_dynamics_low = np.asarray(path_treshold_water_level_dynamics_low, dtype='float64')#float(input(path))
        path_treshold_water_level_dynamics_medium = self.dlg.lineEdit_67.text()
        treshold_water_level_dynamics_medium = np.asarray(path_treshold_water_level_dynamics_medium, dtype='float64')#float(input(path))
        path_treshold_water_level_dynamics_high = self.dlg.lineEdit_68.text()
        treshold_water_level_dynamics_high = np.asarray(path_treshold_water_level_dynamics_high, dtype='float64')#float(input(path))
        if water_level_dynamics_restoration < treshold_water_level_dynamics_low:
        	self.dlg.lineEdit_617.setText("1")
        	FEM_water_level_dynamics_restoration = 1
        	print(FEM_water_level_dynamics_restoration)
        elif water_level_dynamics_restoration > treshold_water_level_dynamics_high:
        	self.dlg.lineEdit_617.setText("5")
        	FEM_water_level_dynamics_restoration = 5
        	print(FEM_water_level_dynamics_restoration)
        else:
        	self.dlg.lineEdit_617.setText("3")
        	FEM_water_level_dynamics_restoration = 3
        	print(FEM_water_level_dynamics_restoration)        
        path_treshold_potential_for_typical_habitats_low = self.dlg.lineEdit_69.text()
        treshold_potential_for_typical_habitats_low = np.asarray(path_treshold_potential_for_typical_habitats_low, dtype='float64')#float(input(path))
        path_treshold_potential_for_typical_habitats_medium = self.dlg.lineEdit_70.text()
        treshold_potential_for_typical_habitats_medium = np.asarray(path_treshold_potential_for_typical_habitats_medium, dtype='float64')#float(input(path))
        path_treshold_potential_for_typical_habitats_high = self.dlg.lineEdit_71.text()
        treshold_potential_for_typical_habitats_high = np.asarray(path_treshold_potential_for_typical_habitats_high, dtype='float64')#float(input(path))
        if potential_for_typical_habitats_restoration < treshold_potential_for_typical_habitats_low:
        	self.dlg.lineEdit_614.setText("1")
        	FEM_potential_for_typical_habitats_restoration = 1
        	print(FEM_potential_for_typical_habitats_restoration)
        elif potential_for_typical_habitats_restoration > treshold_potential_for_typical_habitats_high:
        	self.dlg.lineEdit_614.setText("5")
        	FEM_potential_for_typical_habitats_restoration = 5
        	print(FEM_potential_for_typical_habitats_restoration)
        else:
        	self.dlg.lineEdit_614.setText("3")
        	FEM_potential_for_typical_habitats_restoration = 3
        	print(FEM_potential_for_typical_habitats_restoration)       
        path_treshold_ecological_water_body_status_low = self.dlg.lineEdit_72.text()
        treshold_ecological_water_body_status_low = np.asarray(path_treshold_ecological_water_body_status_low, dtype='float64')#float(input(path))
        path_treshold_ecological_water_body_status_medium = self.dlg.lineEdit_73.text()
        treshold_ecological_water_body_status_medium = np.asarray(path_treshold_ecological_water_body_status_medium, dtype='float64')#float(input(path))
        path_treshold_ecological_water_body_status_high = self.dlg.lineEdit_74.text()
        treshold_ecological_water_body_status_high = np.asarray(path_treshold_ecological_water_body_status_high, dtype='float64')#float(input(path))
        if ecological_water_body_status_restoration < treshold_ecological_water_body_status_low:
        	self.dlg.lineEdit_624.setText("1")
        	FEM_ecological_water_body_status_restoration = 1
        	print(FEM_ecological_water_body_status_restoration)
        elif ecological_water_body_status_restoration > treshold_ecological_water_body_status_high:
        	self.dlg.lineEdit_624.setText("5")
        	FEM_ecological_water_body_status_restoration = 5
        	print(FEM_ecological_water_body_status_restoration)
        else:
        	self.dlg.lineEdit_624.setText("3")
        	FEM_ecological_water_body_status_restoration = 3
        	print(FEM_ecological_water_body_status_restoration)        
        path_treshold_parameter_invasive_species_low = self.dlg.lineEdit_117.text()
        treshold_parameter_invasive_species_low = np.asarray(path_treshold_parameter_invasive_species_low, dtype='float64')#float(input(path))
        path_treshold_parameter_invasive_species_medium = self.dlg.lineEdit_118.text()
        treshold_parameter_invasive_species_medium = np.asarray(path_treshold_parameter_invasive_species_medium, dtype='float64')#float(input(path))
        path_treshold_parameter_invasive_species_high = self.dlg.lineEdit_120.text()
        treshold_parameter_invasive_species_high = np.asarray(path_treshold_parameter_invasive_species_high, dtype='float64')#float(input(path))
        if parameter_invasive_species_restoration < treshold_parameter_invasive_species_low:
        	self.dlg.lineEdit_622.setText("1")
        	FEM_parameter_invasive_species_restoration = 1
        	print(FEM_parameter_invasive_species_restoration)
        elif parameter_invasive_species_restoration > treshold_parameter_invasive_species_high:
        	self.dlg.lineEdit_622.setText("5")
        	FEM_parameter_invasive_species_restoration = 5
        	print(FEM_parameter_invasive_species_restoration)
        else:
        	self.dlg.lineEdit_622.setText("3")
        	FEM_parameter_invasive_species_restoration = 3
        	print(FEM_parameter_invasive_species_restoration)        	
        path_treshold_presence_of_documented_planning_interests_low = self.dlg.lineEdit_123.text()
        treshold_presence_of_documented_planning_interests_low = np.asarray(path_treshold_presence_of_documented_planning_interests_low, dtype='float64')#float(input(path))
        path_treshold_presence_of_documented_planning_interests_medium = self.dlg.lineEdit_125.text()
        treshold_presence_of_documented_planning_interests_medium = np.asarray(path_treshold_presence_of_documented_planning_interests_medium, dtype='float64')#float(input(path))
        path_treshold_presence_of_documented_planning_interests_high = self.dlg.lineEdit_126.text()
        treshold_presence_of_documented_planning_interests_high = np.asarray(path_treshold_presence_of_documented_planning_interests_high, dtype='float64')#float(input(path))
        if presence_of_documented_planning_interests_restoration < treshold_presence_of_documented_planning_interests_low:
        	self.dlg.lineEdit_625.setText("1")
        	FEM_presence_of_documented_planning_interests_restoration = 1
        	print(FEM_presence_of_documented_planning_interests_restoration)
        elif presence_of_documented_planning_interests_restoration > treshold_presence_of_documented_planning_interests_high:
        	self.dlg.lineEdit_625.setText("5")
        	FEM_presence_of_documented_planning_interests_restoration = 5
        	print(FEM_presence_of_documented_planning_interests_restoration)
        else:
        	self.dlg.lineEdit_625.setText("3")
        	FEM_presence_of_documented_planning_interests_restoration = 3
        	print(FEM_presence_of_documented_planning_interests_restoration)
        path_treshold_extended_cost_benefit_analysis_low = self.dlg.lineEdit_127.text()
        treshold_extended_cost_benefit_analysis_low = np.asarray(path_treshold_extended_cost_benefit_analysis_low, dtype='float64')
        path_treshold_extended_cost_benefit_analysis_medium = self.dlg.lineEdit_130.text()
        treshold_extended_cost_benefit_analysis_medium = np.asarray(path_treshold_extended_cost_benefit_analysis_medium, dtype='float64')
        path_treshold_extended_cost_benefit_analysis_high = self.dlg.lineEdit_132.text()
        treshold_extended_cost_benefit_analysis_high = np.asarray(path_treshold_extended_cost_benefit_analysis_high, dtype='float64')
        if extended_cost_benefit_analysis_restoration < treshold_extended_cost_benefit_analysis_low:
        	self.dlg.lineEdit_629.setText("1")
        	FEM_extended_cost_benefit_analysis_restoration = 1
        	print(FEM_extended_cost_benefit_analysis_restoration)
        elif extended_cost_benefit_analysis_restoration > treshold_extended_cost_benefit_analysis_high:
        	self.dlg.lineEdit_629.setText("5")
        	FEM_extended_cost_benefit_analysis_restoration = 5
        	print(FEM_extended_cost_benefit_analysis_restoration)
        else:
        	self.dlg.lineEdit_629.setText("3")
        	FEM_extended_cost_benefit_analysis_restoration = 3
        	print(FEM_extended_cost_benefit_analysis_restoration)

        FEM_sum_restoration = FEM_Delta_v_restoration + FEM_Delta_tau_restoration + FEM_protected_habitat_restoration + FEM_vegetation_naturalness_restoration + FEM_water_level_dynamics_restoration + FEM_potential_for_typical_habitats_restoration + FEM_ecological_water_body_status_restoration + FEM_parameter_invasive_species_restoration + FEM_presence_of_documented_planning_interests_restoration + FEM_extended_cost_benefit_analysis_restoration
        print(FEM_sum_restoration)
        self.dlg.lineEdit_630.setText(str(FEM_sum_restoration))
        if FEM_sum_restoration >= 27:
        	self.dlg.lineEdit_615.setText("Low Demand")
        	print("Low Demand")
        elif FEM_sum_restoration < 23:
        	self.dlg.lineEdit_615.setText("High Demand")
        	print("High Demand")
        else:
        	self.dlg.lineEdit_615.setText("Medium Demand")
        	print("Medium Demand")


        flood_array2 = 0
        flood_array_new = 0
        numpy_object_array_new = 0
    def automatic_floodplain(self):
        layer_danube_cl = riverCenterlineVectorLayer
        layer_HQ100 = floodVectorLayer
        #QgsProject.instance().addMapLayer(layer_danube_cl)
        #QgsProject.instance().addMapLayer(layer_HQ100)
# PART1 #####
        print("Part1 Begin")
        features_HQ100 = layer_HQ100.getFeatures()
        for feature in features_HQ100:
            geom_HQ100 = feature.geometry()
            x_HQ100 = geom_HQ100.asMultiPolyline()
            #print("Length of x_HQ100 = ", len(x_HQ100))
            
        features = layer_danube_cl.getFeatures()
        for feature in features:
            geom = feature.geometry()
            x_danube_cl = geom.asMultiPolyline()
            #print("Length of x_Danube_Centerline = ", len(x_danube_cl))

        myarray_HQ100 = np.array(x_HQ100)

        result_HQ100 = []
        for i in range(len(myarray_HQ100)):
            for j in range(len(myarray_HQ100[i])):
                for k in range(len(myarray_HQ100[i][j])):
                	testarray_HQ100 = np.array((myarray_HQ100[i][j][k]))
                	result_HQ100 = np.append(result_HQ100, testarray_HQ100)

        result_array_HQ100 = np.zeros((int(len(result_HQ100)/2), 2))

        for i in range(len(result_array_HQ100)):
            result_array_HQ100[i,:] = np.array((result_HQ100[2*i], result_HQ100[2*i+1]))

        # SORTING****************************************
        result_array_HQ100 = result_array_HQ100[result_array_HQ100[:,0].argsort()[::-1]]
        #*************************************************

        points_HQ100 = np.zeros(len(result_array_HQ100), dtype=object)
        for i in range(len(result_array_HQ100)):
            points_HQ100[i] = QgsPoint(result_array_HQ100[i,0], result_array_HQ100[i,1])

        layer_HQ100 = QgsVectorLayer('Point?crs=epsg:3035', 'Inudation Area' , "memory") 
        pr_HQ100 = layer_HQ100.dataProvider()
        pt_HQ100 = QgsFeature()

        for i in range(len(points_HQ100)):
            pt_HQ100.setGeometry(points_HQ100[i])
            pr_HQ100.addFeatures([pt_HQ100])
            layer_HQ100.updateExtents()
            QgsProject.instance().addMapLayer(layer_HQ100)
    
        #****** DANUBE CENTERLINE RIVER POINT CREATION ******************************
        myarray_cl = np.array(x_danube_cl)
        
        result_cl = []
        for i in range(len(myarray_cl)):
        	for j in range(len(myarray_cl[i])):
        		for k in range(len(myarray_cl[i][j])):
        			testarray_cl = np.array((myarray_cl[i][j][k]))
        			result_cl = np.append(result_cl, testarray_cl)

        result_array_cl = np.zeros((int(len(result_cl)/2), 2))
        for i in range(len(result_array_cl)):
            result_array_cl[i,:] = np.array((result_cl[2*i], result_cl[2*i+1]))

        # SORTING****************************************
        #result_array_cl = result_array_cl[result_array_cl[:,0].argsort()[::-1]]
        #*************************************************

        points_danube_cl = np.zeros(len(result_array_cl), dtype=object)
        for i in range(len(result_array_cl)):
            points_danube_cl[i] = QgsPoint(result_array_cl[i,0], result_array_cl[i,1])

        layer_cl = QgsVectorLayer('Point?crs=epsg:3035', 'Danube_Centerline' , "memory") 
        pr_cl = layer_cl.dataProvider()
        pt_cl = QgsFeature()

        for i in range(len(points_danube_cl)):
            pt_cl.setGeometry(points_danube_cl[i])
            pr_cl.addFeatures([pt_cl])
            layer_cl.updateExtents()
            #QgsProject.instance().addMapLayer(layer_cl)

        result_array_danube_cl = []
        for i in range(len(result_array_cl)):
            if result_array_cl[i,0] <= max(result_array_HQ100[:,0]) and result_array_cl[i,0] >= min(result_array_HQ100[:,0]):
                result_array_danube_cl.extend(result_array_cl[i])

        result_array_danube2_cl = np.zeros((int(len(result_array_danube_cl)/2), 2))
        for i in range(len(result_array_danube2_cl)):
            result_array_danube2_cl[i,:] = np.array((result_array_danube_cl[2*i], result_array_danube_cl[2*i+1]))

        points_array_danube_cl = np.zeros(len(result_array_danube2_cl), dtype=object)
        for i in range(len(result_array_danube2_cl)):
            points_array_danube_cl[i] = QgsPoint(result_array_danube2_cl[i,0], result_array_danube2_cl[i,1])

        layer_array_danube_cl = QgsVectorLayer('Point?crs=epsg:3035', 'Centerline of the River' , "memory") 
        pr_array_danube_cl = layer_array_danube_cl.dataProvider()
        pt_array_danube_cl = QgsFeature()

        for i in range(len(points_array_danube_cl)):
            pt_array_danube_cl.setGeometry(points_array_danube_cl[i])
            pr_array_danube_cl.addFeatures([pt_array_danube_cl])
            layer_array_danube_cl.updateExtents()
            QgsProject.instance().addMapLayer(layer_array_danube_cl)
        #print("Part1 Completed")
# PART2 #####
        print("Part2 Begin")
        #flood_array2 = 0
        ##def find_nearest2(array, value, treshhold, treshhold_flood_points):
        global flood_array2
        flood_array = []
        dist_array = np.zeros((int(len(result_array_danube2_cl))))
        count = 0
        for i in range(len(result_array_HQ100)):
            for j in range(len(result_array_danube2_cl)):
                  dist_array[j] = np.sqrt((result_array_HQ100[i,0]-result_array_danube2_cl[j,0])**2+(result_array_HQ100[i,1]-result_array_danube2_cl[j,1])**2)  
            id = dist_array.argmin()
            if dist_array[id] >= river_width*ratio_factor:
                count +=1
                if count > 5:
                    #print("Flood")
                    flood_array.extend(result_array_HQ100[i])
                    count = 0
            else: 
                print("Flood event is over")
            #closest_points = value[id]
            #print(closest_points)
            #print(flood_array)
            
        flood_array2 = np.zeros((int(len(flood_array)/2), 2))
        for i in range(len(flood_array2)):
            flood_array2[i,:] = np.array((flood_array[2*i], flood_array[2*i+1]))
        
        #test_data = find_nearest2(result_array_HQ100, result_array_danube2_cl, 1100, 5)
        #print(test_data)
        
        flood_points = np.zeros(len(flood_array2), dtype=object)
        for i in range(len(flood_array2)):
            flood_points[i] = QgsPoint(flood_array2[i,0], flood_array2[i,1])
        
        layer_flood = QgsVectorLayer('Point?crs=epsg:3035', 'danube_flood' , "memory") 
        pr_flood = layer_flood.dataProvider()
        pt_flood = QgsFeature()
        
        for i in range(len(flood_points)):
            pt_flood.setGeometry(flood_points[i])
            pr_flood.addFeatures([pt_flood])
            layer_flood.updateExtents()
            QgsProject.instance().addMapLayer(layer_flood)
        
        ##def find_nearest3(value, array):
        dist_array = np.zeros((int(len(result_array_danube2_cl))))
        flood_array=[]
        global flood_array_new
        
        for i in range(len(flood_array2)):
            for j in range(len(result_array_danube2_cl)):
                dist_array[j] = np.sqrt((flood_array2[i,0]-result_array_danube2_cl[j,0])**2+(flood_array2[i,1]-result_array_danube2_cl[j,1])**2)
            id = dist_array.argmin()
            #print(dist_array[id])
            flood_array.extend(result_array_danube2_cl[id])
            #print(flood_array)
         
        flood_array_new = np.zeros((int(len(flood_array)/2), 2))
        for i in range(len(flood_array_new)):
            flood_array_new[i,:] = np.array((flood_array[2*i], flood_array[2*i+1]))
        flood_array_new = np.unique(flood_array_new, axis=0)
        
            #test_data2 = find_nearest3(flood_array2, result_array_danube2_cl)
        
        flood_points_new = np.zeros(len(flood_array_new), dtype=object)
        for i in range(len(flood_array_new)):
            flood_points_new[i] = QgsPoint(flood_array_new[i,0], flood_array_new[i,1])#
        
        layer_flood_new = QgsVectorLayer('Point?crs=epsg:3035', 'danube_flood_new' , "memory") 
        pr_flood_new = layer_flood_new.dataProvider()
        pt_flood_new = QgsFeature()
        
        for i in range(len(flood_points_new)):
            pt_flood_new.setGeometry(flood_points_new[i])
            pr_flood_new.addFeatures([pt_flood_new])
            layer_flood_new.updateExtents()
            QgsProject.instance().addMapLayer(layer_flood_new)
# PART3 #####
        print("Part3 Begin")
        #numpy_object_array = np.empty((), dtype=object)
        #def separate_flood(array, mythreshold, length_threshold):
        global numpy_object_array_new
        prev_segment=0
        segment_array=np.zeros(0)
            
        for i in range(len(flood_array_new)):
            curr_distance=((flood_array_new[i-1,0]-flood_array_new[i,0])**2+(flood_array_new[i-1,1]-flood_array_new[i,1])**2)**0.5
            if curr_distance >= distance_flood:
                segment_array=np.append(segment_array,i)
        
        myarray_segmented=np.zeros((len(segment_array),2))
        for i in range(len(segment_array)):
             myarray_segmented[i,:]=flood_array_new[int(segment_array[i]),:]
            
        segment_array=np.append(segment_array,len(flood_array_new)+1)
        numpy_object_array = np.zeros((len(myarray_segmented)),dtype=object)
            
        for i in range(len(numpy_object_array)):
             current_matrix=flood_array_new[int(segment_array[i]):int(segment_array[i+1])-1,:]
             numpy_object_array[i]=current_matrix
        full_array=numpy_object_array
        short_arrays=np.zeros(0)
            
        for i in range(len(numpy_object_array)):
             curr_matrix=numpy_object_array[i]
             #print(len(curr_matrix))
             if len(curr_matrix)< no_of_points:
                 short_arrays=np.append(short_arrays,i)
                 print(len(short_arrays))
            
        for i in range(len(short_arrays)):
             numpy_object_array=np.delete(numpy_object_array,int(short_arrays[i-1]))
        numpy_object_array_new = numpy_object_array
            
        #test_data = separate_flood(flood_array_new, 5000, 10)
        
        #*******************************************************************
        # Identification of individual HQ100 from the centerline (X)
        
        result_flood = []
        
        for i in range(len(numpy_object_array_new)):
            temp2 = []
            for j in range(len(result_array_HQ100)):
                if result_array_HQ100[j,0] <= np.amax(numpy_object_array_new[i],axis=0)[0] and result_array_HQ100[j,0] >= np.amin(numpy_object_array_new[i],axis=0)[0]:
                    temp2.append(result_array_HQ100[j])
            result_flood.append(temp2)
        
        fp_np=np.zeros(len(result_flood),dtype="object")
        for i in range(len(result_flood)):
            fp_np[i] = np.array(result_flood[i])
        
        flood_points_test_new = []
        
        for a in fp_np: #this is the list
            temp = []
            for j in range(a.shape[0]):
                temp.append(QgsPoint(a[j][0], a[j][1]))
            flood_points_test_new.append(temp)
        
        fp_np=np.zeros(len(flood_points_test_new),dtype="object")
        for i in range(len(flood_points_test_new)):
            fp_np[i] = np.array(flood_points_test_new[i])
        
        for j in range(len(fp_np)):
            layer_HQ100 = QgsVectorLayer('Point?crs=epsg:3035', 'HQ100_'+str(j), "memory") 
            pr_HQ100 = layer_HQ100.dataProvider()
            pt_HQ100 = QgsFeature()
            for i in range(len(fp_np[j])):
                pt_HQ100.setGeometry(fp_np[j][i])
                pr_HQ100.addFeatures([pt_HQ100])
                layer_HQ100.updateExtents()
                QgsProject.instance().addMapLayer(layer_HQ100)
             
# Create Attribute Table for the Floodplain
        
    def create_attribute_table(self):
        layer = self.dlg.mMapLayerComboBox.currentLayer()
        self.dlg.lineEdit_34.setText("Attribute Table created")
        features=layer.getFeatures()    
        layer_provider = layer.dataProvider()
        #for f in features:
        #    print(len(f.attributes()))
        #    if len(f.attributes()) > 0:
        #        print(len(f.attributes()))
        #        for i in range(len(f.attributes())):
        #            print(f.attributes()[i])
        #            layer_provider.deleteAttributes([i])
        #layer.updateFields()
        layer_provider.addAttributes([QgsField("FID", QVariant.Double), QgsField("DFGIS_ID", QVariant.String), QgsField("FP_Type", QVariant.String), QgsField("Location", QVariant.String), QgsField("Transbound", QVariant.String), QgsField("Area", QVariant.Double), QgsField("FPLength", QVariant.Double), QgsField("Chan_width", QVariant.Double), QgsField("delta_Q", QVariant.Double), QgsField("delta_t", QVariant.Double), QgsField("delta_h", QVariant.Double), QgsField("C_fp_wb", QVariant.Double), QgsField("Prot_spp", QVariant.Double), QgsField("Building", QVariant.Double), QgsField("Land_use", QVariant.Double), QgsField("R_delta_Q", QVariant.Double), QgsField("R_delta_t", QVariant.Double), QgsField("R_delta_h", QVariant.Double), QgsField("R_C_fp_wb", QVariant.Double), QgsField("R_Prot_spp", QVariant.Double), QgsField("R_Building", QVariant.Double), QgsField("R_Land_use", QVariant.Double), QgsField("Hyd_eff", QVariant.Double), QgsField("delta_v", QVariant.Double), QgsField("prot_hab", QVariant.Double), QgsField("veg_nat", QVariant.Double), QgsField("WL_dyn", QVariant.Double), QgsField("p_int", QVariant.Double), QgsField("invasive_sp", QVariant.Double), QgsField("R_invasive_sp", QVariant.Double), QgsField("ext_CBA", QVariant.Double), QgsField("R_ext_CBA", QVariant.Double), QgsField("R_Hyd_eff", QVariant.Double), QgsField("R_delta_v", QVariant.Double), QgsField("R_prob_hab", QVariant.Double), QgsField("R_veg_nat", QVariant.Double), QgsField("R_WL_dyn", QVariant.Double), QgsField("R_pl_int", QVariant.Double), QgsField("delt_Tau", QVariant.Double), QgsField("p_tb_hab", QVariant.Double), QgsField("wb_status", QVariant.String), QgsField("R_delt_Tau", QVariant.Double), QgsField("R_p_tb_hab", QVariant.Double), QgsField("R_wb_stat", QVariant.Double), QgsField("Restoratio", QVariant.String), QgsField("HQ100", QVariant.Double), QgsField("Ecosystem_service", QVariant.Double), QgsField("Habitat_modelling", QVariant.Double), QgsField("Stakeholder_analysis", QVariant.Double), QgsField("km_from", QVariant.Double), QgsField("km_to", QVariant.Double)])
        layer.updateFields()
        #layer.startEditing()
        #features=layer.getFeatures()
        #for f in features:
        #    id=f.id()
        #    attr_value={7:10}
        #    layer_provider.changeAttributeValues({id:attr_value})
        #layer.commitChanges()
        print (layer.fields().names())
        for f in features:
            print(f.attributes())#[0])

    def hydrology_add_attribute_table(self):
        layer = self.dlg.mMapLayerComboBox.currentLayer()
        features=layer.getFeatures()    
        layer_provider = layer.dataProvider()
        print (layer.fields().names())
        #for f in features:                    #shows the values of the attribute table
        #    print(f.attributes())#[0])
        layer.startEditing()
        features=layer.getFeatures()
        for f in features:
            id=f.id()
            attr_value_Q={8:str(Delta_Qrelative)}
            attr_value_T={9:str(Delta_T)}
            layer_provider.changeAttributeValues({id:attr_value_Q})
            layer_provider.changeAttributeValues({id:attr_value_T})
        layer.commitChanges()
        self.dlg.lineEdit_35.setText("Results added")      
            
    def hydraulics_add_attribute_table(self):
        layer = self.dlg.mMapLayerComboBox.currentLayer()
        features=layer.getFeatures()    
        layer_provider = layer.dataProvider()
        layer.startEditing()
        features=layer.getFeatures()
        for f in features:
            id=f.id()
            attr_value={10:str(Delta_h)}
            layer_provider.changeAttributeValues({id:attr_value})
        layer.commitChanges()
        self.dlg.lineEdit_36.setText("Results added")

    def hydraulics_extra_add_attribute_table(self):
        layer = self.dlg.mMapLayerComboBox.currentLayer()
        features=layer.getFeatures()    
        layer_provider = layer.dataProvider()
        layer.startEditing()
        features=layer.getFeatures()
        for f in features:
            id=f.id()
            attr_value1={23:str(Delta_v)}
            attr_value2={38:str(Delta_tau)}
            layer_provider.changeAttributeValues({id:attr_value1})
            layer_provider.changeAttributeValues({id:attr_value2})
        layer.commitChanges()
        self.dlg.lineEdit_39.setText("Results added")     

    def ecology_add_attribute_table(self):
        layer = self.dlg.mMapLayerComboBox.currentLayer()
        features=layer.getFeatures()    
        layer_provider = layer.dataProvider()
        layer.startEditing()
        features=layer.getFeatures()
        for f in features:
            id=f.id()
            attr_value_protected_species={12:str(protected_species)}
            attr_value_c_fwb={11:str(c_fwb)}
            layer_provider.changeAttributeValues({id:attr_value_protected_species})
            layer_provider.changeAttributeValues({id:attr_value_c_fwb})
        layer.commitChanges()
        self.dlg.lineEdit_37.setText("Results added")
        
    def ecology_extra_add_attribute_table(self):
        layer = self.dlg.mMapLayerComboBox.currentLayer()
        features=layer.getFeatures()    
        layer_provider = layer.dataProvider()
        layer.startEditing()
        features=layer.getFeatures()
        for f in features:
            id=f.id()
            attr_value1={24:str(protected_habitat)}
            attr_value2={25:str(vegetation_naturalness)}
            attr_value3={26:str(water_level_dynamics)}
            attr_value4={39:str(potential_for_typical_habitats)}
            attr_value5={40:str(ecological_water_body_status)}
            attr_value6={28:str(parameter_invasive_species)}
            layer_provider.changeAttributeValues({id:attr_value1})
            layer_provider.changeAttributeValues({id:attr_value2})
            layer_provider.changeAttributeValues({id:attr_value3})
            layer_provider.changeAttributeValues({id:attr_value4})
            layer_provider.changeAttributeValues({id:attr_value5})
            layer_provider.changeAttributeValues({id:attr_value6})
        layer.commitChanges()
        self.dlg.lineEdit_56.setText("Results added")

    def socio_economics_add_attribute_table(self):
        layer = self.dlg.mMapLayerComboBox.currentLayer()
        features=layer.getFeatures()    
        layer_provider = layer.dataProvider()
        layer.startEditing()
        features=layer.getFeatures()
        for f in features:
            id=f.id()
            attr_value_buildings={13:str(buildings)}
            attr_value_land_use={14:str(land_use)}
            layer_provider.changeAttributeValues({id:attr_value_buildings})
            layer_provider.changeAttributeValues({id:attr_value_land_use})
        layer.commitChanges()
        self.dlg.lineEdit_38.setText("Results added")   

    def socio_economics_extra_add_attribute_table(self):
        layer = self.dlg.mMapLayerComboBox.currentLayer()
        features=layer.getFeatures()    
        layer_provider = layer.dataProvider()
        layer.startEditing()
        features=layer.getFeatures()
        for f in features:
            id=f.id()
            attr_value_buildings={27:str(presence_of_documented_planning_interests)}
            #attr_value_land_use={30:str(extended_cost_benefit_analysis)}
            layer_provider.changeAttributeValues({id:attr_value_buildings})
            #layer_provider.changeAttributeValues({id:attr_value_land_use})
        layer.commitChanges()
        self.dlg.lineEdit_59.setText("Results added")  
        
    def FEM_minimum_add_attribute_table(self):
        path1 = self.dlg.lineEdit_131.text()
        FEM_Delta_Q_relative = np.asarray(path1, dtype='float64')
        path2 = self.dlg.lineEdit_128.text()
        FEM_Delta_T = np.asarray(path2, dtype='float64')
        path3 = self.dlg.lineEdit_140.text()
        FEM_Delta_h = np.asarray(path3, dtype='float64')
        path4 = self.dlg.lineEdit_139.text()
        FEM_c_fwb = np.asarray(path4, dtype='float64')
        path5 = self.dlg.lineEdit_119.text()
        FEM_protected_species = np.asarray(path5, dtype='float64')
        path6 = self.dlg.lineEdit_124.text()
        FEM_buildings = np.asarray(path6, dtype='float64')
        path7 = self.dlg.lineEdit_147.text()
        FEM_land_use = np.asarray(path7, dtype='float64')
        layer = self.dlg.mMapLayerComboBox.currentLayer()
        features=layer.getFeatures()    
        layer_provider = layer.dataProvider()
        layer.startEditing()
        features=layer.getFeatures()
        for f in features:
            id=f.id()
            attr_value_FEM_Delta_Q_relative = {15:str(FEM_Delta_Q_relative)}
            attr_value_FEM_Delta_T = {16:str(FEM_Delta_T)}
            attr_value_FEM_Delta_h = {17:str(FEM_Delta_h)}
            attr_value_FEM_c_fwb = {18:str(FEM_c_fwb)}
            attr_value_FEM_protected_species = {19:str(FEM_protected_species)}
            attr_value_FEM_buildings = {20:str(FEM_buildings)}
            attr_value_FEM_land_use = {21:str(FEM_land_use)}
            layer_provider.changeAttributeValues({id:attr_value_FEM_Delta_Q_relative})
            layer_provider.changeAttributeValues({id:attr_value_FEM_Delta_T})
            layer_provider.changeAttributeValues({id:attr_value_FEM_Delta_h})
            layer_provider.changeAttributeValues({id:attr_value_FEM_c_fwb})
            layer_provider.changeAttributeValues({id:attr_value_FEM_protected_species})
            layer_provider.changeAttributeValues({id:attr_value_FEM_buildings})
            layer_provider.changeAttributeValues({id:attr_value_FEM_land_use})
        layer.commitChanges()
        self.dlg.lineEdit_75.setText("Results added")   

    def FEM_extra_add_attribute_table(self):       
        path1 = self.dlg.lineEdit_151.text()
        FEM_Delta_v = np.asarray(path1, dtype='float64')
        path2 = self.dlg.lineEdit_156.text()
        FEM_Delta_tau = np.asarray(path2, dtype='float64')
        path3 = self.dlg.lineEdit_141.text()
        FEM_protected_habitat = np.asarray(path3, dtype='float64')
        path4 = self.dlg.lineEdit_155.text()
        FEM_vegetation_naturalness = np.asarray(path4, dtype='float64')
        path5 = self.dlg.lineEdit_146.text()
        FEM_water_level_dynamics = np.asarray(path5, dtype='float64')
        path6 = self.dlg.lineEdit_144.text()
        FEM_potential_for_typical_habitats = np.asarray(path6, dtype='float64')
        path7 = self.dlg.lineEdit_148.text()
        FEM_ecological_water_body_status = np.asarray(path7, dtype='float64')
        path8 = self.dlg.lineEdit_159.text()
        FEM_parameter_invasive_species = np.asarray(path8, dtype='float64')
        path9 = self.dlg.lineEdit_161.text()
        FEM_presence_of_documented_planning_interests = np.asarray(path9, dtype='float64')
        path10 = self.dlg.lineEdit_163.text()
        FEM_extended_cost_benefit_analysis = np.asarray(path10, dtype='float64')
        layer = self.dlg.mMapLayerComboBox.currentLayer()
        features=layer.getFeatures()    
        layer_provider = layer.dataProvider()
        layer.startEditing()
        features=layer.getFeatures()
        for f in features:
            id=f.id()
            attr_value_FEM_Delta_v = {33:str(FEM_Delta_v)}
            attr_value_FEM_Delta_tau = {41:str(FEM_Delta_tau)}
            attr_value_FEM_protected_habitat = {34:str(FEM_protected_habitat)}
            attr_value_FEM_vegetation_naturalness = {35:str(FEM_vegetation_naturalness)}
            attr_value_FEM_water_level_dynamics = {36:str(FEM_water_level_dynamics)}
            attr_value_FEM_potential_for_typical_habitats = {42:str(FEM_potential_for_typical_habitats)}
            attr_value_FEM_ecological_water_body_status = {43:str(FEM_ecological_water_body_status)}
            attr_value_FEM_parameter_invasive_species = {29:str(FEM_parameter_invasive_species)}
            attr_value_FEM_presence_of_documented_planning_interests = {37:str(FEM_presence_of_documented_planning_interests)}
            attr_value_FEM_extended_cost_benefit_analysis = {31:str(FEM_extended_cost_benefit_analysis)}
            layer_provider.changeAttributeValues({id:attr_value_FEM_Delta_v})
            layer_provider.changeAttributeValues({id:attr_value_FEM_Delta_tau})
            layer_provider.changeAttributeValues({id:attr_value_FEM_protected_habitat})
            layer_provider.changeAttributeValues({id:attr_value_FEM_vegetation_naturalness})
            layer_provider.changeAttributeValues({id:attr_value_FEM_water_level_dynamics})
            layer_provider.changeAttributeValues({id:attr_value_FEM_potential_for_typical_habitats})
            layer_provider.changeAttributeValues({id:attr_value_FEM_ecological_water_body_status})
            layer_provider.changeAttributeValues({id:attr_value_FEM_parameter_invasive_species})
            layer_provider.changeAttributeValues({id:attr_value_FEM_presence_of_documented_planning_interests})
            layer_provider.changeAttributeValues({id:attr_value_FEM_extended_cost_benefit_analysis})
        layer.commitChanges()
        self.dlg.lineEdit_77.setText("Results added")   

#%% Floodplain Areas ######################################################     
        
#    def loadVectorshapefiles(self): #load vector layers to combobox
#        self.dlg.comboBox_2.clear()
#        layers_vector = QgsProject.instance().mapLayers().values()
#        vector_list = []
#        for layer in layers_vector:
#            if layer.type() == QgsMapLayer.VectorLayer:
#               vector_list.append(layer.name())
#        self.dlg.comboBox_2.addItems(vector_list)
    	
#    def openVector(self):
#        infile = str(QFileDialog.getOpenFileNameAndFilter(filter = "Shapefiles (*.shp)")[0])
#        if infile is not None:
#           self.iface.addVectorLayer(infile, str.split(os.path.basename(infile), ".")[0], "ogr")
#           self.loadVectors()
        
        
        
    #def loadRastershapefiles(self): #load raster layers to combobox
    #    self.dlg.comboBox_3.clear()
    #    layers = self.iface.legendInterface().layers()
    #    raster_list = []
    #    for layer in layers:
    #        if layer.type() == QgsMapLayer.VectorLayer:
    #        vector_list.append(layer.name())
    #    self.dlg.comboBox_2.addItems(vector_list)
    	

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = test_pluginDialog()
            self.dlg.toolButton.clicked.connect(self.select_output_file)
            
            self.dlg.toolButton_2.clicked.connect(self.select_input_file1)
            self.dlg.toolButton_3.clicked.connect(self.select_input_file2)
            self.dlg.toolButton_4.clicked.connect(self.select_input_file3)
            self.dlg.toolButton_10.clicked.connect(self.select_input_file1_restoration)
            self.dlg.toolButton_9.clicked.connect(self.select_input_file2_restoration)
            self.dlg.toolButton_11.clicked.connect(self.select_input_file3_restoration)
            
            self.dlg.toolButton_5.clicked.connect(self.select_input_file5)
            self.dlg.toolButton_6.clicked.connect(self.select_input_file6)
            self.dlg.toolButton_7.clicked.connect(self.select_input_file7)
            self.dlg.toolButton_8.clicked.connect(self.select_input_file8)
            
            self.dlg.pushButton_2.clicked.connect(self.automatic_floodplain)
            self.dlg.pushButton_5.clicked.connect(self.import1)
            self.dlg.pushButton_68.clicked.connect(self.import1_restoration)
            self.dlg.pushButton_6.clicked.connect(self.import2)
            self.dlg.pushButton_61.clicked.connect(self.import2_restoration)
            self.dlg.pushButton_7.clicked.connect(self.import3)
            self.dlg.pushButton_66.clicked.connect(self.import3_restoration)
            self.dlg.pushButton_8.clicked.connect(self.import4)
            self.dlg.pushButton_58.clicked.connect(self.import4_restoration)
            self.dlg.pushButton_21.clicked.connect(self.import5)
            self.dlg.pushButton_22.clicked.connect(self.import6)
            self.dlg.pushButton_3.clicked.connect(self.import7)
            self.dlg.pushButton_25.clicked.connect(self.import8)
            self.dlg.pushButton_14.clicked.connect(self.import9)
            self.dlg.pushButton_82.clicked.connect(self.import9_restoration)
            self.dlg.pushButton_15.clicked.connect(self.import10)
            self.dlg.pushButton_83.clicked.connect(self.import10_restoration)
            self.dlg.pushButton_17.clicked.connect(self.import11)
            self.dlg.pushButton_92.clicked.connect(self.import11_restoration)
            self.dlg.pushButton_18.clicked.connect(self.import12)
            self.dlg.pushButton_94.clicked.connect(self.import12_restoration)
            self.dlg.pushButton_19.clicked.connect(self.import13)
            self.dlg.pushButton_103.clicked.connect(self.import13_restoration)
            self.dlg.pushButton_20.clicked.connect(self.import14)
            self.dlg.pushButton_105.clicked.connect(self.import14_restoration)
            self.dlg.pushButton_30.clicked.connect(self.import16)
            self.dlg.pushButton_86.clicked.connect(self.import16_restoration)
            self.dlg.pushButton_32.clicked.connect(self.import17)
            self.dlg.pushButton_85.clicked.connect(self.import17_restoration)
            self.dlg.pushButton_40.clicked.connect(self.import18)
            self.dlg.pushButton_87.clicked.connect(self.import18_restoration)
            self.dlg.pushButton_41.clicked.connect(self.import19)
            self.dlg.pushButton_89.clicked.connect(self.import19_restoration)
            self.dlg.pushButton_43.clicked.connect(self.import20)
            self.dlg.pushButton_98.clicked.connect(self.import20_restoration)
            self.dlg.pushButton_46.clicked.connect(self.import21)
            self.dlg.pushButton_100.clicked.connect(self.import21_restoration)
            self.dlg.pushButton_47.clicked.connect(self.import22)
            self.dlg.pushButton_96.clicked.connect(self.import22_restoration)
            self.dlg.pushButton_48.clicked.connect(self.import23)
            self.dlg.pushButton_95.clicked.connect(self.import23_restoration)
            self.dlg.pushButton_44.clicked.connect(self.import24)
            self.dlg.pushButton_42.clicked.connect(self.import25)
            self.dlg.pushButton_101.clicked.connect(self.import25_restoration)
            self.dlg.pushButton_51.clicked.connect(self.import26)
            self.dlg.pushButton_106.clicked.connect(self.import26_restoration)
            #self.dlg.pushButton_53.clicked.connect(self.import27)
            self.dlg.pushButton_108.clicked.connect(self.import27_restoration)
            self.dlg.pushButton_50.clicked.connect(self.import28)
            self.dlg.pushButton_102.clicked.connect(self.import28_restoration)
            

            self.dlg.pushButton.clicked.connect(self.substract1)
            self.dlg.pushButton_59.clicked.connect(self.substract1_restoration)
            self.dlg.pushButton_4.clicked.connect(self.substract2)
            self.dlg.pushButton_60.clicked.connect(self.substract2_restoration)
            self.dlg.pushButton_9.clicked.connect(self.substract3)
            self.dlg.pushButton_63.clicked.connect(self.substract3_restoration)
            self.dlg.pushButton_10.clicked.connect(self.substract4)
            self.dlg.pushButton_67.clicked.connect(self.substract4_restoration)
            self.dlg.pushButton_11.clicked.connect(self.substract5)
            self.dlg.pushButton_62.clicked.connect(self.substract5_restoration)
            self.dlg.pushButton_12.clicked.connect(self.substract6)
            self.dlg.pushButton_65.clicked.connect(self.substract6_restoration)
            self.dlg.pushButton_13.clicked.connect(self.substract7)
            self.dlg.pushButton_64.clicked.connect(self.substract7_restoration)
            self.dlg.pushButton_16.clicked.connect(self.substract8)
            self.dlg.pushButton_81.clicked.connect(self.substract8_restoration)
            self.dlg.pushButton_31.clicked.connect(self.substract9)
            self.dlg.pushButton_90.clicked.connect(self.substract9_restoration)
            self.dlg.pushButton_39.clicked.connect(self.substract10)
            self.dlg.pushButton_88.clicked.connect(self.substract10_restoration)
            self.dlg.pushButton_45.clicked.connect(self.substract11)
            self.dlg.pushButton_97.clicked.connect(self.substract11_restoration)
            
            self.dlg.pushButton_23.clicked.connect(self.import_flood)
            self.dlg.pushButton_24.clicked.connect(self.create_attribute_table)
            self.dlg.pushButton_26.clicked.connect(self.hydrology_add_attribute_table)
            self.dlg.pushButton_27.clicked.connect(self.hydraulics_add_attribute_table)
            self.dlg.pushButton_33.clicked.connect(self.hydraulics_extra_add_attribute_table)
            self.dlg.pushButton_28.clicked.connect(self.ecology_add_attribute_table)
            self.dlg.pushButton_49.clicked.connect(self.ecology_extra_add_attribute_table)
            self.dlg.pushButton_29.clicked.connect(self.socio_economics_add_attribute_table)
            self.dlg.pushButton_52.clicked.connect(self.socio_economics_extra_add_attribute_table)
            self.dlg.pushButton_34.clicked.connect(self.FEM_minimum_add_attribute_table)
            self.dlg.pushButton_55.clicked.connect(self.FEM_extra_add_attribute_table)
            self.dlg.pushButton_37.clicked.connect(self.load_treshold_defaults)
            self.dlg.pushButton_54.clicked.connect(self.load_extra_treshold_defaults)
            #self.dlg.pushButton_35.clicked.connect(self.select_fp)
            self.dlg.pushButton_35.clicked.connect(self.load_AFP_defaults)
            self.dlg.pushButton_36.clicked.connect(self.confirm_values)
            self.dlg.pushButton_135.clicked.connect(self.confirm_values_restoration)
            self.dlg.pushButton_57.clicked.connect(self.confirm_extra_values)
            self.dlg.pushButton_137.clicked.connect(self.confirm_extra_values_restoration)
            self.dlg.pushButton_38.clicked.connect(self.calculate_FEM)
            self.dlg.pushButton_134.clicked.connect(self.calculate_FEM_restoration)
            self.dlg.pushButton_56.clicked.connect(self.calculate_extra_FEM)
            self.dlg.pushButton_136.clicked.connect(self.calculate_extra_FEM_restoration)
            self.dlg.pushButton_109.clicked.connect(self.restoration_decision)
            
            
            
            
            
        # Fetch the currently loaded layers
        #layers = QgsProject.instance().layerTreeRoot().children()
        # Clear the contents of the comboBox from previous runs
        self.dlg.mMapLayerComboBox.clear()
        # Populate the comboBox with names of all the loaded layers
        #self.dlg.mMapLayerComboBox.addItems([layer.name() for layer in layers])
        #self.dlg.comboBox_2.addItems([layer.name() for layer in layers])

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            filename = self.dlg.lineEdit.text()
            with open(filename, 'w') as output_file:
              selectedLayerIndex = self.dlg.mMapLayerComboBox.currentIndex()
              selectedLayer = layers[selectedLayerIndex].layer()
              fieldnames = [field.name() for field in selectedLayer.fields()]
              # write header
              line = ','.join(name for name in fieldnames) + '\n'
              output_file.write(line)
              
              #write feature attributes
              for f in selectedLayer.getFeatures():
              	line = ','.join(str(f[name]) for name in fieldnames) + '\n'
              	output_file.write(line)
                
            self.iface.messageBar().pushMessage("Success", "Output file written at " + filename, level=Qgis.Success, duration=3)        
            
            #end            
            	
