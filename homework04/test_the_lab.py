from network import get_network, plot_graph
from api import get_friends, get_wall
from age import age_predict
from api_models import normalize


print('test age_predict')
print(age_predict(125483792))

print('test graph')
friends = get_friends(125483792, 'id')['response']
users_ids = []
names = []
k = 0
for friend in friends['items']:
    users_ids.append(friend['id'])
    names.append(friend['first_name'] + ' ' + friend['last_name'])
    k += 1
    if k == 50:
        break
edges = get_network(users_ids, as_edgelist=True)
plot_graph(edges, names)
'''
with open('1.txt', 'w') as f:
    post_list = get_wall(domain='pn6', count=5)
    f.writelines(normalize(post_list))
'''
