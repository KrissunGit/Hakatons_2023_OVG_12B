import pdfplumber
import matplotlib.pyplot as plt

file_name = input("Please enter your grade file relative path:")
with pdfplumber.open(file_name) as f:
    for i in f.pages:
        og_table_data = i.extract_tables()

for i in og_table_data:
    table_data = i

subject_grades = {}

for row in table_data[1:]:  # Start from index 1 to skip the header row
    subject = row[0]  # Get the subject name
    grades = []

    first_grade_found = False
    for item in row[1:]:
        # Splitting the string by spaces and iterating through the resulting substrings
        for substring in item.split():
            try:
                # Extracting digits and converting to int
                number = ''.join(filter(str.isdigit, substring))
                if number:  # Check if digits were found
                    number_int = int(number)
                    if number_int <= 10:  # Check if the integer is 10 or less
                        grades.append(number_int)
                        if not first_grade_found:  # Set the first encountered grade as the benchmark
                            start_of_grade = number_int
                            first_grade_found = True
            except ValueError:
                pass  # Skip non-convertible values

    # Store the grades in the dictionary under the subject name
    subject_grades[subject] = (grades, start_of_grade)

for subject, (grades, start_of_grade) in subject_grades.items():
    months = [i for i in range(len(grades))]  # x-axis representing months (indexes)

    plt.figure(figsize=(8, 6))
    plt.plot(months, grades, marker='o')
    plt.title(f'Grades for {subject}')
    plt.xlabel('Months')
    plt.ylabel('Grades (0-10)')
    plt.xticks(months, [f'Month {i + 1}' for i in range(len(grades))])
    plt.yticks(range(11))
    plt.grid(True)
    plt.show()

# Check for grade trend
    grade_trends = {}
    for subject, (grades, start_of_grade) in subject_grades.items():
        if len(grades) > 1:
            if grades[-1] > start_of_grade:
                grade_trends[subject] = "up"
            elif grades[-1] < start_of_grade:
                grade_trends[subject] = "down"
            else:
                grade_trends[subject] = "unchanged"
        else:
            grade_trends[subject] = "no subsequent data"

    for subject, trend in grade_trends.items():
        if trend == "up":
            print(f"Good job! {subject}'s grades have gone up!")
        elif trend == "down":
            print(f"Could be better. {subject}'s grades have gone down!")
        else:
            print(f"No significant change in {subject}'s grades.")
