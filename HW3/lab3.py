# У класі професора Грубла щойно був іспит.
# Він почав перевіряти роботи, але оцінював їх не дуже уважно.
# Напишіть програму, яка приймає як вхідні дані оцінку кожного учня і те, чи здав він іспит.
# Потім програмі необхідно надрукувати дві речі:
# a. Чи був професор Грубл послідовним у проставленні позначки "Passed" для студентів.
# b. Якщо професор Грубл був послідовним, виведіть діапазон у якому знаходиться поріг для складання іспиту.

# Вхідні дані
grades = [84, 78, 65, 90, 72]
results = ["Passed", "Passed", "Failed", "Passed", "Failed"]

passed_scores = []
failed_scores = []

for i in range(len(grades)):
    if results[i] == "Passed":
        passed_scores.append(grades[i])
    else:
        failed_scores.append(grades[i])

consistent = True
for p in passed_scores:
    for f in failed_scores:
        if p < f:
            consistent = False

if not consistent:
    print("Професор був непослідовний")
else:
    min_passed = min(passed_scores)
    max_failed = max(failed_scores)
    print("Професор був послідовний")
    print("Поріг складання іспиту знаходиться в діапазоні:", max_failed + 1, "-", min_passed)
