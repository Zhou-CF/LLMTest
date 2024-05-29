import ast
from . import Struct as struct

class ParseFile:
    def __init__(self, file_path) -> None:
        self.source_code = self.__readFile(file_path)
        self.tree = ast.parse(self.source_code)
        self.cont_map = self.contMap()
    
    def contMap(self):
        temp = {}
        for node in ast.iter_child_nodes(self.tree):

            start_lineno = getattr(node, 'lineno', 'Unknown')
            # 获取节点的结束行号
            end_lineno = getattr(node, 'end_lineno', start_lineno)  # 同一行的情况下起始行号就是结束行号
            # 获取最外层节点的源码内容
            source_segment = ast.get_source_segment(self.source_code, node)
            temp[start_lineno]=struct.contMapStruct(start_lineno, end_lineno, source_segment)
        return temp
    
    def __readFile(self, file_path):
        with open(file_path, 'r', encoding='utf8') as source_file:
            source_code = source_file.read()
        return source_code
    
    def checkRange(self, textRange:struct.TextRange, continfo:struct.contMapStruct):
        return textRange.startLine >= continfo.startLine and textRange.endLine <= continfo.endLine
    
    def getRangeCode(self, code, startLine, textRange:struct.TextRange):
        sl, el = textRange.startLine - startLine, textRange.endLine - startLine
        codesplit = code.split('\n')
        if sl == el:
            return codesplit[sl][textRange.startOffset: textRange.endOffset]
        s = ''
        for i in (sl, el+1):
            if i == sl:
                s += codesplit[i][textRange.startOffset:]
            elif i == el:
                s += codesplit[i][:textRange.endOffset]
            else:
                s += codesplit[i]
        return s
            


    def getCont(self, textRange:struct.TextRange):
        mapLine = textRange.startLine
        code, rangecode = '', ''
        while (mapLine>=0):
            if self.cont_map.get(mapLine) and self.checkRange(textRange, self.cont_map[mapLine]):
                code = self.cont_map[mapLine].code
                rangecode = self.getRangeCode(code, mapLine, textRange)
                break
            mapLine -= 1
        return code, rangecode
                



