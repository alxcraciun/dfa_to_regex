DFA = {}
f = open('input.txt')

start_state = f.readline()
start_state = start_state.strip()
final_states = f.readline()
final_states = [elem.strip() for elem in final_states.split()]

alphabet = set()
all_states = set()

# States going into start_state
step1_states = set()

for line in f:
    table = [elem.strip() for elem in line.split()]
    all_states.add(table[0])
    all_states.add(table[2])
    alphabet.add(table[1])
    if DFA.get(table[0]) == None:
        DFA[table[0]] = {}
    DFA[table[0]].update({table[1]: table[2]})
    if table[2] == start_state:
        step1_states.add(table[0])
f.close()

# Step1 - outgoing to initial state
if step1_states:
    all_states.add('_qi')
    DFA['_qi'] = {'lambda': start_state}
    start_state = '_qi'


# Step2 - more final states
if len(final_states) > 1:
    all_states.add('_qf')
    for state in final_states:
        DFA[state].update({'lambda': '_qf'})
    final_states = ['_qf']

# Step3 - outgoing from final state
elif DFA.get(final_states[0]):
    all_states.add('_qf')
    DFA[final_states[0]].update({'lambda': '_qf'})
    final_states = ['_qf']

# Step4 - eliminate intermediate states gradually
intermediate_states = all_states.copy()
intermediate_states.remove(start_state)
intermediate_states.remove(final_states[0])

# for state in intermediate_states:

for key in DFA.items():
    print(*key)

print()