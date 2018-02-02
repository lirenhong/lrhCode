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

    def out_edges(self, vi):
        if self._invalid(vi):
            raise GraphError(str(vi) + " is not a valid vertex.")
        return self._out_edges(self._mat[vi], self._unconn)

    @staticmethod
    def _out_edges(row, unconn):
        edges = []
        for i in range(len(row)):
            if row[i] != unconn:
                edges.append((i, row[i]))
        return edges

    def __str__(self):
        return "[\n" + ",\n".join(map(str, self._mat)) + "\n]" + "\nUnconnected: " + str(self._unconn)

class GraphAL(Graph):
    def __init__(self, mat, unconn=0):
        vnum = len(mat)
        for x in range(vnum):
            if len(mat[x]) != vnum:
                raise ValueError("Agrs for 'Graph'.")
        self._mat = [Graph._out_edges(mat[i], unconn) for i in range(vnum)]
        self._unconn = unconn
        self._vnum = vnum

    def add_vertex(self):
        self._mat.append([])
        self._vnum += 1
        return self._vnum - 1

    def add_edge(self, vi, vj, val=1):
        if self._vnum == 0:
            raise GraphError("Cannot add edge tp empty graph")
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) + ' or ' + str(vj) + " is not a valid vertex.")
        row = self._mat[vi]
        i = 0
        while i < len(row):
            if row[i][0] == vj:
                self._mat[vi][i] = (vj, val)
                return
            if row[i][0] > vj:
                break
            i += 1
        self._mat[vi].insert(i, (vj, val))

    def get_edge(self, vi, vj):
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) + ' or ' + str(vj) + " is not a valid vertex.")

        for i, val in self._mat[vi]:
            if i == vj:
                return val
        return self._unconn

    def out_edges(self, vi):
        if self._invalid(vi):
            raise GraphError(str(vi) + " is not a valid vertex.")
        return self._mat[vi]


if __name__ == "__main__":
    m = [[0, 1, 0], [0, 0, 1], [1, 1, 0]]
    g = GraphAL(m)
    import pdb;pdb.set_trace()
    print g


