from nodes.bases.detector_node_base import DetectorGraphicsNode, DetectorNode
from os.path import exists
from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import Qt
from conf import * 

from nodes.bases.ai_node_base import AiNode, AiGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException


@register_node(IS_HUMAN_NODE)
class Node_Input(DetectorNode):
    icon = "icons/in.png"
    op_code = IS_HUMAN_NODE
    op_title = "Contains People"
    content_label_objname = "ai_detector_human"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1,2], outputs=[2])
       
        self.eval()
