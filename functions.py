import itertools
import os
import time
import random
import matplotlib.pyplot as plt

def generate_items(n, max_weight=50, max_value=100):
    """Generuje listę przedmiotów o losowych wagach i wartościach"""
    return [(f'P{i}', random.randint(1, max_weight), random.randint(1, max_value)) 
            for i in range(1, n+1)]

def save_to_file(filename, C, items):
    """Zapisuje dane do pliku w wymaganym formacie"""
    with open(filename, 'w') as f:
        f.write(f"{C}\n")
        f.write(f"{len(items)}\n")
        for item in items:
            f.write(f"{item[0]} {item[1]} {item[2]}\n")

def read_from_file(filename):
    """Wczytuje dane z pliku"""
    with open(filename, 'r') as f:
        lines = f.readlines()
        C = int(lines[0].strip())
        n = int(lines[1].strip())
        items = []
        for line in lines[2:]:
            parts = line.strip().split()
            items.append((parts[0], int(parts[1]), int(parts[2])))
    return C, items

def brute_force_knapsack(C, items):
    """Rozwiązanie problemu plecakowego metodą siłową"""
    max_value = 0
    best_combination = []
    n = len(items)
    
    # Generujemy wszystkie możliwe kombinacje przedmiotów
    for r in range(1, n+1):
        for combination in itertools.combinations(items, r):
            total_weight = sum(item[1] for item in combination)
            total_value = sum(item[2] for item in combination)
            
            if total_weight <= C and total_value > max_value:
                max_value = total_value
                best_combination = combination
                
    return best_combination, max_value

def dynamic_programming_knapsack(C, items):
    """Rozwiązanie problemu plecakowego metodą programowania dynamicznego"""
    n = len(items)
    # Tworzymy tabelę do przechowywania maksymalnych wartości
    dp = [[0] * (C + 1) for _ in range(n + 1)]
    
    # Wypełniamy tabelę dp
    for i in range(1, n + 1):
        name, weight, value = items[i-1]
        for w in range(1, C + 1):
            if weight <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - weight] + value)
            else:
                dp[i][w] = dp[i-1][w]
    
    # Odtwarzamy wybrane przedmioty
    max_value = dp[n][C]
    w = C
    selected_items = []
    
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_items.append(items[i-1])
            w -= items[i-1][1]
    
    return selected_items, max_value

def measure_time(algorithm, C, items, repetitions=1):
    """Mierzy czas wykonania algorytmu"""
    total_time = 0
    for _ in range(repetitions):
        start_time = time.time()
        algorithm(C, items)
        total_time += time.time() - start_time
    return total_time / repetitions

def experiment_varying_n(max_n, C, step=1, data_folder='knapsack_data', filename_prefix='knapsack_data'):
    """Eksperyment z różną liczbą przedmiotów"""
    brute_force_times = []
    dp_times = []
    n_values = list(range(1, max_n + 1, step))
    
    for n in n_values:
        items = generate_items(n)
        filename = os.path.join(data_folder, f"{filename_prefix}_n{n}.txt")  # Use os.path.join
        save_to_file(filename, C, items)
        
        # Pomiar czasu dla brute force (tylko dla małych n)
        if n <= 20:  # Brute force staje się bardzo wolny dla większych n
            bf_time = measure_time(brute_force_knapsack, C, items)
            brute_force_times.append(bf_time)
        else:
            brute_force_times.append(None)
        
        # Pomiar czasu dla programowania dynamicznego
        dp_time = measure_time(dynamic_programming_knapsack, C, items)
        dp_times.append(dp_time)
    
    return n_values, brute_force_times, dp_times

def experiment_varying_C(n, max_C, step=10, data_folder='knapsack_data', filename_prefix='knapsack_data'):
    """Eksperyment z różną pojemnością plecaka"""
    brute_force_times = []
    dp_times = []
    C_values = list(range(10, max_C + 1, step))
    items = generate_items(n)
    
    for C in C_values:
        filename = os.path.join(data_folder, f"{filename_prefix}_C{C}.txt")  # Use os.path.join
        save_to_file(filename, C, items)
        
        # Pomiar czasu dla brute force
        bf_time = measure_time(brute_force_knapsack, C, items)
        brute_force_times.append(bf_time)
        
        # Pomiar czasu dla programowania dynamicznego
        dp_time = measure_time(dynamic_programming_knapsack, C, items)
        dp_times.append(dp_time)
    
    return C_values, brute_force_times, dp_times

def plot_results(project_folder, n_values, bf_times, dp_times, title, xlabel):
    """Generates LaTeX tikz code for performance comparison plots"""
    # Filter out None values for Brute Force
    valid_bf = [(x, y) for x, y in zip(n_values, bf_times) if y is not None]
    
    tikz_code = f"""\\begin{{tikzpicture}}
\\begin{{axis}}[
    title={{{title}}},
    xlabel={{{xlabel}}},
    ylabel={{Czas wykonania (s)}},
    legend pos=north west,
    grid=major,
    width=0.9\\textwidth,
    height=0.6\\textwidth,
    xmin={min(n_values)},
    xmax={max(n_values)},
    ymin=0,
    ymax={max([t for t in dp_times + [t for _, t in valid_bf] if t is not None]) * 1.1},
    scaled y ticks=false,
    y tick label style={{/pgf/number format/fixed}},
    mark options={{solid}}]
    
"""

    # Add Brute Force data if available
    if valid_bf:
        bf_x, bf_y = zip(*valid_bf)
        tikz_code += "\\addplot [\n    color=red,\n    mark=*,\n    ]\n    coordinates {\n"
        for x, y in zip(bf_x, bf_y):
            tikz_code += f"        ({x}, {y:.6f})\n"
        tikz_code += "    };\n    \\addlegendentry{Brute Force}\n\n"

    # Add Dynamic Programming data
    tikz_code += "\\addplot [\n    color=blue,\n    mark=square*,\n    ]\n    coordinates {\n"
    for x, y in zip(n_values, dp_times):
        tikz_code += f"        ({x}, {y:.6f})\n"
    tikz_code += "    };\n    \\addlegendentry{Dynamic Programming}\n\n"

    tikz_code += """\\end{axis}
\\end{tikzpicture}"""

    # Save to a .tex file
    plot_filename = f"plot_{title.replace(' ', '_').lower()}.txt"
    full_path = os.path.join(project_folder, plot_filename)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(tikz_code)

    print(f"Generated LaTeX plot file: {full_path}")