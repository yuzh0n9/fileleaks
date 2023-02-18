import re

# 搜索内容中的所有值,只取正则表达式最外层的括号
def find_all(pattern:str, string:str):
    result = []
    match = re.findall(pattern, string)
    if match == []:
        return []
    if type(match[0]) == tuple:
        for item in match:
            result.append(item[0])
    else:
        result.extend(match)
    return result

# 输入文件路径，读取文件
def read_files(filePath):
    with open(filePath, "rb") as f:
        data = f.read()
    return data.decode()

# 搜索文件中的所有内容,只取正则表达式最外层的括号
# 返回list
def find_all_in_file(pattern:str, filepath:str):
    content = read_files(filepath)
    # print("find_all_in_file")
    # print(content)
    return find_all(pattern, content)

def test():
    str1 = "127.0.0.1 192.168.1.11"
    str2 = "MR_SHOP mr_shop"
    pattern1 = r'[1-9]{1,3}(\.[0-9]{1,3}){3}'
    pattern2 = r'([1-9]{1,3}(\.[0-9]{1,3}){3})'
    pattern3 = r'mr_\w+'

    filepath = r"E:\00Test\apk\firepwd-master\firepwd.py"
    pattern4 = r'([1-9]{1,3}(\.[0-9]{1,3}){3})'
    res = find_all_in_file(pattern4, filepath)
    print(res)

if __name__ == '__main__':
    test()