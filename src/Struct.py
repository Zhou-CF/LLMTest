from typing import NamedTuple

class TextRange(NamedTuple):
    startLine:int
    endLine:int
    startOffset:int
    endOffset:int


class contMapStruct(NamedTuple):
    startLine:int
    endLine:int
    code:str

