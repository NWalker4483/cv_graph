from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import Qt
from conf import register_node, VIDEO_NODE

from nodes.bases.ai_node_base import AiContent, AiNode, AiGraphicsNode
from nodeeditor.utils import dumpException
import cv2
from os.path import exists

class InputContent(AiContent):
    def initUI(self):
        self.edit = QLineEdit("", self)
        self.edit.setAlignment(Qt.AlignCenter)
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
class VideoInputNode(AiNode):
    icon = "icons/in.png"
    op_code = VIDEO_NODE
    op_title = "Video Loader"
    content_label_objname = "ai_node_video"
    NodeContent_class = InputContent

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[1])
        self.cap = None
        self.markDirty()
        
    def resetVideo(self):
        pass

    def grabNextFrame(self):
        pass

    def grabFrame(self, frame_num):
        # TODO Preserve Cap
        self.cap = cv2.VideoCapture(self.value)
        #if self.cap.get(7) > frame_num:
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num - 1)
        ret, frame = self.cap.read()
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