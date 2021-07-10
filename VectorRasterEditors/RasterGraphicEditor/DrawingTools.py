from PyQt5.QtWidgets import QMainWindow, QColorDialog, QDialog, QLabel, QLineEdit, QPushButton,QSpinBox
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QIcon, QImage, QClipboard, QPen
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtWidgets import QApplication, QUndoStack, QUndoCommand

#Базовый класс для инструментов
class ToolController:
    def __init__(self,window):
        self.main_window = window
        self.main_surface = window.drawing_surface
    def mouse_press_handler(self, event):
        pass
    def mouse_move_handler(self, event):
        pass
    def mouse_release_handler(self, event):
        pass
    def activation_this_tool(self):
        pass
    def deactivation_this_tool(self):
        self.clear_tool_surface()
    def clear_tool_surface(self):
        self.main_window.tool_surface.fill(QColor(0, 0, 0, 0))
    def apply_changes_ds(self):
        pass
    def apply_changes_ts(self):
        pass



#Базовый класс, отвечающий за рисование фигур
class ToolController_Figure(ToolController):
    is_draw_start = False
    is_accumulation = False


    def draw_figure(self, painter):
        pass


    def mouse_press_handler(self, event):
        self.point0 = event.pos()
        self.point1 = event.pos()
        self.is_draw_start = True

        # Поскольку размер фигуры задается перемещением мыши, нет смысла дублировать код
        # который отвечает за отрисовку фигуры на буферной поверхности
        self.mouse_move_handler(event)

    def mouse_move_handler(self, event):
        if self.is_draw_start:
            self.point1 = event.pos()
            self.apply_changes_ts()

    def mouse_release_handler(self, event):
        self.is_draw_start = False
        self.point1 = event.pos()
        self.apply_changes_ds()

        print(self.point1)

    def apply_changes_ts(self):
        # Сначала временная поверхность для рисования отчищается в цвет с нулевой прозрачностью
        # Затем на ней рисуется, как будет выглядить фигура при текущих параметрах
        painter_ts = QPainter(self.main_window.tool_surface)
        painter_ts.setPen(self.main_window.tool_data['color'])

        if (not self.is_accumulation):
            self.clear_tool_surface()

        self.draw_figure(painter_ts)
        self.main_window.update()
    def apply_changes_ds(self):
        painter_ds = QPainter(self.main_window.drawing_surface)
        painter_ds.setPen(self.main_window.tool_data['color'])
        painter_ds.drawPixmap(QPoint(), self.main_window.tool_surface)
        self.main_window.update()
        UndoRedoController.undo_redo_stack.push(UndoRedoCommand())



#Инструмент, отвечающий за рисование прямоугольника
class ToolController_Figure_Rectangle(ToolController_Figure):
    def draw_figure(self, painter):
        rect = QRect(self.point0, self.point1)
        painter.drawRect(rect.normalized())


#Инструмент, отвечающий за рисование эллипса
class ToolController_Figure_Ellipse(ToolController_Figure):
    def draw_figure(self, painter):
        rect = QRect(self.point0, self.point1)
        painter.drawEllipse(rect)


#Инструмент, отвечающий за рисование прямой
class ToolController_Figure_Line(ToolController_Figure):
    def draw_figure(self, painter):
        painter.drawLine(self.point0, self.point1)


#Инструмент, отвечающий за рисование точки
class ToolController_Figure_Point(ToolController_Figure):
    def __init__(self,window):
        super(ToolController_Figure_Point, self).__init__(window)
        self.is_accumulation = True

    def draw_figure(self, painter):
        painter.drawLine(self.point0, self.point1)

    def mouse_move_handler(self,event):
        if self.is_draw_start:
            self.point0 = self.point1
        super(ToolController_Figure_Point, self).mouse_move_handler(event)






