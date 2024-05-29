from src import Auto
from src import ERNIESpeed128_apply as WXYY
from src import FILEIO
import random
import json
import os
import time

def Q(question):
    if type(question) != str:
        return 
    answer = WXYY.main(question)
    return answer


def dealAnswer(answer):
    try:
        data = json.loads(answer)
        result = data['result']
        result = result.replace("```json\n", '').replace("\n```", '').replace("```json\\n", '').replace("\\n```", '')
        try:
            res = json.loads(result)
            return res
        except:
            return result
    except:
        print(answer)
        return
        




def main(file_path, project, save_path, i):
    # 从sonarqube上获取项目的待审计信息
    P = Auto.RuAnAn(file_path, project)

    for key in P.hotspots:
        print(key)
        if FILEIO.is_file_in_folder(save_path, key+'.json'):  
            continue
        # 获取Key相关的信息
        info = P.gethotspotInfo(key)
        # 提取关键信息
        keyInfo = {"HighLightCode": info["rangecode"], "Message": info['message'], 'risk': info['risk']}
        for k in keyInfo:
            print(k, ':', keyInfo[k])
        # 构造问题
        question = P.getOneInfoQ(key)
        # 询问WXYY
        answer = WXYY.main(question)
        answer = dealAnswer(answer)
        if answer:
            print(answer)
            RESULT = {'基本信息': keyInfo, "回答情况": answer}
            FILEIO.save_json(os.path.join(save_path, key+'.json'), RESULT)
        
        print('*' * 10 + f'{i}')
        sleeptime = random.randint(60, 63)
        time.sleep(sleeptime)
        





    


if __name__ == '__main__':
    # 项目地址
    file_path = r'E:\iie\新项目\代码区'
    # 询问结果保存地址
    save_path = r'G:\ZCF\LLMTest\dataset\versions'
    # 询问轮数
    round_num = 10
    # 此项目名称应与sonarqube上的标识一致
    proejct = 'versions'
    for i in range(round_num):
        _savepath = os.path.join(save_path, f'Q{i+1}')
        if not os.path.exists(_savepath):
            os.makedirs(_savepath)
        main(file_path, proejct, _savepath, i)

    # P = Auto.RuAnAn(file_path, 'versions')
    # # 构造问题
    # for i in P.hotspots:
        # question = P.getOneInfoQ(i)
    # question = P.getOneInfoQ('AY-zweegWByPg3BEAi8Q')
    # # 询问WXYY
    # answer = WXYY.main(question)
    # print(answer)
    # answer = dealAnswer(answer)
    # print(answer)
    

