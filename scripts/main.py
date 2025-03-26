import sys
import os

path_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(path_root)
# sys.path.insert(0, config.LIB_DIR)




from ui.main_controller import MainController


if __name__ == "__main__":
    main_ctrl = MainController()
    main_ctrl.launch()
