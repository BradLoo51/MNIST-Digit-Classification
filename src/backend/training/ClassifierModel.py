from torch import nn

class ImageClassifier(nn.Module):
    def __init__(self):
        super(ImageClassifier, self).__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3), # 28 - 2 - 1 + 1 = 26
            nn.MaxPool2d(kernel_size=2), # 26 / 2 = 13
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3), # 13 - 2 - 1 + 1 = 11
            nn.MaxPool2d(kernel_size=2), # 11 / 2 = 5
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3), # 5 - 2 - 1 + 1 = 3
            nn.ReLU()
        )
        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 3 * 3, 10),
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x
