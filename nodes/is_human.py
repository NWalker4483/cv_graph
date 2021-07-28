from nodes.bases.detector_node_base import DetectorGraphicsNode, DetectorNode
from os.path import exists
from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import Qt
from conf import * 

from nodes.bases.ai_node_base import AiNode, AiGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException
import os

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


@register_node(IS_HUMAN_NODE)
class Node_Input(DetectorNode):
    icon = "icons/in.png"
    op_code = IS_HUMAN_NODE
    op_title = "Contains People"
    content_label_objname = "ai_detector_human"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1,2], outputs=[2])
       
        self.eval()

    def initInnerClasses(self):
        self.content = InputContent(self)
        self.grNode = DetectorGraphicsNode(self)

    def evalImplementation(self):
        video_node = self.getInput(0)
        if not video_node:
            self.grNode.setToolTip("Input is not connected")
            self.markInvalid()
            return
        if not (video_node.op_code == VIDEO_NODE):
            self.grNode.setToolTip("Input is an invalid")
            self.markInvalid()
            return
        detector_node = self.getInput(0)
        if not detector_node:
            self.grNode.setToolTip("Input is not connected")
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
