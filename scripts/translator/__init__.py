# import os
# import importlib

# for filename in os.listdir(os.path.dirname(__file__)):
#     if filename.endswith(".py") and filename != "__init__.py":
#         module_name = filename[:-3]  #删.py
#         module = importlib.import_module(f".{module_name}", package=__name__)
#         for attr_name in dir(module):
#             attr = getattr(module, attr_name)
#             if isinstance(attr, type):  #类类型
#                 globals()[attr_name] = attr #加包
