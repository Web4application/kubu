class ReactiveMachine:
def __init__(self):
self.rules = {
'hungry': 'eat',
'tired': 'sleep',
'bored': 'play'
}

def respond(self, state):
return self.rules.get(state, 'do nothing')

if __name__ == "__main__":
machine = ReactiveMachine()
states = ['hungry', 'tired', 'bored', 'happy']
for state in states:
action = machine.respond(state)
print(f"State: {state} -> Action: {action}")
