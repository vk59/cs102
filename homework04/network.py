from api import get_friends
from igraph import Graph, plot
import igraph
import numpy as np


def plot_graph(g, N):
     # Задаем стиль отображения графа
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
            maxiter=1000,
            area=N**3,
            repulserad=N**3)

    # Отрисовываем граф
    g.simplify(multiple=True, loops=True)
    communities = g.community_edge_betweenness(directed=False)
    clusters = communities.as_clustering()
    print(clusters)
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    plot(g, **visual_style)


def get_network(users_ids, as_edgelist=True):
    vertices = [i for i in range(len(users_ids))]
    edges = []
    for user in users_ids:
        users_friends = get_friends(user, 'id')
        count = users_friends['response']['count']
        for i in range(count):
            this_friend_id = users_friends['response']['items'][i]['id']
            if this_friend_id in users_ids:
                edges.append((users_ids.index(user), 
                    users_ids.index(this_friend_id)))

    # Создание графа
    print(edges)
    g = Graph(vertex_attrs={"label":vertices}, edges=edges, directed=False)
    plot_graph(g, len(vertices))
