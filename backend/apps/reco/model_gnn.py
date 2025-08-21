import torch
import torch.nn as nn
from torch_geometric.nn import SAGEConv, to_hetero


class SAGENet(torch.nn.Module):
    def __init__(self, hidden_channels):
        super().__init__()
        self.conv1 = SAGEConv((-1, -1), hidden_channels)
        self.conv2 = SAGEConv((hidden_channels, hidden_channels), hidden_channels)
    def forward(self, x, edge_index):
        h = self.conv1(x, edge_index).relu()
        h = self.conv2(h, edge_index)
        return h


class HeteroLP(torch.nn.Module):
    def __init__(self, metadata, hidden_channels=64, out_dim=64):
        super().__init__()
        self.base = SAGENet(hidden_channels)
        self.gnn = to_hetero(self.base, metadata=metadata, aggr='sum')
        self.user_proj = nn.Linear(hidden_channels, out_dim)
        self.item_proj = nn.Linear(hidden_channels, out_dim)
        self.scorer = nn.CosineSimilarity(dim=-1)
    def forward(self, x_dict, edge_index_dict, user_idx, item_idx, user_node='user', item_node='product'):
        h_dict = self.gnn(x_dict, edge_index_dict)
        u = self.user_proj(h_dict[user_node][user_idx])
        v = self.item_proj(h_dict[item_node][item_idx])
        score = self.scorer(u, v)
        return (score + 1)/2