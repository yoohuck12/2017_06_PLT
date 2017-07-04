import networkx as nx
import json
import matplotlib.pyplot as plt


class JsonToDag():
    dep_visited_nodes = set()

    def __init__(self, my_file):
        self.my_file = my_file
        self.json_orig = open(self.my_file)
        self.j_orig = json.load(self.json_orig)
        self.G = nx.DiGraph(n_download_no_trigger=self.j_orig['n_download_no_trigger'],
                            start_activity=self.j_orig['start_activity'],
                            name=self.j_orig['name'],
                            load_activity=self.j_orig['load_activity'])
        self.G.add_node(self.G.graph['start_activity'])
        self.populate_attributes(self.G.graph['start_activity'])
        self.G.add_node(self.j_orig['objs'][0]['comps'][0]['id'])
        self.populate_attributes(self.j_orig['objs'][0]['comps'][0]['id'])
        # Edge comp_gap means difference between next edge s_time and current edge end_time(computation gap)
        self.G.add_edge(self.G.graph['start_activity'], self.j_orig['objs'][0]['comps'][0]['id'],
                        comp_gap=self.j_orig['objs'][0]['comps'][0]['s_time'] - float(
                            self.j_orig['objs'][0]['download']['receivedTime']), id='dep0')
        self.add_dependencies(self.G.node[self.j_orig['objs'][0]['comps'][0]['id']]['id'])
        self.dep_visited_nodes.add(self.G.node[self.j_orig['objs'][0]['comps'][0]['id']]['id'])

    def return_attr(self, object_id, attr):

        attr_dict = {'receivedTime':'e_time', 's_time': 's_time', }
        if object_id.startswith('download'):
            for my_index in range(len(self.j_orig['objs'])):
                if self.j_orig['objs'][my_index]['download']['id'] == object_id:
                    attr_value = self.j_orig['objs'][my_index]['download'][attr]
        else:
            for j_index in range(len(self.j_orig['objs'])):
                for k_index in range(len(self.j_orig['objs'][j_index]['comps'])):
                    if self.j_orig['objs'][j_index]['comps'][k_index]['id'] == object_id:
                        attr_value = self.j_orig['objs'][j_index]['comps'][k_index][attr_dict[attr]]
        return float(attr_value)

    def populate_attributes(self, object_id):

        if object_id.startswith('download'):
            for i in range(len(self.j_orig['objs'])):
                if self.j_orig['objs'][i]['download']['id'] == object_id:
                    self.G.node[object_id]['receiveFirst'] = self.j_orig['objs'][i]['download']['receiveFirst']
                    self.G.node[object_id]['len'] = self.j_orig['objs'][i]['download']['len']
                    self.G.node[object_id]['dns'] = self.j_orig['objs'][i]['download']['dns']
                    self.G.node[object_id]['dnsEnd'] = self.j_orig['objs'][i]['download']['dnsEnd']
                    self.G.node[object_id]['receiveHeadersEnd'] = self.j_orig['objs'][i]['download'][
                        'receiveHeadersEnd']
                    self.G.node[object_id]['sslEnd'] = self.j_orig['objs'][i]['download']['sslEnd']
                    self.G.node[object_id]['connectEnd'] = self.j_orig['objs'][i]['download']['connectEnd']
                    self.G.node[object_id]['connectStart'] = self.j_orig['objs'][i]['download']['connectStart']
                    self.G.node[object_id]['id'] = self.j_orig['objs'][i]['download']['id']
                    self.G.node[object_id]['receivedTime'] = float(self.j_orig['objs'][i]['download']['receivedTime'])
                    self.G.node[object_id]['sslStart'] = self.j_orig['objs'][i]['download']['sslStart']
                    self.G.node[object_id]['dnsStart'] = self.j_orig['objs'][i]['download']['dnsStart']
                    self.G.node[object_id]['receiveLast'] = self.j_orig['objs'][i]['download']['receiveLast']
                    self.G.node[object_id]['s_time'] = self.j_orig['objs'][i]['download']['s_time']
                    self.G.node[object_id]['dnsStart'] = self.j_orig['objs'][i]['download']['dnsStart']
                    self.G.node[object_id]['sendStart'] = self.j_orig['objs'][i]['download']['sendStart']
                    self.G.node[object_id]['sendEnd'] = self.j_orig['objs'][i]['download']['sendEnd']
                    self.G.node[object_id]['type'] = self.j_orig['objs'][i]['download']['type']
                    self.G.node[object_id]['when_comp_start'] = self.j_orig['objs'][i]['when_comp_start']
                    self.G.node[object_id]['url'] = self.j_orig['objs'][i]['url']
                    self.G.node[object_id]['parent_id'] = self.j_orig['objs'][i]['id']

        else:
            for j in range(len(self.j_orig['objs'])):
                for k in range(len(self.j_orig['objs'][j]['comps'])):
                    if self.j_orig['objs'][j]['comps'][k]['id'] == object_id:
                        self.G.node[object_id]['s_time'] = self.j_orig['objs'][j]['comps'][k]['s_time']
                        self.G.node[object_id]['time'] = self.j_orig['objs'][j]['comps'][k]['time']
                        self.G.node[object_id]['type'] = self.j_orig['objs'][j]['comps'][k]['type']
                        self.G.node[object_id]['id'] = self.j_orig['objs'][j]['comps'][k]['id']
                        self.G.node[object_id]['e_time'] = self.j_orig['objs'][j]['comps'][k]['e_time']
                        self.G.node[object_id]['when_comp_start'] = self.j_orig['objs'][j]['when_comp_start']
                        self.G.node[object_id]['url'] = self.j_orig['objs'][j]['url']
                        self.G.node[object_id]['parent_id'] = self.j_orig['objs'][j]['id']

    def add_dependencies(self, object_id=None):
        time_diff = 0
        # Assumption: never there is a download as a1.
        if object_id is None:
            fringe_set = set()
            for j in range(len(self.j_orig['deps'])):
                fringe_set.add(self.j_orig['deps'][j]['a1'])
                # print('fringe', fringe_set)
            while fringe_set:
                my_object_id = fringe_set.pop()
                # print(my_object_id)
                for i in range(len(self.j_orig['deps'])):
                    if self.j_orig['deps'][i]['a1'] == my_object_id and not self.j_orig['deps'][i][
                        'a1'] in self.dep_visited_nodes:
                        #print("match", self.j_orig['deps'][i]['a1'])
                        try:
                            if not self.G.node[my_object_id]:
                                self.G.add_node(my_object_id)
                        except KeyError:
                            self.G.add_node(my_object_id)
                        self.populate_attributes(self.j_orig['deps'][i]['a1'])

                        try:
                            if not self.G.node[self.j_orig['deps'][i]['a2']]:
                                self.G.add_node(self.j_orig['deps'][i]['a2'])
                        except KeyError:
                            self.G.add_node(self.j_orig['deps'][i]['a2'])
                        self.populate_attributes(self.j_orig['deps'][i]['a2'])

                        if self.j_orig['deps'][i]['time'] == -1:
                            time_diff = self.G.node[my_object_id]['e_time']
                        else:
                            time_diff = self.G.node[my_object_id]['e_time'] - self.j_orig['deps'][i]['time']

                        a2_s_time = self.return_attr(self.j_orig['deps'][i]['a2'], 's_time')
                        self.G.add_edge(my_object_id, self.j_orig['deps'][i]['a2'],
                                        comp_gap= a2_s_time - float(self.G.node[my_object_id]['s_time']),
                                        id=self.j_orig['deps'][i]['id'])
                self.dep_visited_nodes.add(object_id)
        else:
            if object_id not in self.dep_visited_nodes:
                for i in range(len(self.j_orig['deps'])):
                    if self.j_orig['deps'][i]['a1'] == object_id:
                        # print("match", self.j_orig['deps'][i]['a1'])
                        self.G.add_node(self.j_orig['deps'][i]['a2'])
                        self.populate_attributes(self.j_orig['deps'][i]['a2'])
                        if self.j_orig['deps'][i]['time'] == -1:
                            time_diff = self.G.node[object_id]['e_time']
                        else:
                            time_diff = self.G.node[object_id]['e_time'] - self.j_orig['deps'][i]['time']

                        a2_s_time = self.return_attr(self.j_orig['deps'][i]['a2'], 's_time')
                        self.G.add_edge(object_id, self.j_orig['deps'][i]['a2'],
                                        comp_gap=a2_s_time - float(self.G.node[object_id]['s_time']),
                                        id=self.j_orig['deps'][i]['id'])


    def draw_graph(self):
        pos = nx.spring_layout(self.G, iterations=200)
        # print(pos)
        nx.draw(self.G, pos, node_size=500)
        node_labels = nx.get_node_attributes(self.G, 'id')
        nx.draw_networkx_labels(self.G, pos, labels=node_labels)
        edge_labels = nx.get_edge_attributes(self.G, 'comp_gap')
        #print('edge lbl', edge_labels)
        nx.draw_networkx_edge_labels(self.G, pos, labels=edge_labels)
        plt.show()
        #plt.savefig("origin.png")

    def longest_path(self, G):
        dist = {} # stores [node, distance] pair
        for node in nx.topological_sort(G):
            # pairs of dist,node for all incoming edges
            pairs = [(dist[v][0]+1,v) for v in G.pred[node]]
            if pairs:
                dist[node] = max(pairs)
            else:
                dist[node] = (0, node)
        node,(length,_) = max(dist.items(), key=lambda x:x[1])
        path = []
        while length > 0:
            path.append(node)
            length,node = dist[node]
        return list(reversed(path))

    def get_last_node(self):
        last_node = 'download_0'
        for n, d in self.G.nodes_iter(data=True):
            if self.return_attr(n, 'receivedTime') > self.return_attr(last_node, 'receivedTime'):
                last_node = n
        return last_node


def main():
    file_name = '../dev/js-img/original.testbed.localhost_www.reddit.com_.json'
    my_graph = JsonToDag(file_name)
    my_graph.add_dependencies()
    print('PLT: ', my_graph.return_attr(my_graph.get_last_node(), 'receivedTime'))

    #print(my_graph.G.node)
    #print(nx.dfs_successors(my_graph.G, 'download_0'))
    my_edges = (my_graph.G.edge)

    #print(my_edges)
    #print(my_edges.__len__())
    #print(my_graph.longest_path(my_graph.G))
    my_graph.draw_graph()

    # self.dep_visited_nodes.append(self.G.node[self.j_orig['objs'][0]['comps'][0]['id']]['id'])


if __name__ == '__main__':
    main()