class ToolController_Fill(ToolController):

    def mouse_press_handler(self, event):
        self.apply_changes_ts(event)

    def mouse_release_handler(self, event):
        self.apply_changes_ds()


    def apply_changes_ds(self):
        painter = QPainter(self.main_window.drawing_surface)
        # painter.drawImage(QPoint(), self.main_window.drawing_surface)
        painter.setPen(self.main_window.tool_data['color'])
        painter.drawPixmap(QPoint(), self.main_window.tool_surface)

        self.main_window.update()
        UndoRedoController.undo_redo_stack.push(UndoRedoCommand())
    def apply_changes_ts(self,event):
        # Сначала временная поверхность для рисования отчищается в цвет с нулевой прозрачностью
        # Затем на ней рисуется исходное изображение, но с заливкой, как будет выглядить фигура при текущих параметрах
        painter = QPainter(self.main_window.tool_surface)
        painter.begin(self.main_window.tool_surface)
        painter.setPen(self.main_window.tool_data['color'])

        self.main_window.tool_surface.fill(QColor(0, 0, 0, 0))

        # Сама заливка
        image = self.main_window.drawing_surface
        set_checked = set()
        set_for_check = set()
        set_for_check.add((event.pos().x(), event.pos().y()))

        while True:
            self.fill(image, painter, image.pixelColor(event.pos()), set_checked, set_for_check, set_for_check.pop())
            if len(set_for_check) == 0:
                break

        painter.end()

        self.main_window.update()




    def fill(self, image, painter, right_color, set_checked,set_for_check,pos):
        set_checked.add(pos)
        painter.drawPoint(int(pos[0]), int(pos[1]))

        for i in (-1,0,1):
            for j in (-1,0,1):
                if not ((pos[0]+i,pos[1]+j) in set_checked) and pos[0]>=0 and pos[1]>=0 and pos[0]<image.width() and pos[1]<image.height() and not (abs(i)==abs(j)):
                    if image.pixelColor(pos[0]+i,pos[1]+j).getRgb() == right_color.getRgb():
                        set_for_check.add((pos[0]+i,pos[1]+j))







class ToolController_Select(ToolController):
    #Процесс выбора. -1=ничего не выбрано,0=выбирается,1=что-то выбрано
    selecting=-1

    selected_image = 0


    def __init__(self,window):
        super(ToolController_Select, self).__init__(window)
        ToolController_Select.selected_image = QImage(QPixmap())

    def mouse_press_handler(self, event):
        if self.selecting==-1:
            self.selecting=0
            self.point0 = event.pos()
            self.point1 = event.pos()

    def mouse_move_handler(self, event):
        if self.selecting==0:
            self.point1 = event.pos()

            self.apply_changes_ts()

            self.main_window.update()

    def mouse_release_handler(self, event):
        if self.selecting == 0:
            self.selecting=-1
            self.point1 = event.pos()

            ToolController_Select.selected_image=self.main_window.drawing_surface.copy(QRect(self.point0, self.point1))

            self.apply_changes_ds()

            self.main_window.draw_tools["move"].move_start_point=self.point0
            self.main_window.draw_tools["move"].move_now_point=self.point0
            self.main_window.changeTool('move')
            self.main_window.update()
            #UndoRedoController.undo_redo_stack.push(UndoRedoCommand())
    def apply_changes_ds(self):
        painter = QPainter(self.main_window.drawing_surface)
        painter.begin(self.main_window.drawing_surface)

        black_image = QImage(self.selected_image)
        black_image.fill(Qt.black)
        painter.setPen(Qt.white)
        painter.drawImage(self.point0, black_image)

        painter.end()
    def apply_changes_ts(self):
        # Сначала временная поверхность для рисования отчищается в цвет с нулевой прозрачностью
        # Затем на ней рисуется, как будет выглядить фигура при текущих параметрах
        painter = QPainter(self.main_window.tool_surface)
        painter.begin(self.main_window.tool_surface)

        self.clear_tool_surface()

        painter.setPen(QPen(Qt.black, 2, Qt.DashLine))
        rect = QRect(self.point0, self.point1)
        painter.drawRect(rect.normalized())

        painter.end()



