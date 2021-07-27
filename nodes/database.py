from models.detection import Base
from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import Qt
from sqlalchemy.engine import create_engine
from conf import NODE_DATABASE, register_node, VIDEO_NODE
from nodes.bases.ai_node_base import AiNode, AiGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException


class CalcInputContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit("SELECT * FROM detections", self)
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

from os.path import exists

@register_node(NODE_DATABASE)
class CalcNode_Input(AiNode):
    icon = "icons/out.png"
    op_code = NODE_DATABASE
    op_title = "SQL DATABASE"
    content_label_objname = "ai_node_database"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[3])
        self.width = 300 
        self.height = 600
        self.engine =  create_engine('sqlite:///sqlalchemy_example.db')
        Base.metadata.create_all(self.engine)
        self.eval()
    
    def initInnerClasses(self):
        self.content = CalcInputContent(self)
        self.grNode = AiGraphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)

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
        print(detector.getDetections())

        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.grNode.setToolTip("")

        self.evalChildren()

        return None