import pdfplumber
import matplotlib.pyplot as plt
#-----------------------------------------------
# Acquires the file path to extract the needed table

file_name = input("Please enter your grade file relative path:")
with pdfplumber.open(file_name) as f:
    for i in f.pages:
        og_table_data = i.extract_tables()

table_data = og_table_data[0]  # Assuming the first table extracted is the relevant one
#-----------------------------------------------
subject_grades = {}

for row in table_data[1:]:  # Start from index 1 to skip the header row
    subject = row[0]  # Get the subject name
    if "mājasdarbi" in subject.lower():  # Skip subjects containing "mājasdarbi" (case insensitive)
        continue

    grades = []

    first_grade_found = False
    for item in row[1:]:
        for substring in item.split():
            try:
                if '%' not in substring:
                    number = ''.join(filter(str.isdigit, substring))
                    if number:
                        number_int = int(number)
                        if 0 < number_int <= 10:
                            grades.append(number_int)
                            if not first_grade_found:
                                start_of_grade = number_int
                                first_grade_found = True
            except ValueError:
                pass
    subject_grades[subject] = (grades, start_of_grade)

# Creating a dictionary to store all grades data for non-"mājasdarbi" subjects
all_grades_data = {subject: grades for subject, (grades, _) in subject_grades.items()}
#-----------------------------------------------
plt.figure(figsize=(10, 8))

for subject, grades in all_grades_data.items():
    months = [i for i in range(len(grades))]  # x-axis representing months (indexes)
    plt.plot(months, grades, marker='o', label=subject)

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

plt.title('Combined Grades for All Subjects (Excluding "mājasdarbi")')
plt.xlabel('Months')
plt.ylabel('Grades (0-10)')
plt.xticks(months, [f'Month {i + 1}' for i in range(len(months))])
plt.yticks(range(11))
plt.legend()
plt.grid(True)
average_status_of_grades = 0
for subject, trend in grade_trends.items():
    if "mājasdarbi" not in subject.lower():  # Skip "mājasdarbi" subjects (case insensitive)
        if trend == "up":
            print(f"Good job! {subject}'s grades have gone up!")
            average_status_of_grades += 1
        elif trend == "down":
            print(f"Could be better. {subject}'s grades have gone down!")
            average_status_of_grades -= 1
        else:
            print(f"No significant change in {subject}'s grades.")

# Determine the overall status of grades
if average_status_of_grades > 0:
    print("Overall your grades have gone up!")
elif average_status_of_grades < 0:
    print("Overall your grades have gone down!")
else:
    print("Overall your grades have stayed the same")

plt.show()



