import sys

class PDA:
    def __init__(self, transitions, start_state, accept_states, accept_by_empty_stack=False):
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
        self.accept_by_empty_stack = accept_by_empty_stack

    def accepts(self, input_string):
        # Usa busca em profundidade para simular PDA não determinístico
        stack = []
        return self._dfs(self.start_state, input_string, stack)

    def _dfs(self, state, remaining_input, stack):
        # Condição de aceitação
        if not remaining_input:
            if self.accept_by_empty_stack and not stack:
                return True
            if not self.accept_by_empty_stack and state in self.accept_states:
                return True

        # Transições possíveis
        current_symbol = remaining_input[0] if remaining_input else None
        stack_top = stack[-1] if stack else None

        possible_moves = []
        if (state, current_symbol, stack_top) in self.transitions:
            possible_moves.extend(self.transitions[(state, current_symbol, stack_top)])
        if (state, None, stack_top) in self.transitions:  # ε-transição
            possible_moves.extend(self.transitions[(state, None, stack_top)])

        for (next_state, push_symbols) in possible_moves:
            new_stack = stack.copy()
            if stack_top:
                new_stack.pop()
            if push_symbols:
                for sym in reversed(push_symbols):
                    new_stack.append(sym)

            new_input = remaining_input[1:] if current_symbol else remaining_input
            if self._dfs(next_state, new_input, new_stack):
                return True

        return False


def load_transitions(file_path):
    transitions = {}
    start_state = None
    accept_states = set()

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if parts[0] == "start":
                start_state = parts[1]
            elif parts[0] == "accept":
                accept_states.add(parts[1])
            else:
                # Formato: estado símbolo pilha_topo -> prox_estado push
                state, symbol, stack_top, arrow, next_state, push = parts
                symbol = None if symbol == "ε" else symbol
                stack_top = None if stack_top == "ε" else stack_top
                push_symbols = [] if push == "ε" else list(push)

                transitions.setdefault((state, symbol, stack_top), []).append((next_state, push_symbols))

    return transitions, start_state, accept_states


def main():
    transitions, start_state, accept_states = load_transitions("transitions.txt")
    pda = PDA(transitions, start_state, accept_states, accept_by_empty_stack=False)

    with open("patterns.txt", "r") as f:
        patterns = f.read().split()

    output = []
    for word in patterns:
        if pda.accepts(word):
            output.append("*")
        else:
            output.append(word)

    with open("output.txt", "w") as f:
        f.write(" ".join(output))


if __name__ == "__main__":
    main()
