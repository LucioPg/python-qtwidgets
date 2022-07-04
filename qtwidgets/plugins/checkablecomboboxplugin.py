#!/usr/bin/env python



from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin
import os
from qtwidgets.checkablecombobox import CheckableComboBox





class  CheckableComboBoxPlugin(QPyDesignerCustomWidgetPlugin):
    """CheckableComboBoxPlugin(QPyDesignerCustomWidgetPlugin)
    
    Provides a Python custom plugin for Qt Designer by implementing the
    QDesignerCustomWidgetPlugin via a PyQt-specific custom plugin class.
    """

    # The __init__() method is only used to set up the plugin and define its
    # initialized variable.
    def __init__(self, parent=None):
    
        super(CheckableComboBoxPlugin, self).__init__(parent)

        self.initialized = False

    # The initialize() and isInitialized() methods allow the plugin to set up
    # any required resources, ensuring that this can only happen once for each
    # plugin.
    def initialize(self, core):

        if self.initialized:
            return

        self.initialized = True

    def isInitialized(self):

        return self.initialized

    # This factory method creates new instances of our custom widget with the
    # appropriate parent.
    def createWidget(self, parent):
        return CheckableComboBox(parent)
        # return Toggle(parent)

    # This method returns the name of the custom widget class that is provided
    # by this plugin.
    def name(self):
        return "CheckableComboBox"
        # return "Toggle"

    # Returns the name of the group in Qt Designer's widget box that this
    # widget belongs to.
    def group(self):
        return "Input Widgets"

    # Returns the icon used to represent the custom widget in Qt Designer's
    # widget box.
    def icon(self):
        return QIcon(icon_path)

    # Returns a short description of the custom widget for use in a tool tip.
    def toolTip(self):
        return ""

    # Returns a short description of the custom widget for use in a "What's
    # This?" help message for the widget.
    def whatsThis(self):
        return ""

    # Returns True if the custom widget acts as a container for other widgets;
    # otherwise returns False. Note that plugins for custom containers also
    # need to provide an implementation of the QDesignerContainerExtension
    # interface if they need to add custom editing support to Qt Designer.
    def isContainer(self):
        return False

    # Returns an XML description of a custom widget instance that describes
    # default values for its properties. Each custom widget created by this
    # plugin will be configured using this description.
    def domXml(self):
        return (
            '<widget class="CheckableComboBox" name=\"checkable_combobox\">\n'
            "</widget>\n"
        )


    # Returns the module containing the custom widget class. It may include
    # a module path.
    def includeFile(self):
        return "qtwidgets.checkablecombobox"


icon_path = os.path.join(os.path.dirname((os.path.dirname(__file__))),'checkablecombobox','icons', 'checkable_icon.png')

