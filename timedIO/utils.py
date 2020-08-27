import networkx as nx


class MealyMachine:
    _filename   = None
    _nx         = None
    _s0         = None
    _graph      = None

    def __init__(self, fname):
        self._filename = fname
        self._nx = nx.drawing.nx_pydot.read_dot(fname)
        self._s0 = [_nod for _nod in self._nx.neighbors('__start0')][0]
        self._graph = dict()

        for _i in self._nx.adj:
            if _i == '__start0': continue
            self._graph[_i] = dict()
            for _j in self._nx.adj[_i]:
                for _label in self._nx.adj[_i][_j]:
                    _in, _out = str(self._nx.adj[_i][_j][_label]['label']).replace('\"', '').split(' / ')
                    self._graph[_i][_in] = [_out, _j]

    def get_states(self):
        return [n for n in self._graph.keys()]

    def next_state(self, i, label):
        return self._graph[i][label]

    def list_destination(self, inputs):
        curr = self._s0
        states = []
        for an_in in inputs:
            if an_in == 'Reset':
                curr = self._s0
            else:
                curr = self._graph[curr][an_in][1]
            states.append(curr)
        return states

    def list_origin(self, inputs):
        curr = self._s0
        states = []
        for an_in in inputs:
            states.append(curr)
            if an_in == 'Reset':
                curr = self._s0
            else:
                curr = self._graph[curr][an_in][1]

        return states


    def list_outputs(self, inputs):
        curr = self._s0
        outputs = []
        for an_in in inputs:
            if an_in == 'Reset':
                outputs.append("Reset")
                curr = self._s0
            else:
                outputs.append(self._graph[curr][an_in][0])
                curr = self._graph[curr][an_in][1]

        return outputs

# mm = MealyMachine("learnedModel.dot")
#
# print(mm.list_origin(["ApplicationDataEmpty"]))
# print(["ApplicationDataEmpty"])
# print(mm.list_outputs(["ApplicationDataEmpty"]))
# print(mm.list_destination(["ApplicationDataEmpty"]))