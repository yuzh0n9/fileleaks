import yaml
import argparse

import fileOperation
import reCompile
from queue import Queue
import threading
import csv
from operator import itemgetter # 导入定位的头方便定位按照哪里排序

"""
获取目录下的所有文件名
读取每一个文件，在文件中寻找敏感信息
生产者消费者模式
"""

# 生产者类
class Producer(threading.Thread):
    def __init__(self, name, queue, filepath):
        threading.Thread.__init__(self, name=name)
        self.data = queue
        self.filepath = filepath
    def run(self) -> None:
        for i in self.filepath:
            self.data.put(i)

# 消费者类
class Consumer(threading.Thread):
    def __init__(self, name, queue, json_re, res_json):
        threading.Thread.__init__(self, name=name)
        self.data = queue
        self.json_re = json_re
        self.res_json = res_json



    def run(self) -> None:
        while queue.empty() != True:
            filepath = self.data.get()
            file_content = reCompile.read_files(filepath)
            # 对文件进行正则搜索
            temp_json = {}
            for key, value in self.json_re.items():
                pattern_res_json = {}
                if isinstance(value, str):
                    info_list = reCompile.find_all(value, file_content)
                    if info_list != []:
                        info_list = list(set(info_list)) # 列表去重
                        pattern_res_json.update({key:info_list})
                elif isinstance(value, list): # 如果是列表就遍历列表
                    temp_list = [] # 暂时保存匹配到的值
                    for i in value:
                        info_list = reCompile.find_all_in_file(i, filepath)
                        temp_list.extend(info_list)
                    if temp_list != []:
                        temp_list = list(set(temp_list)) # 列表去重
                        pattern_res_json.update({key: temp_list})
                if pattern_res_json != {}:
                    temp_json.update(pattern_res_json)
            if temp_json != {}:
                self.res_json.update({filepath: temp_json})



# 读取yaml
# https://blog.csdn.net/Asaasa1/article/details/109448444
def read_yaml(fileName:str):
    '''
    :param fileName: yaml文件
    :return: result type:dict
    '''
    with open(fileName, 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    return result

def main_argparse():
    parser = argparse.ArgumentParser(description='从文件中搜索敏感信息')

    parser.add_argument('-s', type=str, dest='sourcefile', action='store', required=True, help='原文件或目录')
    parser.add_argument('-o', type=str, dest='outfile', action='store', default='output.csv', help='将结果导出为csv')
    parser.add_argument('-t', type=int, dest='threads', action='store', default=20, help='设置的线程数量，默认为20')

    args = parser.parse_args()
    return (args.sourcefile, args.outfile, args.threads)

# 导出csv: 三列，名 信息 filepath
def output_csv(outfile, res_json):
    csvfile = open(outfile, 'w', newline="")
    writer = csv.writer(csvfile)
    writer.writerow(['描述', '信息', '文件路径'])
    table = []
    try:
        for filepath, value in res_json.items():
            for key_1, value_1 in value.items():
                str1 = ",".join(value_1)
                table.append((key_1, str1, filepath))
        # 按照第一列排序
        table_sorted = sorted(table,key=itemgetter(0),reverse=True)

    finally:
        writer.writerows(table_sorted)
        csvfile.close()


if __name__ == '__main__':
    args = main_argparse()
    sourcefile = args[0]
    outfile = args[1]
    threads_customer = args[2]
    # 最后的结果
    res_json = {}
    # 读取正则表达式
    re_json = read_yaml("./config/reDict.yaml")
    # for key,value in re_json.items():
    #     print(key)
    #     # print(value)
    #     if isinstance(value, str):
    #         print(value)
    #     elif isinstance(value, list):
    #         for i in value:
    #             print(i)
    # exit(0)

    # 文件检测，防止跑完报错
    try:
        test_file = open(outfile, 'w', newline="")
    except Exception as e:
        print(e)
        exit(0)

    print("---主线程开始---")
    # 读取指定目录下的所有文件
    filepath = []
    fileOperation.get_all_files(sourcefile, filepath)
    print("文件数量: " + str(len(filepath)))


    queue = Queue(1000)
    # 保存结果 json格式 {文件路径:{正则说明: [敏感信息]}}}
    # 初始化线程
    threads = []  # 存放线程的数组，相当于线程池
    # 开100个线程
    produce =Producer('Producer', queue, filepath)
    produce.start()

    for i in range(0,threads_customer):
        thread = Consumer('Consumer', queue, re_json,res_json)
        threads.append(thread)
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    produce.join()
    print("---主线程结束---")
    output_csv(outfile, res_json)