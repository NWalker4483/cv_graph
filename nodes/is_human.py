from os.path import exists
from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import Qt
from conf import IS_HUMAN, MOTION_TRACK_NODE, YOLO_V4_NODE, register_node, VIDEO_NODE

from nodes.bases.ai_node_base import AiNode, AiGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException
import os


import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import cv2
import utils.common as bb
# A Python based implementation of the algorithm described on https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6928767/ s

class InputContent(QDMNodeContentWidget):
    def initUI(self):
        pass

    def serialize(self):
        res = super().serialize()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node(IS_HUMAN)
class Node_Input(AiNode):
    icon = "icons/in.png"
    op_code = IS_HUMAN
    op_title = "Contains People"
    content_label_objname = "ai_node_human"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1,2], outputs=[2])
       
        self.eval()

    def initInnerClasses(self):
        self.content = InputContent(self)
        self.grNode = AiGraphicsNode(self)

    def evalImplementation(self):
        input_node = self.getInput(0)
        if not input_node:
            self.grNode.setToolTip("Input is not connected")
            self.markInvalid()
            return
        if not (input_node.op_code == VIDEO_NODE):
            self.grNode.setToolTip("Input is an invalid")
            self.markInvalid()
            return


        # TODO: LOAD FRAMES
        self.value = 0
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.grNode.setToolTip("")

        self.evalChildren()

        return self.value
