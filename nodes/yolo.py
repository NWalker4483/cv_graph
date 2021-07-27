from os.path import exists
from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import Qt
from conf import YOLO_V4_NODE, register_node, VIDEO_NODE

from nodes.bases.ai_node_base import AiNode, AiGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException
# ssfrom imageai.Detection import ObjectDetection
import os


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


@register_node(YOLO_V4_NODE)
class Node_Input(AiNode):
    icon = "icons/in.png"
    op_code = YOLO_V4_NODE
    op_title = "YoloV4"
    content_label_objname = "ai_node_yolo"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[2])
        execution_path = os.getcwd()
        # self.detector = ObjectDetection()
        # self.detector.setModelTypeAsTinyYOLOv3()
        # self.detector.setModelPath(os.path.join(execution_path, "yolo-tiny.h5"))
        # self.detector.loadModel()
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
        if (input_node.op_code != VIDEO_NODE) or input_node.isInvalid():
            self.grNode.setToolTip("Input node is invalid")
            self.markInvalid()
            return
            
        execution_path = os.getcwd()
        # detections = self.detector.detectObjectsFromImage(input_image=os.path.join(
        #     execution_path, input_node.value), output_image_path=os.path.join(execution_path, "new.jpg"), minimum_percentage_probability=30)

        # for eachObject in detections:
        #     print(eachObject["name"], " : ", eachObject["percentage_probability"],
        #           " : ", eachObject["box_points"])
        #     print("--------------------------------")
    
        # TODO: LOAD FRAMES
        self.value = 0
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.grNode.setToolTip("")

        self.evalChildren()

        return self.value
