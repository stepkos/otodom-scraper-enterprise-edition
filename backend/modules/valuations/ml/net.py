import torch


class MLP(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Linear(19, 256),
            torch.nn.ReLU(),
            torch.nn.Dropout(.3),
            torch.nn.Linear(256, 128),
            torch.nn.ReLU(),
            torch.nn.Dropout(.3),
            torch.nn.Linear(128, 1),
        )

    def forward(self, x):
        return self.net(x)
