from PyQt5.QtGui import QImage
from nodeeditor.node_graphics_node import QDMGraphicsNode
from qtpy.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QGridLayout
from qtpy.QtCore import Qt
from sqlalchemy.engine import create_engine
from conf import *
from nodes.bases.ai_node_base import AiNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException
from qtpy.QtGui import QImage
from qtpy.QtCore import QRectF

from sqlalchemy.orm import Session

class DatabaseGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 350
        self.height = 400
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()
        self.icons = QImage("icons/status_icons.png")

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        offset = 24.0
        if self.node.isDirty(): offset = 0.0
        if self.node.isInvalid(): offset = 48.0

        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        )

class DatabaseQueryContent(QDMNodeContentWidget):
    def initUI(self):
        self.layout = QGridLayout(self)
        self.edit = QLineEdit("SELECT * FROM detections", self)
        self.edit.setAlignment(Qt.AlignCenter)
        self.edit.setObjectName(self.node.content_label_objname)
        self.layout.addWidget(self.edit, 0, 0)
        self.table = QTableWidget(10, 5, self)
        # self.table.setColumnCount(len(colors[0]) + 1)
        self.table.setHorizontalHeaderLabels(["ID", "Frame Num", "x1", "y1", "x2", "y2"])
        self.layout.addWidget(self.table,1,0,1,2)

    def updateTable(self, detections):
        self.table.setRowCount(len(detections))
        for num, detection in enumerate(detections):
            item_name = QTableWidgetItem(str(detection.id))
            item_code = QTableWidgetItem(str(detection.frame_num))
            item_color = QTableWidgetItem(str(detection.x1))
            self.table.setItem(num, 1, item_code)
            self.table.setItem(num, 0, item_name)
            self.table.setItem(num, 2, item_color)      
    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res

@register_node(DATABASE_NODE)
class DatabaseNode(AiNode):
    icon = "icons/out.png"
    op_code = DATABASE_NODE
    op_title = "SQL TABLE"
    content_label_objname = "ai_node_database"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[2, 3])
        # TODO Create random or unused filename 
        self.engine = create_engine('sqlite:///temp/sqlalchemy.db')
        self.session = Session(self.engine)
        self.session.expire_on_commit = False
        self.model_type = None
        self.eval()
    
    def initInnerClasses(self):
        self.content = DatabaseQueryContent(self)
        self.grNode = DatabaseGraphicsNode(self)
        self.content.edit.textChanged.connect(self.runQuery)

    def fillDatabase(self, detections):
        self.model_type = type(detections[0])
        # WTH Man
        try:
            self.model_type.__table__.drop(self.engine)
        except:
            pass
        finally:
            self.model_type.__table__.create(self.engine)

        for detection in detections:
            self.session.add(detection)
        self.session.commit()


    def runQuery(self):
        try:
            query = self.content.edit.text()
            rs = self.session.execute(query)
            self.content.updateTable(rs)
        except Exception as e:
            pass
        

    def evalImplementation(self):
        detector = self.getInput(0)
        if not detector:
            self.grNode.setToolTip("Input is not connected")
            self.markInvalid()
            return
        if not ("detector" in detector.content_label_objname):
            self.grNode.setToolTip("Input is an invalid")
            self.markInvalid()
            return

        self.fillDatabase(detector.getDetections())
        self.runQuery()

        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.grNode.setToolTip("")

        self.evalChildren()

        return None