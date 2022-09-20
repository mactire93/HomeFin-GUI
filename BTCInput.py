# Funkcja służąca do wprowadzania tekstu i liczb

def read_text(prompt):
    ''' Wyświetla monit i czyta ciąg tekstu.
    Przerwania z klawiaturt CTRL+C są ignorowane'''
    while True: #potwarzaj w nieskończoność
        try:
            result = input(prompt) #czytaj dane wejściowe
            # skoro nie zgłoszono wyjątku, przerywamy działanie pętli
            break
        except KeyboardInterrupt:
            # działa w przypadky ctrl + c
            print('Wprowadź tekst')
    return result

def read_number(prompt, function):
    """
    Wyświetla monit i wczytuje liczbę zmiennoprzecinkową.
    Przerwania z klawiatury CTRL + C są ignorowane/
    Nieprawidłowe liczby są odrzucane.
    Zwraca liczbę zmiennoprzecinkową reprezentującą wartość wprowadzoną
    przez użytkownika
    """

    while True:
        try:
            number_text = read_text(prompt)
            result = function(number_text) # czytanie wejścia
            break
        except ValueError:
            print('Podaj liczbę')

    return result

def read_number_ranged(prompt, function, min_value, max_value):
    '''
    Wyświetla monit i wczytuje liczbę.
    min_value określa minimalną wartość (włącznie); 
    max_value określa wartość maksymalną (włącznie).
    Zgłasza wyjątek, jeśli max i min są podane odwrotnie
    Przerwania z klawiatury (Ctrl + C) są ignorowane.
    Nieprawidłowe liczby są odrzucane.
    Zwraca liczbę zmiennoprzecinkową reprezentującą wartość wprowadzoną przez użytkownika.
    '''

    if min_value > max_value:
        # jeśli parametry min i max zostały podane odwrotnie
        raise Exception('Wartość min. jest większa od wartości max!')

    while True:
        result = read_number(prompt, function)
        if result < min_value:
            # wprowadzona wartość jest za mała
            print('Ta liczba jest za mała!')
            print('Minimalna wartość to: ', min_value)
            continue
        if result > max_value:
            # Wprowadzona wartość jest zbyt duża
            print('Ta liczba jest za duża')
            print('Maksymalna wartość to:', max_value)
            continue
        break
    return result
    


def read_float(prompt):
    """
    wyświetla monit i wczytuje liczbę/
    Przerwania z klawiatury (CTRL + C) ssą ignorowane.
    Nieprawidłowe liczby są odrzucane.
    Zwraca liczbę zmiennoprzecinkową
    """

    while True:
        try:
            number_text = read_text(prompt)
            result = float(number_text) # wczytaj dane wejściowe
            break
        except ValueError:
            # jeśli użytkownik wprowadzi nieprawidłową liczbę
            print('Podaj liczbę')

    return result

def read_int(prompt):
    """
    wyświetla monit i wczytuje liczbę/
    Przerwania z klawiatury (CTRL + C) ssą ignorowane.
    Nieprawidłowe liczby są odrzucane.
    Zwraca liczbę integralną
    """

    while True:
        try:
            number_text = read_text(prompt)
            result = int(number_text)
            break
        except ValueError:
            print('Podaj liczbę całkowitą')

    return result

def read_int_ranged(prompt, min_value, max_value):
    '''
    Wyświetla monit i wczytuje liczbę całkowitą.
    min_value określa minimalną wartość (włącznie); 
    max_value określa wartość maksymalną (włącznie).
    Zgłasza wyjątek, jeśli max i min są podane odwrotnie
    Przerwania z klawiatury (Ctrl + C) są ignorowane.
    Nieprawidłowe liczby są odrzucane.
    Zwraca liczbę  reprezentującą wartość wprowadzoną przez użytkownika.
    '''
    return read_number_ranged(prompt, int, min_value, max_value)

def read_float_ranged(prompt, min_value, max_value):
    '''
    Wyświetla monit i wczytuje liczbę całkowitą.
    min_value określa minimalną wartość (włącznie); 
    max_value określa wartość maksymalną (włącznie).
    Zgłasza wyjątek, jeśli max i min są podane odwrotnie
    Przerwania z klawiatury (Ctrl + C) są ignorowane.
    Nieprawidłowe liczby są odrzucane.
    Zwraca liczbę  reprezentującą wartość wprowadzoną przez użytkownika.
    '''
    return read_number_ranged(prompt, float, min_value, max_value)


def readme():
    print('''Witaj w module BTCInput wersja 1.0

Możesz używać funkcji w module do czytania liczb i ciągów znaków w Twoich programach.
Funkcji używa się w następujący sposób:
text = read_text(prompt) 
int_value = read_int(prompt) 
float_value = read_float(prompt) 
int_value = read_int_ranged(prompt, max_value, min_value) 
float_value = read_float_ranged(prompt, max_value, min_value) 
Życzę przyjemnego korzystania.

Szafranu-san''')

if __name__ == '__main__':
    # przedstawienie się programu
    readme()

    input('\nAby zakończyć wciśnij Enter')

