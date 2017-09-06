#!/usr/bin/env python3
from sys import argv
from collections import namedtuple

builtin = namedtuple('builtin', ['function'])
procedure = namedtuple('procedure', ['name', 'parameters', 'operator', 'operands'])
closure = namedtuple('closure', ['procedure', 'environment'])
apply = namedtuple('apply', ['closure', 'arguments'])

def parse(source):
    program = {}
    for line in source.splitlines():
        if line == '':
            continue
        left, right = line.split('↦')
        left = left.split()
        right = right.split()
        yield procedure(left[0], left[1:], right[0], right[1:])

def transition(state): 
    
    # Builtins
    if isinstance(state.closure, builtin):
        return state.closure.function(state.arguments)
    
    # Closures
    assert(isinstance(state.closure, closure))
    (c, e), a = state
    n, p, t, r = c
    
    # Update environment
    e = e.copy()
    e[n] = c
    for k, v in zip(p, a):
        e[k] = v
    
    # Close over procedures
    t = closure(e[t], e) if isinstance(e[t], procedure) else e[t]
    r = [closure(e[s], e) if isinstance(e[s], procedure) else e[s] for s in r]
    
    # Create new state
    return apply(t, r)

# Runtime environment
env = {
    'is_zero': builtin(lambda x: 
        apply(x[1], []) if x[0] == 0 else apply(x[2], [])
    ),
    'add': builtin(lambda x:
        apply(x[2], [x[0] + x[1]])
    ),
    'sub': builtin(lambda x:
        apply(x[2], [x[0] - x[1]])
    ),
    'mul': builtin(lambda x: 
        apply(x[2], [x[0] * x[1]])
    ),
    'procedure': builtin(lambda x: 
        apply(x[1], list(x[0][0]))
    ),
    'environment': builtin(lambda x: 
        apply(x[1], [x[0][1]])
    ),
    'procedure': builtin(lambda x: 
        apply(x[1], [x[0][0], x[0][1]])
    ),
}
for i in range(100):
    env[str(i)] = i

# Read program
program = ""
with open(argv[1]) as file:
    program = file.read()

# Load program in environment
for p in parse(program):
    env[p.name] = p

# Initial state
state = apply(closure(env['main'], env), ['exit'])

# Itterate state transition
while state.closure != 'exit':
    state = transition(state)

# Print final result
print(state.arguments)
