#-*- coding:utf-8 -*-

class GraphError(Exception):
    pass

class Graph(object):
    def __init__(self, mat, unconn=0):
        vnum = len(mat)
        for x in range(vnum):
            if len(mat[x]) != vnum:
                raise ValueError("Agrs for 'Graph'.")
        self._mat = [mat[i][:] for i in range(vnum)]
        self._unconn = unconn
        self._vnum = vnum

    def vertext_num(self):
        return self._vnum

    def _invalid(self, v):
        return v < 0 or v >= self._vnum

    def add_vertex(self):
        raise GraphError(
            "Adj-Matrix dose not support 'add_vertex'.")

    def add_edge(self, vi, vj, val=1):
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) + ' or ' + str(vj) + " is not a valid vertex.")

        self._mat[vi][vj] = val

    def get_edge(self, vi, vj):
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) + ' or ' + str(vj) + " is not a valid vertex.")

        return self._mat[vi][vj]

if __name__ == "__main__":
    m = [[0, 1, 0], [0, 0, 1], [1, 1, 0]]
    g = Graph(m)
    import pdb;pdb.set_trace()
    print g.vertext_num
    print g.get_edge(2,2)