class ToolController_Move(ToolController):

    #Включен ли режим перемещения
    is_moving=False

    move_start_point=QPoint()
    move_now_point=QPoint()


    #def __init__(self,window):
        #super(ToolController_Move, self).__init__(window)

    def mouse_press_handler(self, event):
        rect = ToolController_Select.selected_image.rect()
        rect.moveTo(self.move_now_point)
        if not rect.intersects(QRect(event.pos(), event.pos())):

            self.is_moving = False
            self.main_window.changeTool('select')
        else:
            self.move_start_point = event.pos()
            self.move_now_point = event.pos()

            self.is_moving = True

    def mouse_move_handler(self, event):
        if self.is_moving==1:
            self.move_now_point=event.pos()
            self.apply_changes_ts()


    def mouse_release_handler(self, event):
        if self.is_moving:
            self.move_now_point = event.pos()
            self.is_moving = False

    def apply_changes_ds(self):
        painter = QPainter(self.main_window.drawing_surface)

        painter.setPen(Qt.white)
        painter.drawImage(self.move_now_point, ToolController_Select.selected_image)

        self.main_window.update()
        UndoRedoController.undo_redo_stack.push(UndoRedoCommand())
    def apply_changes_ts(self):
        # Сначала временная поверхность для рисования отчищается в цвет с нулевой прозрачностью
        # Затем на ней рисуется, как будет выглядить фигура при текущих параметрах
        painter = QPainter(self.main_window.tool_surface)

        self.clear_tool_surface()

        painter.setPen(Qt.white)
        painter.drawImage(self.move_now_point, ToolController_Select.selected_image)

        painter.setPen(QPen(Qt.black, 2, Qt.DashLine))
        rect = ToolController_Select.selected_image.rect()
        rect.moveTo(self.move_now_point)
        painter.drawRect(rect.normalized())
        self.main_window.update()

    def activation_this_tool(self):
        self.apply_changes_ts()

    def deactivation_this_tool(self):
        super(ToolController_Move, self).deactivation_this_tool()
        self.apply_changes_ds()
        self.is_moving = False



class ToolController_Copy(ToolController):


    def __init__(self,window,select_controller):
        super(ToolController_Copy, self).__init__(window)

    def press_button_handler(self):
        buff = QApplication.clipboard()
        buff.setImage(ToolController_Select.selected_image)



class ToolController_Paste(ToolController):


    def __init__(self,window,move_controller):
        super(ToolController_Paste, self).__init__(window)
        self.move_controller=move_controller

    def press_button_handler(self):
        self.main_window.changeTool("none")

        buff = QApplication.clipboard()
        ToolController_Select.selected_image = buff.image()#.copy(QRect(buff.image.rect()))
        self.move_controller.is_move=False
        self.move_controller.move_start_point = buff.image().rect().topLeft()
        self.move_controller.move_now_point = buff.image().rect().topLeft()
        self.main_window.update()

        self.main_window.changeTool("move")


class ToolController_Cut(ToolController):
    def press_button_handler(self):
        if self.main_window.draw_tool_now_id == 'move':
            buff = QApplication.clipboard()
            buff.setImage(ToolController_Select.selected_image)
            ToolController_Select.selected_image = QImage(QPixmap())
            self.main_window.changeTool("select")
            self.main_window.update()



