import random

def char_model(input, first, second):
    if input.endswith('.txt'):
        # Leer el archivo
        with open(input, 'r', encoding='utf-8') as f:
            text = f.read()
        letters = list(text)

        # Crear un diccionario para contar trigramas
        tri_counts = {}
        for i in range(0, len(letters) - 2):
            first = letters[i]
            second = letters[i + 1]
            curr = letters[i + 2]
            if (first, second) not in tri_counts:
                tri_counts[(first, second)] = {}
            if curr not in tri_counts[(first, second)]:
                tri_counts[(first, second)][curr] = 1
            else:
                tri_counts[(first, second)][curr] += 1

        # Crear un diccionario para las probabilidades
        probs = {}
        for history in tri_counts:
            probs[history] = {}
            total = sum(tri_counts[history].values())  # Total de apariciones para ese historial
            for next_char in tri_counts[history]:
                probs[history][next_char] = tri_counts[history][next_char] / total

        # Generar nuevo texto a partir del historial
        new_text = [first, second]
        history = (first, second)
        for i in range(0, len(text) - 2):
            if history in probs:
                new_letter = random.choices(population=list(probs[history].keys()),
                                            weights=list(probs[history].values()), 
                                            k=1)[0]
                new_text.append(new_letter)
                first = new_text[-2]
                second = new_text[-1]
                history = (first, second)
            else:
                break  # Si no se encuentra el historial, se detiene

        return ''.join(new_text)
    else:
        return 'El input no es un .txt'
