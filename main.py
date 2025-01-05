DFA = {}
f = open('input.txt')

start_state = f.readline()
start_state = start_state.strip()
final_states = f.readline()
final_states = [elem.strip() for elem in final_states.split()]

alphabet = set()
all_states = set()
alphabet.add('lambda')

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
    for elim_state in final_states:
        DFA[elim_state].update({'lambda': '_qf'})
    final_states = ['_qf']

# Step3 - outgoing from final state
elif DFA.get(final_states[0]):
    all_states.add('_qf')
    DFA[final_states[0]].update({'lambda': '_qf'})
    final_states = ['_qf']

DFA['_qf'] = {'lambda': '_qf'}

# Step4 - eliminate intermediate states gradually
intermediate_states = all_states.copy()
intermediate_states.remove(start_state)
intermediate_states.remove(final_states[0])


for elim_state in intermediate_states:
    print('\nState to eliminate: ', elim_state)

    end_state = None
    end_transition = None
    cycle_transition = None
    # find cycle transition & finishing state
    for transition, state in DFA[elim_state].items():
        if DFA[elim_state].get(transition) == elim_state:
            cycle_transition = transition
        else:
            end_state = DFA[elim_state].get(transition)
            end_transition = transition

    # find starting state
    init_state = None
    init_transition = None
    for state in DFA.keys():
        for letter in alphabet:
            if DFA[state].get(letter) == elim_state and state != end_state:
                init_state = state
                init_transition = letter
                break

    print('Init state: ', init_state)
    print('Init transition: ', init_transition)
    print('Cycle Transition' , cycle_transition)
    print('End State: ', end_state)
    print('End Transition: ', end_transition)
    print()

    DFA.pop(elim_state)
    new_transition = init_transition + ' ' + end_transition

    # created cycle
    for transition, state in DFA[end_state].items():
        if state == elim_state:
            DFA[end_state].pop(transition)
            created_cycle_transition = transition + end_transition
            DFA[end_state].update({created_cycle_transition: end_state})
    DFA[init_state] = {new_transition: end_state}

    print()
    for key, value in DFA.items():
        print(key, value)
    
# Print the DFA
print()
for key, value in DFA.items():
    print(key, value)