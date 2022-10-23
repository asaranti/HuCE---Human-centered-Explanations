"""
    Create a Graph Dataset

    :author: Anna Saranti
    :copyright: © 2021 HCI-KDD (ex-AI) group
    :date: 2021-10-04
"""


import torch
from torch_geometric.data import Dataset


class GraphDataset(Dataset):
    """

    """

    def __init__(self, data):
        """

        :param data:
        """

        super(GraphDataset, self).__init__()
        self.data = data

    def __len__(self):
        """

        :return:
        """

        return len(self.data)

    def __getitem__(self, idx):
        """

        :param idx:
        :return:
        """

        if torch.is_tensor(idx):
            idx = idx.tolist()
        return self.data[idx]
