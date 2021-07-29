import os, sys
from qtpy.QtWidgets import QApplication
from PyQt5.QtWidgets import *

from ai_editor_window import AiEditorWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    wnd = AiEditorWindow()
    wnd.show()
    sys.exit(app.exec_())

