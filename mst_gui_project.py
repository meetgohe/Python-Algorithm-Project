
import tkinter as tk
from tkinter import messagebox, filedialog
import networkx as nx
import matplotlib.pyplot as plt
import json

G = nx.Graph()

def add_edge():
    try:
        edge_data = entry.get()
        node1, node2, weight = edge_data.split()
        weight = int(weight)
        G.add_edge(node1, node2, weight=weight)
        messagebox.showinfo("Success", f"Edge ({node1}, {node2}, {weight}) added.")
    except ValueError:
        messagebox.showerror("Error", "Enter data in format: node1 node2 weight")

def remove_edge():
    try:
        edge_data = entry.get()
        node1, node2 = edge_data.split()
        G.remove_edge(node1, node2)
        messagebox.showinfo("Success", f"Edge ({node1}, {node2}) removed.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to remove edge: {e}")

def run_prim():
    if nx.is_connected(G):
        mst = nx.minimum_spanning_tree(G, algorithm='prim')
        show_graph(mst, title="Prim's MST")
    else:
        messagebox.showerror("Error", "Graph must be connected to find MST.")

def run_kruskal():
    if nx.is_connected(G):
        mst = nx.minimum_spanning_tree(G, algorithm='kruskal')
        show_graph(mst, title="Kruskal's MST")
    else:
        messagebox.showerror("Error", "Graph must be connected to find MST.")

def show_graph(graph, title="Graph"):
    pos = nx.spring_layout(graph)
    weights = nx.get_edge_attributes(graph, 'weight')
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='black', node_size=2000, font_size=10)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=weights)
    plt.title(title)
    plt.show()

def save_graph():
    file_path = filedialog.asksaveasfilename(defaultextension=".json")
    if file_path:
        data = nx.node_link_data(G)
        with open(file_path, 'w') as f:
            json.dump(data, f)
        messagebox.showinfo("Saved", "Graph saved successfully.")

def load_graph():
    global G
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'r') as f:
            data = json.load(f)
            G = nx.node_link_graph(data)
        messagebox.showinfo("Loaded", "Graph loaded successfully.")

# Tkinter GUI setup
root = tk.Tk()
root.title("MST Algorithm Visualizer")
root.geometry("600x400")

entry = tk.Entry(root, width=40)
entry.pack(pady=10)

tk.Button(root, text="Add Edge", command=add_edge).pack(pady=5)
tk.Button(root, text="Remove Edge", command=remove_edge).pack(pady=5)
tk.Button(root, text="Run Prim's Algorithm", command=run_prim).pack(pady=5)
tk.Button(root, text="Run Kruskal's Algorithm", command=run_kruskal).pack(pady=5)
tk.Button(root, text="Save Graph", command=save_graph).pack(pady=5)
tk.Button(root, text="Load Graph", command=load_graph).pack(pady=5)
tk.Button(root, text="Exit", command=root.quit).pack(pady=20)

root.mainloop()
