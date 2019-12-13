from api import get_friends
from igraph import Graph, plot
import igraph
import numpy as np
import time


def plot_graph(edges, names_list = []):
    # Создаём граф
    if names_list == []:
        vertices = [i for i in range(len(edges))]
    else:
        vertices = names_list
    N = len(vertices)
    g = Graph(vertex_attrs={'label': vertices}, edges=edges, directed=False)
    g.simplify(multiple=True, loops=True)
     # Задаем стиль отображения графа
    visual_style = {
        "layout": g.layout_fruchterman_reingold(
            maxiter=10000,
            area=N**2,
            repulserad=N**2),
        "vertex_size": 10,
        "margin": 100
    }
    # Отрисовываем граф
    clusters = g.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    plot(g, **visual_style)
    


def get_network(users_ids, as_edgelist=True):

    if as_edgelist:

        edges = []
        for user in users_ids:
            try:
                users_friends = get_friends(user, 'id')['response']
            except KeyError:
                continue
            else:
                count = users_friends['count']
                for i in range(count):
                    this_friend_id = users_friends['items'][i]['id']
                    if this_friend_id in users_ids:
                        edges.append((users_ids.index(user), 
                            users_ids.index(this_friend_id)))
            time.sleep(1)
        return edges

    else:

        matrix = [[0] * len(users_ids) for l in range(len(users_ids))]
        for user in users_ids:
            users_friends = get_friends(user, 'id')
            count = users_friends['response']['count']
            for i in range(count):
                this_friend_id = users_friends['response']['items'][i]['id']
                if this_friend_id in users_ids:
                    this_index = users_ids.index(user)
                    this_friend_index = users_ids.index(this_friend_id)
                    matrix[this_index][this_friend_index] = 1
                    matrix[this_friend_index][this_index] = 1
        return matrix