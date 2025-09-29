from antlr4 import *


class BisonLexerBase(Lexer):
    is_like_c = False

    def isLikeC(self):
        return self.is_like_c

    def isLikePy(self):
        return not self.is_like_c
