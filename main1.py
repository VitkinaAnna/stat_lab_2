import random
import matplotlib.pyplot as plt

def generate_state_probabilities(num_states: int, add_zero: bool = False):
    # Генерує ймовірності для кожного стану
    probabilities = [random.randint(0, 10) for _ in range(num_states)]
    total = sum(probabilities)
    probabilities = [round(prob / total, 1) for prob in probabilities]

    if add_zero:
        probabilities.append(0.0)
    random.shuffle(probabilities)
    return probabilities


def generate_transition_matrix(num_states: int):
    # Генерує матрицю переходів між станами
    transition_matrix = []
    for _ in range(num_states):
        transition_matrix.append(generate_state_probabilities(num_states, add_zero=True))
    return transition_matrix


def random_next_state(row):
    # Вибирає наступний стан випадковим чином на основі ймовірностей у рядку
    value = random.random()
    state = 0
    while value > row[state] and state < len(row) - 1:
        value -= row[state]
        state += 1
    return state


def simulate_markov_chain(initial_probabilities, transition_matrix, num_steps, num_realizations):
    # Симулює поглинаючий ланцюг Маркова
    num_states = len(transition_matrix)
    states = [random_next_state(initial_probabilities) for _ in range(num_realizations)]
    realizations = [[] for _ in range(num_realizations)]

    while any(state != num_states for state in states):
        for i in range(num_realizations):
            realizations[i].append(states[i])
            if states[i] != num_states:
                states[i] = random_next_state(transition_matrix[states[i]])

    for i in range(num_realizations):
        realizations[i].append(states[i])

    return realizations


def regular_markov_chain_simulation(num_states, transition_matrix, initial_probabilities, num_steps, num_realizations):
    # Симулює регулярний ланцюг Маркова
    states = [random_next_state(initial_probabilities) for _ in range(num_realizations)]
    realizations = [[] for _ in range(num_realizations)]

    for _ in range(num_steps):
        for i in range(num_realizations):
            realizations[i].append(states[i])
            states[i] = random_next_state(transition_matrix[states[i]])

    return realizations


def plot_markov_chain(realizations, num_states, title_prefix=''):
    # Візуалізує ланцюг Маркова
    for i in range(min(len(realizations), 3)):
        realization_len = len(realizations[i])
        end_state = realizations[i][realization_len - 1]
        for j in range(realization_len):
            if realizations[i][realization_len - 1 - j] != end_state:
                end_index = j + 2
                break

        values = realizations[i][:realization_len - j + 1]
        y = values
        x = [i for i in range(len(values))]
        plt.plot(x, y)
        plt.xlabel('Крок часу')
        plt.ylabel('Стан')
        plt.title(f'{title_prefix} Реалізація {i}')
        plt.show()


def calculate_transition_matrix(realizations, num_states):
    # Обчислює матрицю переходів на основі симуляції
    transition_matrix = [[0.0 for _ in range(num_states + 1)] for _ in range(num_states + 1)]

    for time_step in range(len(realizations[0])):
        if time_step == 0:
            pre_states = [row[time_step] for row in realizations]
            continue
        current_states = [row[time_step] for row in realizations]
        for realization_idx in range(len(current_states)):
            transition_matrix[pre_states[realization_idx]][current_states[realization_idx]] += 1
        pre_states = current_states

    transition_matrix = [[round(value / sum(row), 3) for value in row] for row in transition_matrix]
    return transition_matrix


def calculate_state_times(realizations, num_states):
    # Обчислює середні часи перебування в кожному стані
    num_of_steps = [0.0] * (num_states + 1)
    duration_on_step = [0.0] * (num_states + 1)

    for time_step in range(len(realizations[0])):
        if time_step == 0:
            pre_states = [row[time_step] for row in realizations]
            continue
        current_states = [row[time_step] for row in realizations]

        for realization_idx in range(len(current_states)):
            num_of_steps[current_states[realization_idx]] += 1

            if current_states[realization_idx] != pre_states[realization_idx]:
                duration_on_step[current_states[realization_idx]] += 1

        pre_states = current_states

    state_times = [round(num_of_steps[i] / duration_on_step[i], 3) for i in range(num_states + 1)]
    return state_times


def main():
    """"""" Поглинаючий ланцюг Маркова """""""
    num_of_states_absorbing = 5
    transition_matrix_absorbing = [
        [0.1, 0.2, 0.3, 0.2, 0.0, 0.2],
        [0.2, 0.0, 0.5, 0.1, 0.1, 0.1],
        [0.0, 0.3, 0.6, 0.1, 0.0, 0.0],
        [0.1, 0.0, 0.1, 0.2, 0.5, 0.1],
        [0.2, 0.0, 0.1, 0.1, 0.4, 0.2],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    ]
    initial_probabilities_absorbing = [0.1, 0.1, 0.2, 0.2, 0.4]
    num_of_realizations_absorbing = 1000

    realizations_absorbing = simulate_markov_chain(
        initial_probabilities_absorbing,
        transition_matrix_absorbing,
        num_steps=1000,
        num_realizations=num_of_realizations_absorbing
    )

    plot_markov_chain(realizations_absorbing, num_of_states_absorbing, title_prefix='Поглинаючий')

    transition_matrix_absorbing_calculated = calculate_transition_matrix(realizations_absorbing,
                                                                         num_of_states_absorbing)
    for row in transition_matrix_absorbing_calculated:
        print(row)

    print("---------------")

    state_times_absorbing = calculate_state_times(realizations_absorbing, num_of_states_absorbing)
    print(state_times_absorbing)

    print("---------------")

    step_counts = [0.0] * len(realizations_absorbing)
    for time_step in range(len(realizations_absorbing[0])):
        current_states = [row[time_step] for row in realizations_absorbing]
        for realization_idx in range(len(current_states)):
            if current_states[realization_idx] != num_of_states_absorbing:
                step_counts[realization_idx] += 1

    print(round(sum(step_counts) / len(step_counts), 3))

    print("---------------")

    """""""Звичайний ланцюг Маркова"""""""""
    num_of_states_regular = 4
    transition_matrix_regular = [
        [0.1, 0.1, 0.3, 0.2, 0.3],
        [0.5, 0.1, 0.1, 0.3, 0.0],
        [0.3, 0.1, 0.4, 0.2, 0.0],
        [0.8, 0.1, 0.1, 0.0, 0.0],
        [0.2, 0.5, 0.1, 0.1, 0.1],
    ]
    initial_probabilities_regular = [0.2, 0.2, 0.2, 0.2, 0.2]
    num_of_realizations_regular = 1000
    num_steps_regular = 100

    realizations_regular = regular_markov_chain_simulation(
        num_of_states_regular,
        transition_matrix_regular,
        initial_probabilities_regular,
        num_steps_regular,
        num_of_realizations_regular
    )

    plot_markov_chain(realizations_regular, num_of_states_regular, title_prefix='Регулярний')

    transition_matrix_regular_calculated = calculate_transition_matrix(realizations_regular, num_of_states_regular)
    for row in transition_matrix_regular_calculated:
        print(row)

    state_times_regular = calculate_state_times(realizations_regular, num_of_states_regular)
    print(state_times_regular)

    flat_realization = []
    for row in realizations_regular:
        flat_realization.extend(row)
    plt.hist(flat_realization)
    plt.xlabel('Стан')
    plt.ylabel('Частота')
    plt.show()


if __name__ == "__main__":
    main()
