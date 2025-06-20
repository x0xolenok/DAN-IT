# 4. Використовуйте модуль часу, щоб порівняти продуктивність «ефективного» методу пошуку
# простих чисел із простою реалізацією (без перерв, тестування за всіма числами тощо).
#
# Перевірте кілька діапазонів пошуку простих чисел (наприклад, до 100, до 1000 і т.д.)
#
# Ефективний метод - будь який математично визначиний підхід обрахунку.
#
# Рекомендую дивитись метод Решето Эратосфена - https://uk.wikipedia.org/wiki/Решето_Ератосфена

import time

# Простий метод пошуку простих чисел
def simple_primes(n):
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, num):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

# Метод Решето Ератосфена
def sieve_primes(n):
    numbers = [True] * (n + 1)
    numbers[0] = False
    numbers[1] = False

    for i in range(2, n + 1):
        if numbers[i]:
            for j in range(i * 2, n + 1, i):
                numbers[j] = False

    primes = []
    for i in range(len(numbers)):
        if numbers[i]:
            primes.append(i)
    return primes


ranges = [100, 1000, 10000]

for limit in ranges:
    print("\nПеревірка до", limit)

    # Простий метод
    start = time.time()
    simple = simple_primes(limit)
    end = time.time()
    print("Простий метод:", round(end - start, 5), "секунд")

    # Решето Ератосфена
    start = time.time()
    sieve = sieve_primes(limit)
    end = time.time()
    print("Решето Ератосфена:", round(end - start, 5), "секунд")
