
from . import getInfoFromSonarQube as GIFS
from . import Struct as ST
from . import getFileContent
from . import FILEIO
import os
import sys


class RuAnAn:
    def __init__(self, path, project, dataset=None) -> None:
        """孺安安"""
        self.path = path
        self.project = project
        self.__currPath = os.path.dirname(os.path.abspath(__file__)).split('src')[0]
        self.__initDataset(dataset)
        self.hotspots:list = self.__getKey()
        
        # self.AI = AI.ZPQY()
    
    
    def __initDataset(self, dataset):
        if dataset:
            self.dataset = dataset
            return
        self.dataset = os.path.join(self.__currPath, 'dataset', self.project, 'hotspot')
        self.question = os.path.join(self.__currPath, 'dataset', self.project, 'question')
        flag = FILEIO.is_exist_path(self.dataset) and FILEIO.is_exist_path(self.question)
        if not flag:
            sys.exit()
        
    
    def __getKey(self):
        # 获取hotspot信息
        hotspots = []
        data = GIFS.search(self.project)
        hotspots += data['hotspots']
        # 如果一次性没获取完
        while (self.__isContinueSearch(data['paging'])):
            data = GIFS.search(self.project)
            hotspots += data['hotspots']
        # 返回所有的key
        return [hotspot['key'] for hotspot in hotspots]
    
    def __isContinueSearch(self, page):
        return page['pageIndex'] * page['pageSize'] < page['total']
    

    def __constructQuestion(self, code, rangecode, message, risk):
        return f"{code}\n上述代码中{rangecode}代码显示{message},风险是{risk}。" + "如果在此代码中无相关风险，请回答`否`。如果有相关风险，则回答`是`。请仅以JSON格式回答，格式如下{是否有风险：`是`或者`否`, 理由：因为...}。"


    # 返回问题，构建问题，保存，方便下次调用
    def getOneInfoQ(self, key):
        if FILEIO.is_file_in_folder(self.question, key+'.txt'):
            return FILEIO.read_txt(os.path.join(self.question, key+'.txt'))
        data = self.gethotspotInfo(key=key)
        question = self.__constructQuestion(data['code'], data['rangecode'], data["message"], data['risk'])
        FILEIO.save_txt(os.path.join(self.question, key+'.txt'), question)
        return question
    
    # 获取key对应的信息，保存，方便以后调用
    def gethotspotInfo(self, key):
        if not FILEIO.is_file_in_folder(self.dataset, key+'.json'):
            data = GIFS.show(key=key)
            FILEIO.save_json(os.path.join(self.dataset, key+'.json'), data)
        else:
            data = FILEIO.read_json(os.path.join(self.dataset, key+'.json'))

        filepath = data["component"]["path"]
        range = data["textRange"]
        message = data["message"]
        risk = data["rule"]["riskDescription"].split('.')[0].replace('<p>', '')

        file_path = os.path.join(self.path, filepath)

        # 创建分析目标文件对象
        P = getFileContent.ParseFile(file_path)
        # 根据目标文件获取 对应源码 以及 有问题源码
        code, rangecode = P.getCont(
            ST.TextRange(range['startLine'], range['endLine'], range['startOffset'], range['endOffset']))
        
        return {'file_path': file_path, "range": range, "message": message, "risk": risk, "code":code, "rangecode": rangecode}
    

if __name__ == '__main__':
    RuAnAn('', '')