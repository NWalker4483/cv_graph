from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import Qt
from conf import register_node, VIDEO_NODE

from nodes.bases.ai_node_base import AiNode, AiGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException
import cv2
from os.path import exists

class CalcInputContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit("", self)
        self.edit.setAlignment(Qt.AlignLeft)
        self.edit.setObjectName(self.node.content_label_objname)

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

@register_node(VIDEO_NODE)
class CalcNode_Input(AiNode):
    icon = "icons/in.png"
    op_code = VIDEO_NODE
    op_title = "Video Loader"
    content_label_objname = "ai_node_video"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[1])
        self.cap = None
        self.eval()

    def initInnerClasses(self):
        self.content = CalcInputContent(self)
        self.grNode = AiGraphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)
    
    def grabFrame(self, frame_num):
        # TODO Preserve Cap
        self.cap = cv2.VideoCapture(self.value)
        if self.cap.get(7) > frame_num:
            self.cap.set(1, frame_num)
            ret, frame = self.cap.read()
            if ret:
                return frame

    def evalImplementation(self):
        u_value = self.content.edit.text()
        if not exists(u_value):
            self.grNode.setToolTip(f"Video File {u_value} does not exist")
            assert(exists(u_value)) #TODO Change to raise

        self.cap = cv2.VideoCapture(u_value)
        assert(self.cap.isOpened())
        self.cap.release()
        self.value = u_value
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.grNode.setToolTip("")

        self.evalChildren()

        return self.value