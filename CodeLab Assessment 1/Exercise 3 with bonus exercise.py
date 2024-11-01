import tkinter as tk
from tkinter import messagebox, ttk
import csv

# the main class for studentmanagement app with all the function in it creating a good student management system.
class StudentManagementSystem:
    # In this function we setup the variables and call the display fucntions
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1000x700")
        self.students = []
        self.load_data()
        self.create_menu_frame()
        self.create_display_frame()
        
    # this function include all the left pannel clickable buttons which does something for student managemennt system.
    def create_menu_frame(self):
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(menu_frame, text="Student\nManagement\nSystem", 
                font=('Helvetica', 14, 'bold')).pack(pady=20)
        
        buttons = [
            ("View All Records", self.view_all_records),
            ("View Individual Record", self.show_student_selection),
            ("Sort Records", self.show_sort_options),
            ("Highest Score", self.show_highest_score),
            ("Lowest Score", self.show_lowest_score),
            ("Add Student", self.show_add_student),
            ("Update Student", self.show_update_student),
            ("Delete Student", self.show_delete_student)
        ]
        
        for text, command in buttons:
            tk.Button(menu_frame, text=text, command=command, width=20).pack(pady=5)
    
    # this function display the frames to hold widgets.
    def create_display_frame(self):
        self.display_frame = tk.Frame(self.root)
        self.display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.display_text = tk.Text(self.display_frame, wrap=tk.WORD, font=('Courier', 11))
        scrollbar = ttk.Scrollbar(self.display_frame, command=self.display_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.display_text.pack(fill=tk.BOTH, expand=True)
        self.display_text.config(yscrollcommand=scrollbar.set)

# it loads the data from the studentmarks file using try block.
    def load_data(self):
        try:
            with open('studentMarks.txt', 'r') as file:
                reader = csv.reader(file)
                next(reader)
                self.students = [{'id': row[0], 'name': row[1], 'course1': int(row[2]),
                               'course2': int(row[3]), 'course3': int(row[4]), 'exam': int(row[5])}
                               for row in reader]
        except FileNotFoundError:
            messagebox.showinfo("Info", "No data file found. Starting with empty database.")

#it saves the data that is being updated once the program is executed.
    def save_data(self):
        with open('studentMarks.txt', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([len(self.students)])
            for s in self.students:
                writer.writerow([s['id'], s['name'], s['course1'], s['course2'], s['course3'], s['exam']])

# this function calculate the grades, percentage and total marks of the new student we add.
    def calculate_results(self, student):
        coursework_total = student['course1'] + student['course2'] + student['course3']
        total_marks = coursework_total + student['exam']
        percentage = (total_marks / 160) * 100
        grade = 'A' if percentage >= 70 else 'B' if percentage >= 60 else 'C' if percentage >= 50 else 'D' if percentage >= 40 else 'F'
        return coursework_total, percentage, grade

# this function formats to student details into a strutural string for a good interface.
    def format_student_info(self, student):
        coursework_total, percentage, grade = self.calculate_results(student)
        return f"\n{'='*50}\nStudent Name: {student['name']}\nStudent Number: {student['id']}" \
               f"\nCourse Marks: {student['course1']}, {student['course2']}, {student['course3']}" \
               f"\nTotal Coursework: {coursework_total}\nExam Mark: {student['exam']}" \
               f"\nOverall Percentage: {percentage:.1f}%\nGrade: {grade}\n{'='*50}\n"

# this function sorts the students names according to the filter provided by the user.
    def show_sort_options(self):
        if not self.students:
            messagebox.showinfo("Info", "No student records found.")
            return
            
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sort Records")
        sort_window.geometry("300x250")
        
        sort_by = tk.StringVar(value="percentage")
        sort_order = tk.StringVar(value="descending")
        
        for text, value in [("Overall Percentage", "percentage"), ("Student ID", "id"),
                          ("Student Name", "name"), ("Exam Mark", "exam")]:
            tk.Radiobutton(sort_window, text=text, variable=sort_by, 
                          value=value).pack(anchor='w', padx=10)
            
        for text, value in [("Ascending", "ascending"), ("Descending", "descending")]:
            tk.Radiobutton(sort_window, text=text, variable=sort_order, 
                          value=value).pack(anchor='w', padx=10)
            
        tk.Button(sort_window, text="Apply Sort",
                 command=lambda: [self.sort_and_display(sort_by.get(), 
                 sort_order.get()), sort_window.destroy()]).pack(pady=10)
#in this after the filter is selected in the correct student list is displayed.
    def sort_and_display(self, criteria, order):
        key_func = lambda s: (self.calculate_results(s)[1] if criteria == "percentage" 
                            else s['exam'] if criteria == "exam" else s[criteria])
        self.students.sort(key=key_func, reverse=(order == "descending"))
        
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, f"Records sorted by {criteria} in {order} order:\n\n")
        total_percentage = sum(self.calculate_results(s)[1] for s in self.students)
        
        for student in self.students:
            self.display_text.insert(tk.END, self.format_student_info(student))
            
        self.display_text.insert(tk.END, f"\nSummary:\nTotal Students: {len(self.students)}\n"
                               f"Class Average: {total_percentage/len(self.students):.1f}%\n")

# in this function it displays all the student record that are present in the .txt file.
    def view_all_records(self):
        if not self.students:
            messagebox.showinfo("Info", "No student records found.")
            return
        
        self.display_text.delete(1.0, tk.END)
        total_percentage = sum(self.calculate_results(s)[1] for s in self.students)
        
        for student in self.students:
            self.display_text.insert(tk.END, self.format_student_info(student))
            
        self.display_text.insert(tk.END, f"\nSummary:\nTotal Students: {len(self.students)}\n"
                               f"Class Average: {total_percentage/len(self.students):.1f}%\n")

# this function helps choose from the list of student and show the details of the selected student only.
    def show_student_selection(self):
        if not self.students:
            messagebox.showinfo("Info", "No student records found.")
            return
        
        select_window = tk.Toplevel(self.root)
        select_window.title("Select Student")
        select_window.geometry("300x250")
        listbox = tk.Listbox(select_window, selectmode=tk.SINGLE)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for student in self.students:
            listbox.insert(tk.END, f"{student['id']} - {student['name']}")
            
        tk.Button(select_window, text="Show Record",
                 command=lambda: [self.display_text.delete(1.0, tk.END),
                                self.display_text.insert(tk.END, 
                                self.format_student_info(self.students[listbox.curselection()[0]])),
                                select_window.destroy()]).pack(pady=10)

# this function shows the details of student that have the highest score using if statement.
    def show_highest_score(self):
        if not self.students:
            messagebox.showinfo("Info", "No student records found.")
            return
        self.display_text.delete(1.0, tk.END)
        highest_student = max(self.students, key=lambda s: self.calculate_results(s)[1])
        self.display_text.insert(tk.END, "Highest Scoring Student:\n" + 
                               self.format_student_info(highest_student))

# this function shows the details of student that have the lowest score using if statement.
    def show_lowest_score(self):
        if not self.students:
            messagebox.showinfo("Info", "No student records found.")
            return
        self.display_text.delete(1.0, tk.END)
        lowest_student = min(self.students, key=lambda s: self.calculate_results(s)[1])
        self.display_text.insert(tk.END, "Lowest Scoring Student:\n" + 
                               self.format_student_info(lowest_student))

# this function add student to students list and update it in the .txt file.
    def show_add_student(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Student")
        add_window.geometry("300x250")
        
        fields = [("Student ID (1000-9999):", 'id'), ("Name:", 'name'),
                 ("Course 1 Mark (0-20):", 'course1'), ("Course 2 Mark (0-20):", 'course2'),
                 ("Course 3 Mark (0-20):", 'course3'), ("Exam Mark (0-100):", 'exam')]
        
        entries = {}
        for label_text, key in fields:
            tk.Label(add_window, text=label_text).pack()
            entries[key] = tk.Entry(add_window)
            entries[key].pack()

        def save_student():
            try:
                student_id = entries['id'].get()
                if not (1000 <= int(student_id) <= 9999):
                    raise ValueError("Invalid Student ID")
                if any(s['id'] == student_id for s in self.students):
                    raise ValueError("Student ID already exists")
                    
                name = entries['name'].get().strip()
                if not name:
                    raise ValueError("Name cannot be empty")
                    
                marks = [int(entries[f'course{i}'].get()) for i in range(1, 4)]
                exam = int(entries['exam'].get())
                
                if not all(0 <= m <= 20 for m in marks) or not 0 <= exam <= 100:
                    raise ValueError("Invalid marks")
                    
                self.students.append({
                    'id': student_id,
                    'name': name,
                    'course1': marks[0],
                    'course2': marks[1],
                    'course3': marks[2],
                    'exam': exam
                })
                self.save_data()
                messagebox.showinfo("Success", "Student added successfully")
                add_window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                
        tk.Button(add_window, text="Save Student", command=save_student).pack(pady=10)

# this function update the student information if needed.
    def show_update_student(self):
        if not self.students:
            messagebox.showinfo("Info", "No student records found.")
            return
            
        update_window = tk.Toplevel(self.root)
        update_window.geometry("300x250")
        update_window.title("Update Student")
        
        tk.Label(update_window, text="Select Student:").pack(pady=5)
        student_var = tk.StringVar()
        student_list = [f"{s['id']} - {s['name']}" for s in self.students]
        student_menu = ttk.Combobox(update_window, textvariable=student_var, values=student_list)
        student_menu.pack(pady=5)
        
        tk.Label(update_window, text="Select Field to Update:").pack(pady=5)
        field_var = tk.StringVar()
        fields = ['name', 'course1', 'course2', 'course3', 'exam']
        field_menu = ttk.Combobox(update_window, textvariable=field_var, values=fields)
        field_menu.pack(pady=5)
        
        tk.Label(update_window, text="New Value:").pack(pady=5)
        new_value = tk.Entry(update_window)
        new_value.pack(pady=5)
        
        def update_record():
            try:
                student_id = student_var.get().split(' - ')[0]
                student = next(s for s in self.students if s['id'] == student_id)
                field = field_var.get()
                value = new_value.get()
                
                if field == 'name':
                    if not value.strip():
                        raise ValueError("Name cannot be empty")
                    student['name'] = value
                else:
                    num_value = int(value)
                    if field == 'exam' and not 0 <= num_value <= 100:
                        raise ValueError("Exam mark must be between 0 and 100")
                    elif field.startswith('course') and not 0 <= num_value <= 20:
                        raise ValueError("Course mark must be between 0 and 20")
                    student[field] = num_value
                
                self.save_data()
                messagebox.showinfo("Success", "Record updated successfully")
                update_window.destroy()
                self.view_all_records()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                
        tk.Button(update_window, text="Update Record", command=update_record).pack(pady=10)

# this function helps delete a student from the student list and .txt file.
    def show_delete_student(self):
        if not self.students:
            messagebox.showinfo("Info", "No student records found.")
            return
            
        delete_window = tk.Toplevel(self.root)
        delete_window.geometry("300x250")
        delete_window.title("Delete Student")
        
        listbox = tk.Listbox(delete_window, selectmode=tk.SINGLE)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for student in self.students:
            listbox.insert(tk.END, f"{student['id']} - {student['name']}")
            
        def delete_selected():
            if listbox.curselection() and messagebox.askyesno("Confirm", "Delete this student?"):
                del self.students[listbox.curselection()[0]]
                self.save_data()
                messagebox.showinfo("Success", "Student deleted successfully")
                delete_window.destroy()
                
        tk.Button(delete_window, text="Delete Student", command=delete_selected).pack(pady=10)

# this is the main function it intialize the root function and start the app.
def main():
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()