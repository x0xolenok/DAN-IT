# 1.Запросіть у користувача ім'я та місячну зарплату в доларах та виведіть їхню річну зарплату в тисячах доларів.
# Наприклад: «Мішель», «12345» → «Річна зарплата Мішель складає 148 тис. доларів».

username = input("Введіть ім’я: ")
salary_month = float(input("Введіть місячну зарплату в доларах: "))

salary_year = (salary_month * 12) / 1000

print(f"Річна зарплата {username} складає {int(salary_year)} тис. доларів.")


#2. Запросіть ціле число і виведіть True, якщо це парне число діапазоні від 100 до 999, інакше - «False».

number = int(input("Введіть ціле число:"))

bool = (number % 2 == 0) and (100 <= number <= 999)

print(bool)

# 3. Як вхідні дані візьмемо ціле число; Це буде ціле число від 101 до 999,
# а його остання цифра не дорівнює нулю(робити перевірку не обовʼязково)
# Виведіть число, що складається з чисел першого у зворотньому порядку.
#
# Наприклад: 256 → 652.

number1 = int(input("Введіть ціле число (від 101 до 999):"))

valid_number = number1 % 10 != 0

reversed_num = str(number1)[::-1]

print(reversed_num if valid_number else "Please, enter a valid number.(without 0 in the end)")

# 4. Запитайте два цілих числа та виведіть:
#
# a. Їхню суму
#
# b. Їхня різниця
#
# c. результат множення
#
# d. Результат поділу першого на друге
#
# e. Залишок від поділу першого на друге
#
# f. True, якщо перше число більше або дорівнює другому, інакше False.

num1 = int(input("Введіть перше число: "))
num2 = int(input("Введіть друге число: "))

sum = num1 + num2
diff = num1 - num2
mult = num1 * num2
comparison = num1 >= num2

print("Сума:", sum)
print("Різниця:", diff)
print("Добуток:", mult)

if num2 != 0:
    div = num1 // num2
    remainder = num1 % num2
    print("Ділення:", div)
    print("Залишок від ділення:", remainder)
else:
    print("Ділення: неможливо (ділення на нуль)")
    print("Залишок від ділення: неможливо (ділення на нуль)")

print("Перше число більше або дорівнює другому?:", comparison)
