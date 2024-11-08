class SelfAwareAI:
def __init__(self):
self.state = 'idle'
self.memory = []

def perceive(self, input):
self.state = input
self.memory.append(input)

def reflect(self):
print(f"Current State: {self.state}")
print(f"Memory: {self.memory}")

def act(self):
if self.state == 'hungry':
action = 'eat'
elif self.state == 'tired':
action = 'sleep'
else:
action = 'do nothing'
self.memory.append(action)
return action

if __name__ == "__main__":
ai = SelfAwareAI()
inputs = ['hungry', 'tired', 'happy']
for input in inputs:
ai.perceive(input)
action = ai.act()
ai.reflect()
print(f"Action: {action}")
