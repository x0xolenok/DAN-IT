# У класі професора Грубла щойно був іспит.
# Він почав перевіряти роботи, але оцінював їх не дуже уважно.
# Напишіть програму, яка приймає як вхідні дані оцінку кожного учня і те, чи здав він іспит.
# Потім програмі необхідно надрукувати дві речі:
# a. Чи був професор Грубл послідовним у проставленні позначки "Passed" для студентів.
# b. Якщо професор Грубл був послідовним, виведіть діапазон у якому знаходиться поріг для складання іспиту.

grades = [70, 70, 70]
results = ["Passed", "Failed", "Passed"]

passed_scores = []
failed_scores = []

for i in range(len(grades)):
    if results[i] == "Passed":
        passed_scores.append(grades[i])
    else:
        failed_scores.append(grades[i])

# Перевірка послідовності
consistent = True
for p in passed_scores:
    for f in failed_scores:
        if p <= f:  # якщо хоча б один склав з гіршим або рівним балом
            consistent = False

if not consistent:
    print("Професор був непослідовний")
else:
    print("Професор був послідовний")
    # Діапазон прохідного балу можна обчислити лише якщо є обидві групи
    if passed_scores and failed_scores:
        min_passed = min(passed_scores)
        max_failed = max(failed_scores)
        print("Поріг складання іспиту знаходиться в діапазоні:", max_failed + 1, "-", min_passed)
    else:
        print("Недостатньо даних для визначення порогу (усі склали або усі не склали)")
