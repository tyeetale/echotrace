from pyvis.network import Network
import tempfile

class TreeVisualizer:
    def render(self, edges, nodes):
        net = Network(height="500px", directed=True)
        for node_id, node in nodes.items():
            net.add_node(node_id, label=node.user_msg[:30], title=node.ai_msg)

        for src, tgt in edges:
            net.add_edge(src, tgt)

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        net.save_graph(tmp.name)
        return tmp.name