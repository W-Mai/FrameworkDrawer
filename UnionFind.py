class UnionFind(object):
    def __init__(self):
        self.father = dict()
        self.rank = dict()

    def find(self, x):
        if x not in self.father:
            self.father[x] = x
            self.rank[x] = 0
            return x
        if self.father[x] == x:
            return x
        self.father[x] = self.find(self.father[x])
        return self.father[x]

    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return
        if self.rank[x_root] < self.rank[y_root]:
            self.father[x_root] = y_root
        elif self.rank[x_root] > self.rank[y_root]:
            self.father[y_root] = x_root
        else:
            self.father[y_root] = x_root
            self.rank[x_root] += 1

    def connected(self, x, y):
        return self.find(x) == self.find(y)


if __name__ == '__main__':
    uf = UnionFind()
    uf.union(1, 2)
    uf.union(3, 4)
    uf.union(5, 6)
    uf.union(1, 3)
    uf.union(6, 4)

    assert uf.connected(1, 6)
