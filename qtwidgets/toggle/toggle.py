import sys

if 'PyQt5' in sys.modules:
    from PyQt5.QtCore import (
        Qt, QSize, QPoint, QPointF, QRectF,
        QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup, Q_ENUMS)
    from PyQt5.QtWidgets import QCheckBox
    from PyQt5.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter

    from PyQt5.QtCore import pyqtSlot as Slot, pyqtProperty as Property

else:
    from PySide2.QtCore import (
        Qt, QSize, QPoint, QPointF, QRectF,
        QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup,
        Slot, Property)

    from PySide2.QtWidgets import QCheckBox
    from PySide2.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter

import pydevd_pycharm

pydevd_pycharm.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True)


class HandleInvertedModeEnum:
    straight = 0
    inverted = 1


class Toggle(QCheckBox):
    Q_ENUMS(HandleInvertedModeEnum)
    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)

    def __init__(self,
                 parent=None
                 ):
        super().__init__(parent)
        self._pulse_radius = 0

        self._handle_color = self._handle_color_default = QColor('white')
        self._checked_color = self._checked_color_default = QColor("#00B0FF")
        self._bar_color = self._bar_color_default = QColor('gray')
        self._bar_brush = QBrush(self._bar_color)
        self._bar_checked_brush = QBrush(QColor(self._checked_color).lighter())
        self._handle_brush = QBrush(self._handle_color)
        self._handle_checked_brush = QBrush(QColor(self._checked_color))

        self._handle_size_factor = self._handle_size_factor_default = 24
        self.handle_size = self._handle_size_factor / 100
        self.setContentsMargins(8, 0, 8, 0)
        self._start_position, self._end_position = 0, 1
        self._handle_position = self._start_position
        self._handle_inverted_mode = HandleInvertedModeEnum.straight

        self.stateChanged.connect(self.handle_state_change)

    def reset_checked_color(self):
        self.set_checked_color(self._checked_color_default)
        return self._checked_color_default

    def get_checked_color(self):
        return self._checked_color

    @Slot(QColor)
    def set_checked_color(self, color):
        self._checked_color = color
        lightness_factor_color = color.lightness()
        if lightness_factor_color * 1.5 >= 200:
            lightness_factor_color = 90
        else:
            lightness_factor_color = 150
        self._bar_checked_brush = self._create_brush(color.lighter(factor=lightness_factor_color)) # note: its necessary redeclare as QColor in order to make it lighter
        self._handle_checked_brush = self._create_brush( color)
        self.update()

    checked_color = Property(QColor, fset=set_checked_color, fget=get_checked_color, freset=reset_checked_color)


    def reset_bar_color(self):
        self.set_bar_color(self._bar_color_default)
        return self._bar_color_default

    def get_bar_color(self):
        return self._bar_color

    @Slot(QColor)
    def set_bar_color(self, color):
        self._bar_color = color
        self._bar_brush = self._create_brush( color)
        self.update()

    bar_color = Property(QColor, fset=set_bar_color, fget=get_bar_color, freset=reset_bar_color)


    def reset_handle_color(self):
        self.set_handle_color(self._handle_color_default)
        return self._handle_color_default

    def get_handle_color(self):
        return self._handle_color

    @Slot(QColor)
    def set_handle_color(self, color):
        self._handle_color = color
        self._handle_brush = self._create_brush( color)
        self.update()

    handle_color = Property(QColor, fset=set_handle_color, fget=get_handle_color, freset=reset_handle_color)

    def _create_brush(self, color):
        return QBrush(color)

    def sizeHint(self):
        return QSize(58, 45)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e: QPaintEvent):

        contRect = self.contentsRect()
        handleRadius = round(self._handle_size_factor * contRect.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.40 * contRect.height()
        )
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2

        # the handle will move along this line
        trailLength = contRect.width() - 2 * handleRadius
        xPos = contRect.x() + handleRadius + trailLength * self._handle_position

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)

        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)

        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)

        p.end()

    @Property(HandleInvertedModeEnum)
    def inverted_mode(self):
        return self._handle_inverted_mode

    @inverted_mode.setter
    def inverted_mode(self, value):
        if self._handle_inverted_mode != value:
            self._handle_inverted_mode = value
            self._start_position, self._end_position = self._end_position, self._start_position
            self.setProperty('handle_position', value)
            self.update()

    @Slot(int)
    def handle_state_change(self, value):
        self._handle_position = self._end_position if value else self._start_position

    @Property(float, designable=False)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        """change the property
        we need to trigger QWidget.update() method, either by:
            1- calling it here [ what we're doing ].
            2- connecting the QPropertyAnimation.valueChanged() signal to it.
        """
        self._handle_position = pos
        self.update()

    def get_handle_size_factor(self):
        return self._handle_size_factor

    @Slot(int)
    def set_handle_size_factor(self, factor):
        """change the property
        we need to trigger QWidget.update() method, either by:
            1- calling it here [ what we're doing ].
            2- connecting the QPropertyAnimation.valueChanged() signal to it.
        """
        self._handle_size_factor = factor
        self.handle_size = factor / 100
        self.update()

    def reset_handle_size_factor(self):
        self.set_handle_size_factor(self._handle_size_factor_default)

    handle_size_factor = Property(int, fset=set_handle_size_factor, fget=get_handle_size_factor,
                                  freset=reset_handle_size_factor)

    @Property(float, designable=False)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()


class AnimatedToggle(Toggle):
    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)

    def __init__(self, *args, pulse_unchecked_color="#44999999", pulse_checked_color="#4400B0EE", **kwargs):

        self._pulse_radius = 0

        super().__init__(*args, **kwargs)

        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(200)  # time in ms

        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setDuration(350)  # time in ms
        self.pulse_anim.setStartValue(10)
        self.pulse_anim.setEndValue(20)

        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)
        self.animations_group.addAnimation(self.pulse_anim)

        self._pulse_unchecked_animation = QBrush(QColor(pulse_unchecked_color))
        self._pulse_checked_animation = QBrush(QColor(pulse_checked_color))

    @Slot(int)
    def handle_state_change(self, value):
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(self._end_position)
        else:
            self.animation.setEndValue(self._start_position)
        self.animations_group.start()

    def paintEvent(self, e: QPaintEvent):

        contRect = self.contentsRect()
        handleRadius = round(self.handle_size * contRect.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.40 * contRect.height()
        )
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2

        # the handle will move along this line
        trailLength = contRect.width() - 2 * handleRadius

        xPos = contRect.x() + handleRadius + trailLength * self._handle_position

        if self.pulse_anim.state() == QPropertyAnimation.Running:
            p.setBrush(
                self._pulse_checked_animation if
                self.isChecked() else self._pulse_unchecked_animation)
            p.drawEllipse(QPointF(xPos, barRect.center().y()),
                          self._pulse_radius, self._pulse_radius)

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)

        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)

        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)

        p.end()
