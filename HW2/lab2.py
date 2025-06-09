# 1. Як вхідні дані запитайте ціле число.
# Якщо воно ділиться на 3, виведіть "foo";
# якщо воно ділиться на 5, виведіть "bar";
# якщо воно ділиться на обидва, виведіть "ham" (а не "foo" або "bar").
print("Task 1")
number = int(input("Введіть ціле число: "))

if number % 3 == 0 and number % 5 == 0:
    print("ham")
elif number % 3 == 0:
    print("foo")
elif number % 5 == 0:
    print("bar")
else:
    print("Спробуйте ще раз)")

#2. Як вхідні дані запитайте два числа та виведіть яке з них менше і яке більше

print("Task 2")
a = float(input("Введіть перше число: "))
b = float(input("Введіть друге число: "))


if a > b:
    print("Більше число:", a)
    print("Менше число:", b)
elif a < b:
    print("Більше число:", b)
    print("Менше число:", a)
else:
    print("Обидва числа рівні:", a)


# 3 Як вхідні дані запитайте три числа і виведіть найменше, середнє та найбільше.
# Припустимо, всі вони різні
print("Task 3")

d = float(input("Введіть число d: "))
e = float(input("Введіть число e: "))
f = float(input("Введіть число f: "))

if d < e and d < f:
    minimum = d
elif e < d and e < f:
    minimum = e
else:
    minimum = f

if d > e and d > f:
    maximum = d
elif e > d and e > f:
    maximum = e
else:
    maximum = f

if (d != minimum) and (d != maximum):
    middle = d
elif (e != minimum) and (e != maximum):
    middle = e
else:
    middle = f

print("Найменше число:", minimum)
print("Середнє число:", middle)
print("Найбільше число:", maximum)


#4. Зіграйте у гру Fizz-Buzz: виведіть усі числа від 1 до 100;
# якщо число ділиться на 3, замість числа виведіть "fizz".
# Якщо воно ділиться на 5, замість числа виведіть "Buzz".
# Якщо воно ділиться на обидва, виведіть "fizz buzz" замість числа.

print("Task 4: Fizz-Buzz")
for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:
        print("fizz buzz")
    elif i % 3 == 0:
        print("fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)

#5. Зіграйте у гру 7-boom: виведіть усі числа від 1 до 100;
# якщо число ділиться на 7 або містить цифру 7, виведіть "BOOM" замість числа.

print("Task 5: 7-boom")
for x in range(1, 101):
    if x % 7 == 0 or '7' in str(x):
        print("BOOM")
    else:
        print(x)
