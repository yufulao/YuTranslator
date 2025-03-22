import os
import shutil

# 原始项目路径
src_root = "D:/project/YuTranslator/scripts"
# 目标去 BOM 目录
dst_root = "D:/project/YuTranslator/scripts_no_bom"

def remove_bom_and_copy(src_file, dst_file):
    with open(src_file, "rb") as f:
        content = f.read()
    
    # 检查 BOM 并移除
    if content.startswith(b'\xef\xbb\xbf'):
        content = content[3:]

    # 确保目标文件夹存在
    os.makedirs(os.path.dirname(dst_file), exist_ok=True)

    # 写入新文件
    with open(dst_file, "wb") as f:
        f.write(content)

def traverse_and_copy(src_root, dst_root):
    for root, _, files in os.walk(src_root):
        for file in files:
            if file.endswith(".py"):
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_root, os.path.relpath(src_file, src_root))
                remove_bom_and_copy(src_file, dst_file)

if __name__ == "__main__":
    # 确保目标目录干净
    if os.path.exists(dst_root):
        shutil.rmtree(dst_root)
    
    print("正在去除 BOM 并复制文件...")
    traverse_and_copy(src_root, dst_root)
    
    
    
    
# pipreqs . 
# pip install -r requirements.txt --target=D:\project\YuTranslator\lib_test