class ToolController_Delete(ToolController):
    #Включен ли режим удаления
    is_deleting=False
    deleting_zone=QRect(QPoint(),QPoint())

    move_start_point=QPoint()
    move_now_point=QPoint()



    def mouse_press_handler(self, event):
        if event.buttons() & Qt.LeftButton:
            self.is_deleting = True
            self.apply_changes_ds(event)
        if event.buttons() & Qt.RightButton:
            if self.is_deleting==False:
                self.change_deleting_zone_dialog()


    def mouse_move_handler(self, event):
        if self.is_deleting:
            self.apply_changes_ds(event)
        #self.apply_changes_ts(event)


    def mouse_release_handler(self, event):
        if self.is_deleting:
            self.is_deleting = False
            UndoRedoController.undo_redo_stack.push(UndoRedoCommand())

    def apply_changes_ds(self,event):
        painter = QPainter(self.main_window.drawing_surface)

        rect = QRect(self.deleting_zone)
        im=QImage(QPixmap(rect.size()))
        im.fill(QColor(0,0,0,0))
        #rect.moveTo(event.pos())
        painter.drawImage(event.pos(),im)

        self.main_window.update()
    def apply_changes_ts(self,event):
        # Сначала временная поверхность для рисования отчищается в цвет с нулевой прозрачностью
        # Затем на ней рисуется, как будет выглядить фигура при текущих параметрах
        painter = QPainter(self.main_window.tool_surface)
        painter.begin(self.main_window.tool_surface)

        self.clear_tool_surface()

        painter.setPen(QPen(Qt.black, 2, Qt.DashLine))
        rect = QRect(self.deleting_zone)
        rect.moveTo(event.pos())
        painter.drawRect(rect.normalized())

        painter.end()

    def deactivation_this_tool(self):
        self.is_deleting = False
    def change_deleting_zone_dialog(self):
        dlg = QDialog()
        dlg.resize(300, 150)
        windowFlag=0
        windowFlag |= Qt.CustomizeWindowHint
        windowFlag |= Qt.WindowCloseButtonHint
        dlg.setWindowFlags(windowFlag)
        label_h = QLabel("Ширина", dlg)
        label_w = QLabel("Длина", dlg)
        label_h.move(25, 25)
        label_w.move(25, 50)
        line_h = QSpinBox(dlg)
        line_h.setRange(1, 100000)
        line_h.move(100, 25)
        line_h.setValue(self.deleting_zone.height())
        line_w = QSpinBox(dlg)
        line_w.setRange(1, 100000)
        line_w.setValue(self.deleting_zone.width())
        line_w.move(100, 50)
        button_ok = QPushButton(dlg)
        button_ok.setText("Применить")
        button_ok.move(25, 100)
        button_cansel = QPushButton(dlg)
        button_cansel.setText("Отмена")
        button_cansel.move(200, 100)
        button_cansel.clicked.connect(lambda: dlg.reject())
        button_ok.clicked.connect(lambda: dlg.accept())
        button_ok.clicked.connect(lambda: self.change_deleting_zone(int(line_h.value()), int(line_w.value())))
        dlg.setWindowTitle("Задать размер удаляемой области")
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()

    def change_deleting_zone(self,w,h):
        self.deleting_zone.setRect(self.deleting_zone.x(),self.deleting_zone.y(),w,h)




class UndoRedoController:
    stage_stack = []
    stage_now = -1
    main_window = 0
    undo_redo_stack = QUndoStack()

    @staticmethod
    def init(window):
        UndoRedoController.main_window = window
        UndoRedoController.save_stage()

    @staticmethod
    def save_stage():
        s = UndoRedoController
        while len(s.stage_stack)>s.stage_now+1:
            del s.stage_stack[-1]

        s.stage_stack.append(s.main_window.drawing_surface.copy(s.main_window.drawing_surface.rect()))
        s.stage_now+=1

    @staticmethod
    def set_now_stage():
        s = UndoRedoController
        s.main_window.drawing_surface = s.stage_stack[s.stage_now].copy(s.main_window.drawing_surface.rect())
        s.main_window.tool_surface.fill(QColor(0,0,0,0))
        s.main_window.update()

    @staticmethod
    def undo():
        s = UndoRedoController
        if s.stage_now>0:
            s.stage_now-=1
            s.set_now_stage()

    @staticmethod
    def redo():
        s = UndoRedoController
        if s.stage_now<len(s.stage_stack)-1:
            s.stage_now+=1
            s.set_now_stage()


class UndoRedoCommand(QUndoCommand):
    def __init__(self):
        super(UndoRedoCommand, self).__init__()
        UndoRedoController.save_stage()
    def undo(self):
        UndoRedoController.undo()
    def redo(self):
        UndoRedoController.redo()