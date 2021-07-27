from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import Qt
from conf import NODE_DATABASE, register_node, VIDEO_NODE
from nodes.bases.ai_node_base import AiNode, AiGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException


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

from os.path import exists

@register_node(NODE_DATABASE)
class CalcNode_Input(AiNode):
    icon = "icons/out.png"
    op_code = NODE_DATABASE
    op_title = "SQL DATABASE"
    content_label_objname = "ai_node_database"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[])
        self.width = 300 
        self.height = 200
        self.eval()

    def initInnerClasses(self):
        self.content = CalcInputContent(self)
        self.grNode = AiGraphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        u_value = self.content.edit.text()
        assert(exists(u_value))
        # TODO: LOAD FRAMES
        self.value = u_value
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.grNode.setToolTip("")

        self.evalChildren()

        return self.value