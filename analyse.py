from src import FILEIO
import os

path = r'G:\ZCF\LLMTest\dataset\versions\summary'

data = []
firstLine = ["Key", "HighLightCode", "Message", "risk", "yes", "no", "or"]

for file in os.listdir(path):
    print(file)
    key = file.replace('.json', '')

    line_cont = [] # 用于存储每行数据
    line_cont.append(key) # 存储Key

    cont = FILEIO.read_json(os.path.join(path, file))
    for k in cont["基本信息"]:
        print(k, ':', cont["基本信息"][k])
        line_cont.append(cont["基本信息"][k]) # 存储基本信息
        
    print('yes', cont['yes'])
    print('or', cont['or'])
    print('no', cont['no'])

    # 存储是否有影响的数量
    line_cont.append(cont['yes'])
    line_cont.append(cont['no'])
    line_cont.append(cont['or'])

    # 准备写入excel
    data.append(line_cont)

FILEIO.save_excel(os.path.join(path, 'summary.xlsx'), data, firstLine)


