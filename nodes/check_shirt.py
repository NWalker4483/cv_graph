from conf import *
from nodes.bases.ai_node_base import AiNode

# A Python based implementation of the algorithm described on https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6928767/ s


@register_node(CHECK_SHIRT_NODE)
class ShirtCheckerNode(AiNode):
    icon = "icons/in.png"
    op_code = CHECK_SHIRT_NODE
    op_title = "Check Shirt Color"
    content_label_objname = "ai_node_shirt"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1,2], outputs=[2])
       
        self.eval()
