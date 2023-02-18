import os


#遍历filepath下所有文件，包括子目录
def get_all_files(filepath, dir_list:list):
    # 判断路径是文件还是目录
    if os.path.isdir(filepath) != True:
        return dir_list.append(filepath)
    files = os.listdir(filepath)
    for fi in files:
        fi_d = os.path.join(filepath,fi)
        if os.path.isdir(fi_d):
            get_all_files(fi_d, dir_list)
        else:
            dir_list.append(os.path.join(filepath,fi_d))
            # print(os.path.join(filepath,fi_d))

# 输入文件路径，读取文件
def read_files(filePath):
    with open(filePath, "rb") as f:
        data = f.read()
    return data