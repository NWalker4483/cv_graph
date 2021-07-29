
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton, QGridLayout
from nodeeditor.node_graphics_node import QDMGraphicsNode
from qtpy.QtWidgets import QLabel
from conf import *
from nodes.bases.ai_node_base import AiGraphicsNode, AiNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException
from qtpy.QtGui import QImage
from qtpy.QtCore import QRectF
from qtpy.QtCore import Qt

class DatabaseGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 500
        self.height = 500
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

class GalleryInputContent(QDMNodeContentWidget):
    def initUI(self):
        self._next = QPushButton('next', self)
        self._prev = QPushButton('previous', self)
        self.gallery_index = 0
        self.image_frame = QLabel(parent=self)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self._next, 1, 1)
        self.layout.addWidget(self._prev, 1, 2)
        self.layout.addWidget(self.image_frame, 2, 1, 1, 2)

        # self.edit = QLineEdit("SELECT * FROM detections", self)
        # self.edit.setAlignment(Qt.AlignCenter)
        # self.edit.setObjectName(self.node.content_label_objname)
        # self.layout.addWidget(self.edit, 0, 0)
        # self.table = QTableWidget(10, 5, self)
        # # self.table.setRowCount(len(colors))
        # # self.table.setColumnCount(len(colors[0]) + 1)
        # self.table.setHorizontalHeaderLabels(["ID", "Frame Num", "x1", "y1", "x2", "y2"])
        # self.layout.addWidget(self.table,1,0,1,2)

    def updateDisplay(self, frame):
        self.image = frame
        self.image = QImage(self.image.data, self.image.shape[1], self.image.shape[0], QImage.Format_RGB888).rgbSwapped()
        self.image_frame.setPixmap(QPixmap.fromImage(self.image))

    def serialize(self):
        res = super().serialize()
        res['gallery_index'] = self.gallery_index
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            self.gallery_index = data['gallery_index']
            return True & res
        except Exception as e:
            dumpException(e)
        return res

@register_node(GALLERY_NODE)
class GalleryNode(AiNode):
    icon = "icons/out.png"
    op_code = GALLERY_NODE
    op_title = "Detection Gallery"
    content_label_objname = "ai_node_gallery"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 2], outputs=[])
        self.gallery_index = 0
        self.eval()
    
    def initInnerClasses(self):
        self.content = GalleryInputContent(self)
        self.grNode = DatabaseGraphicsNode(self)
        
        self.content._next.clicked.connect(self.next_img)
        self.content._prev.clicked.connect(self.prev_img)

    def next_img(self):
        self.gallery_index += 1
        self.gallery_index = self.gallery_index if self.gallery_index <= 10 else 10
        self.show_img()

    def prev_img(self):
        self.gallery_index -= 1
        self.gallery_index = self.gallery_index if self.gallery_index >= 0 else 0
        self.show_img()

    def show_img(self):
        input_node = self.getInput(0)
        if not input_node:
            self.grNode.setToolTip("Input is not connected")
            self.markInvalid()
            return
        if (input_node.op_code != VIDEO_NODE) or input_node.isInvalid():
            self.grNode.setToolTip("Input is an invalid")
            self.markInvalid()
            return

        detector = self.getInput(1)
        if not detector:
            self.grNode.setToolTip("Input is not connected")
            self.markInvalid()
            return

        if not ("detector" in detector.content_label_objname):
            self.grNode.setToolTip("Input is an invalid")
            self.markInvalid()
            return
        
        det = detector.getDetections()
        if len(det) > 0:
            frame_num = det[self.gallery_index].frame_num
            img = input_node.grabFrame(frame_num)
            if type(img) != type(None):
                self.content.updateDisplay(img)

                self.markDirty(False)
                self.markInvalid(False)

                self.markDescendantsInvalid(False)
                self.markDescendantsDirty()

                self.grNode.setToolTip("")
    def evalImplementation(self):
        input_node = self.getInput(0)
        if not input_node:
            self.grNode.setToolTip("Input is not connected")
            self.markInvalid()
            return
        if (input_node.op_code != VIDEO_NODE) or input_node.isInvalid():
            self.grNode.setToolTip("Input is an invalid")
            self.markInvalid()
            return

        detector = self.getInput(1)
        if not detector:
            self.grNode.setToolTip("Input is not connected")
            self.markInvalid()
            return
        if not ("detector" in detector.content_label_objname):
            self.grNode.setToolTip("Input is an invalid")
            self.markInvalid()
            return
        self.gallery_index = 0 
        detector.getDetections()
        img = input_node.grabFrame(50)
        if type(img) != type(None):
            self.content.updateDisplay(img)

            self.markDirty(False)
            self.markInvalid(False)

            self.markDescendantsInvalid(False)
            self.markDescendantsDirty()

            self.grNode.setToolTip("")
        else:
            print
            self.markDirty()

        return None