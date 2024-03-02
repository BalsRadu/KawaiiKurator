import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl

class RecommenderNet(pl.LightningModule):
    def __init__(self, num_users, num_animes, embedding_size=128):
        super(RecommenderNet, self).__init__()
        self.embedding_size = embedding_size
        self.user_embedding = nn.Embedding(num_users, embedding_size)
        self.anime_embedding = nn.Embedding(num_animes, embedding_size)

        self.fc1 = nn.Linear(1, 64)
        self.fc2 = nn.Linear(64, 1)

        # Parameters for LR scheduler
        self.start_lr = 0.00001
        self.min_lr = 0.00001
        self.max_lr = 0.0004
        self.rampup_epochs = 5
        self.sustain_epochs = 0
        self.exp_decay = .8

    def forward(self, user_input, anime_input):
        # Embedding layers
        user_embedded = self.user_embedding(user_input)
        anime_embedded = self.anime_embedding(anime_input)

        # Normalize embeddings
        user_embedded_norm = F.normalize(user_embedded, p=2, dim=1)
        anime_embedded_norm = F.normalize(anime_embedded, p=2, dim=1)

        # Dot product and flattening
        dot_product = torch.sum(user_embedded_norm * anime_embedded_norm, dim=1, keepdim=True)

        # Dense layers
        x = F.relu(self.fc1(dot_product))
        x = torch.sigmoid(self.fc2(x))
        return x

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.start_lr)

        # Define the learning rate schedule function
        def lr_lambda(epoch):
            if epoch < self.rampup_epochs:
                return (self.max_lr - self.start_lr) / self.rampup_epochs * epoch + self.start_lr
            elif epoch < self.rampup_epochs + self.sustain_epochs:
                return self.max_lr
            else:
                return (self.max_lr - self.min_lr) * self.exp_decay**(epoch - self.rampup_epochs - self.sustain_epochs) + self.min_lr

        # Create the scheduler
        scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)

        return [optimizer], [scheduler]


    def lr_lambda(self, epoch):
        if epoch < self.rampup_epochs:
            return (self.max_lr - self.start_lr) / self.rampup_epochs * epoch + self.start_lr
        elif epoch < self.rampup_epochs + self.sustain_epochs:
            return self.max_lr
        else:
            return (self.max_lr - self.min_lr) * self.exp_decay**(epoch - self.rampup_epochs - self.sustain_epochs) + self.min_lr

    def training_step(self, batch, batch_idx):
        user_input, anime_input, labels = batch
        predictions = self(user_input, anime_input)
        loss = F.binary_cross_entropy(predictions, labels.view(-1, 1))
        self.log('train_loss', loss, on_step=False, on_epoch=True, prog_bar=True, logger=True)
        return loss

    def validation_step(self, batch, batch_idx):
        user_input, anime_input, labels = batch
        predictions = self(user_input, anime_input)
        loss = F.binary_cross_entropy(predictions, labels.view(-1, 1))
        self.log('val_loss', loss, on_step=False, on_epoch=True, prog_bar=True, logger=True)
        return loss