import argparse
import torch
from app.core.model import SimpleMLP

def train_dummy(epochs=5):
    model = SimpleMLP(input_dim=4, hidden=16)
    optim = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = torch.nn.BCELoss()

    # Dummy dataset: random
    for epoch in range(epochs):
        x = torch.rand(64, 4)
        y = (x.sum(dim=1) > 2.0).float().unsqueeze(1)
        preds = model(x)
        loss = loss_fn(preds, y)
        optim.zero_grad()
        loss.backward()
        optim.step()
        if epoch % 1 == 0:
            print(f"Epoch {epoch} loss={loss.item():.4f}")
    return model

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, default='./models/sample_model.pt')
    args = parser.parse_args()

    model = train_dummy(epochs=10)
    data = {'state_dict': model.state_dict(), 'input_dim': model.fc1.in_features}
    import os
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    torch.save(data, args.output)
    print('Saved model to', args.output)
