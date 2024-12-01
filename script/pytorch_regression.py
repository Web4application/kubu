import torch
import torch.nn as nn
import torch.optim as optim

# Generate some sample data
x = torch.randn(100, 1)
y = 3 * x + 2 + torch.randn(100, 1) * 0.1

# Define the model
model = nn.Linear(1, 1)

# Define the loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Train the model with self-monitoring
for epoch in range(1000):
model.train()
optimizer.zero_grad()
outputs = model(x)
loss = criterion(outputs, y)
loss.backward()
optimizer.step()

# Self-awareness: Monitor and print loss
if epoch % 100 == 0:
print(f'Epoch {epoch}, Loss: {loss.item()}')

# Print the learned parameters
print(model.weight.item(), model.bias.item())
