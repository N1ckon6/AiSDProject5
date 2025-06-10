import os
from functions import (
    brute_force_knapsack,
    dynamic_programming_knapsack,
    experiment_varying_C,
    experiment_varying_n,
    generate_items,
    plot_results,
    read_from_file,
    save_to_file
    )

project_folder = os.path.dirname(os.path.abspath(__file__))

def main():
    # Ustawienia eksperymentów
    max_n = 30  # Maksymalna liczba przedmiotów
    fixed_C = 50  # Stała pojemność plecaka
    step_n = 1   # Krok dla n
    
    max_C = 200  # Maksymalna pojemność plecaka
    fixed_n = 10  # Stała liczba przedmiotów
    step_C = 10   # Krok dla C
    
    # Utwórz folder knapsack_data w folderze AiSDProject5
    data_folder = os.path.join(project_folder, "knapsack_data")
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        print(f"Utworzono folder: {data_folder}")
    
    # Najpierw generujemy plik z danymi
    items = generate_items(fixed_n)
    filename = os.path.join(data_folder, f"knapsack_data_n{fixed_n}.txt")
    save_to_file(filename, fixed_C, items)
    print(f"Wygenerowano plik z danymi: {filename}")
    
    # Teraz możemy bezpiecznie odczytać dane
    print("\nPrzykład użycia dla konkretnego przypadku:")
    C, items = read_from_file(filename)
    print(f"Pojemność plecaka: {C}")
    print(f"Przedmioty: {items}")
    
    # Brute force
    bf_items, bf_value = brute_force_knapsack(C, items)
    print("\nBrute Force:")
    print(f"Wybrane przedmioty: {bf_items}")
    print(f"Maksymalna wartość: {bf_value}")
    
    # Dynamic programming
    dp_items, dp_value = dynamic_programming_knapsack(C, items)
    print("\nDynamic Programming:")
    print(f"Wybrane przedmioty: {dp_items}")
    print(f"Maksymalna wartość: {dp_value}")
    
    # Eksperymenty
    print("\nPrzeprowadzanie eksperymentów...")
    n_values, bf_times_n, dp_times_n = experiment_varying_n(max_n, fixed_C, step_n, data_folder)  # Pass data_folder
    plot_results(project_folder, n_values, bf_times_n, dp_times_n,
            f'Czas wykonania dla stałej pojemności C={fixed_C}',
            'Liczba przedmiotów (n)')
    
    C_values, bf_times_C, dp_times_C = experiment_varying_C(fixed_n, max_C, step_C, data_folder)  # Also update experiment_varying_C similarly
    plot_results(project_folder, C_values, bf_times_C, dp_times_C,
            f'Czas wykonania dla stałej liczby przedmiotów n={fixed_n}',
            'Pojemność plecaka (C)')

if __name__ == "__main__":
    main()