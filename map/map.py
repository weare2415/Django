import networkx as nx
import osmnx as ox
import folium

G = ox.graph_from_place('대한민국', network_type='drive', simplify=True)

G_proj = ox.project_graph(G, to_crs="EPSG:4326")
ox.save_graphml(G_proj, 'graph.osm')