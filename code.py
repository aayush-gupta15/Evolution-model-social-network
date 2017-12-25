import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import time

def create_graph():
	G=nx.Graph()
	#G.add_nodes_from(range(1,101))
	for i in range(1,21):
		G.add_node(i)
	return G

def vis(G,t):
	time.sleep(1)
	labeldict=get_label(G)
	nodesize=get_size(G)
	color=get_color(G)
	nx.draw(G,labels=labeldict,node_size=nodesize,node_color=color)
	plt.savefig('evolution_'+str(t)+'.jpg')
	plt.clf()
	plt.cla()
	nx.write_gml(G,'evolution_'+str(t)+'.gml')

def assign_health(G):
	for each in G.nodes():
		G.node[each]['name']=random.randint(1,30)
		G.node[each]['type']='Person'


def get_label(G):
	dict1={}
	for each in G.nodes():
		dict1[each]=G.node[each]['name']
	return dict1

def get_size(G):
	array1=[]
	for each in G.nodes():
		if G.node[each]['type']=='Person':
			array1.append(G.node[each]['name']*40)
		else:
			array1.append(1000)
	return array1

def add_foci(G):
	n=G.number_of_nodes()
	i=n+1
	foci_nodes=['smoking','drinking','exercise','playing_sports']
	for j in range(0,4):
		G.add_node(i)
		G.node[i]['name']=foci_nodes[j]
		G.node[i]['type']='foci'
		i=i+1

def get_color(G):
	c=[]
	for each in G.nodes():
		if G.node[each]['type']=='Person':
			if G.node[each]['name']==1:
				c.append('green')
			elif G.node[each]['name']==30:
				c.append('yellow')
			else:
				c.append('blue')
		else:
			c.append('red')
	return c

def get_foci_nodes():
	f=[]
	for each in G.nodes():
		if G.node[each]['type']=='foci':
			f.append(each)
	return f

def get_person_nodes():
	f=[]
	for each in G.nodes():
		if G.node[each]['type']=='Person':
			f.append(each)
	return f

def add_foci_edges():
	foci_nodes=get_foci_nodes()
	people_node=get_person_nodes()
	for each in people_node:
		r=random.choice(foci_nodes)
		G.add_edge(each,r)

def homophily(G):
	pnodes=get_person_nodes()
	for u in pnodes:
		for v in pnodes:
			if u!=v:
				diff=abs(G.node[u]['name']-G.node[v]['name'])
				prob=float(1)/(diff+1000)
				r=random.uniform(0,1)
				if r<prob:
					G.add_edge(u,v)


def cmn(u,v,G):
	nu=set(G.neighbors(u))
	nv=set(G.neighbors(v))
	return len(nu & nv)

def closure(G):
	array1=[]
	for u in G.nodes():
		for v in G.nodes():
			if u!=v and (G.node[u]['type']=='Person' or G.node[v]['type']=='Person'):
				k=cmn(u,v,G)
				p=1-math.pow((1-0.01),k)
				tmp=[]
				tmp.append(u)
				tmp.append(v)
				tmp.append(p)
				array1.append(tmp)
	for each in array1:
		u=each[0]
		v=each[1]
		p=each[2]
		r=random.uniform(0,1)
		if r<p:
			G.add_edge(u,v)

def change_health(G):
	fnodes=get_foci_nodes()
	for each in fnodes:
		if G.node[each]['name']=='smoking':
			for each1 in G.neighbors(each):
				if G.node[each1]['name']!=30:
					G.node[each1]['name']=G.node[each1]['name']+3
					if G.node[each1]['name']>30:
						G.node[each1]['name']=30


		if G.node[each]['name']=='drinking':
			for each1 in G.neighbors(each):
				if G.node[each1]['name']!=30:
					G.node[each1]['name']=G.node[each1]['name']+2
					if G.node[each1]['name']>30:
						G.node[each1]['name']=30

		if G.node[each]['name']=='exercise':
			for each1 in G.neighbors(each):
				if G.node[each1]['name']!=1:
					G.node[each1]['name']=G.node[each1]['name']-2
					if G.node[each1]['name']<1:
						G.node[each1]['name']=1	

		if G.node[each]['name']=='playing_sports':
			for each1 in G.neighbors(each):
				if G.node[each1]['name']!=1:
					G.node[each1]['name']=G.node[each1]['name']-1
					if G.node[each1]['name']<1:
						G.node[each1]['name']=1			


G=create_graph()
assign_health(G)
add_foci(G)


add_foci_edges()
time.sleep(10)
t=0
vis(G,t)
for t in range(0,5):
	homophily(G)
	closure(G)
	change_health(G)
	vis(G,t+1)

