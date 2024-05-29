from src import FILEIO
import os
import re

r'否有风险：否，\n理由'

def extract_ans(answer):
    if type(answer) == str:
        match = re.search(r'\"是否有风险\":\s*\"(.+)\"', answer)
        if match:
           return match.group(1)

        match = re.search(r'是否有风险：(.+)，', answer)
        if match:
            return match.group(1)
        print("没有找到匹配的值")
    return answer["是否有风险"]


datasetPath = r'G:\ZCF\LLMTest\dataset\versions'
savepath = r'G:\ZCF\LLMTest\dataset\versions\summary'

FILEIO.is_exist_path(savepath)


hotspots = os.listdir(os.path.join(datasetPath, 'hotspot'))

for hotspot in hotspots:
    print(hotspot)
    if FILEIO.is_file_in_folder(savepath, hotspot):
        continue
    hotspot_cont = {}
    yes_count, or_count, no_count = 0, 0, 0
    try:
        for i in range(10):
            A_path = os.path.join(datasetPath, f'Q{i+1}')
            filepath = os.path.join(A_path, hotspot)
            cont = FILEIO.read_json(filepath)
            if not hotspot_cont:
                hotspot_cont['基本信息'] = cont['基本信息']
            hotspot_cont[f'第{i+1}次回答'] = cont["回答情况"]
            yesorno = extract_ans(cont["回答情况"])
            if yesorno == '是':
                yes_count += 1
            elif yesorno == '否':
                no_count += 1
            else:
                or_count += 1
                print(hotspot, f'Q{i+1}')
        hotspot_cont['yes'] = yes_count
        hotspot_cont['no'] = no_count
        hotspot_cont['or'] = or_count
        FILEIO.save_json(os.path.join(savepath, hotspot), hotspot_cont)
    except:
        print(hotspot, f'Q{i+1}')
        break
    
