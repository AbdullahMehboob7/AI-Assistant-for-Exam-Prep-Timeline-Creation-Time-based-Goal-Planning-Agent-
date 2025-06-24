

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime, timedelta


class SmartExamPlanner:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("AI Exam Planner with Spaced Repetition")
        self.window.geometry("600x700")

        # Input Fields
        self.create_input_section()

        # Spaced Repetition Settings
        self.create_spaced_repetition_settings()

        # Output
        self.output = tk.Text(self.window, height=20, width=80)
        self.output.pack(pady=10)

        # Buttons
        ttk.Button(self.window, text="Generate Smart Plan",
                   command=self.generate_plan).pack()
        ttk.Button(self.window, text="Export to CSV",
                   command=self.export_csv).pack()

    def create_input_section(self):
        frame = ttk.LabelFrame(self.window, text="Exam Details")
        frame.pack(pady=10, fill="x", padx=10)

        ttk.Label(frame, text="Exam Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="w")
        self.date_entry = ttk.Entry(frame)
        self.date_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Subjects (comma separated):").grid(row=1, column=0, sticky="w")
        self.subjects_entry = ttk.Entry(frame)
        self.subjects_entry.grid(row=1, column=1)

        ttk.Label(frame, text="Daily Max Hours:").grid(row=2, column=0, sticky="w")
        self.hours_spinbox = ttk.Spinbox(frame, from_=1, to=8)
        self.hours_spinbox.grid(row=2, column=1)
        self.hours_spinbox.set(3)

    def create_spaced_repetition_settings(self):
        frame = ttk.LabelFrame(self.window, text="Spaced Repetition Settings")
        frame.pack(pady=10, fill="x", padx=10)

        ttk.Label(frame, text="Revision Intervals (days):").grid(row=0, column=0, sticky="w")
        self.intervals_entry = ttk.Entry(frame)
        self.intervals_entry.grid(row=0, column=1)
        self.intervals_entry.insert(0, "1,3,7")  # Default Ebbinghaus intervals

        ttk.Label(frame, text="Priority Subjects:").grid(row=1, column=0, sticky="w")
        self.priority_entry = ttk.Entry(frame)
        self.priority_entry.grid(row=1, column=1)

        ttk.Label(frame, text="Revision Duration (hrs):").grid(row=2, column=0, sticky="w")
        self.rev_duration = ttk.Spinbox(frame, from_=0.5, to=2, increment=0.5)
        self.rev_duration.grid(row=2, column=1)
        self.rev_duration.set(1)

    def generate_plan(self):
        try:
            # Get inputs
            exam_date = datetime.strptime(self.date_entry.get(), "%Y-%m-%d")
            subjects = [s.strip() for s in self.subjects_entry.get().split(",") if s.strip()]
            daily_hours = float(self.hours_spinbox.get())
            intervals = [int(i) for i in self.intervals_entry.get().split(",")]
            priority_subjects = [s.strip() for s in self.priority_entry.get().split(",") if s.strip()]
            rev_duration = float(self.rev_duration.get())

            # Calculate total days
            total_days = (exam_date - datetime.now()).days
            if total_days <= 0:
                raise ValueError("Exam date must be in the future!")

            # Generate base schedule
            plan = []
            study_dates = {}
            current_date = datetime.now()

            for subject in subjects:
                # Add study session
                study_date = current_date
                duration = 2 if subject in priority_subjects else 1.5

                plan.append([
                    f"Day {(study_date - datetime.now()).days + 1}",
                    study_date.strftime("%Y-%m-%d"),
                    subject,
                    f"{duration} hours",
                    "Study"
                ])

                # Track study dates for repetitions
                study_dates[subject] = study_date
                current_date += timedelta(days=1)

                # Add spaced repetitions for priority subjects
                if subject in priority_subjects:
                    for interval in intervals:
                        rev_date = study_date + timedelta(days=interval)
                        if rev_date.date() <= exam_date.date():
                            plan.append([
                                f"Day {(rev_date - datetime.now()).days + 1}",
                                rev_date.strftime("%Y-%m-%d"),
                                f"{subject} Revision",
                                f"{rev_duration} hour",
                                "Revision"
                            ])

            # Create DataFrame
            df = pd.DataFrame(plan, columns=["Day", "Date", "Topic", "Duration", "Type"])
            df = df.sort_values("Date")
            df.reset_index(drop=True, inplace=True)

            # Display
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, df.to_string())
            self.current_plan = df

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

    def export_csv(self):
        try:
            self.current_plan.to_csv("smart_study_plan.csv", index=False)
            messagebox.showinfo("Success", "Plan saved as 'smart_study_plan.csv'")
        except:
            messagebox.showerror("Error", "Generate a plan first!")


if __name__ == "__main__":
    app = SmartExamPlanner()
    app.window.mainloop()