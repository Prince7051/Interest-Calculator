"""Interest Calculator desktop UI using tkinter."""

import tkinter as tk
from tkinter import messagebox, ttk


def calculate_simple_interest(principal, rate, time):
    """Return simple interest using the standard formula."""
    return (principal * rate * time) / 100


def calculate_compound_interest(principal, rate, time):
    """Return compound interest using the standard formula."""
    amount = principal * (1 + rate / 100) ** time
    return amount - principal


def get_yearly_growth(principal, rate, years):
    """Return a list of yearly compound growth values."""
    whole_years = int(years)
    growth_rows = []

    for year in range(1, whole_years + 1):
        amount = principal * (1 + rate / 100) ** year
        growth_rows.append((year, amount))

    return growth_rows


class InterestCalculatorApp:
    """Simple desktop application for interest calculations."""

    def __init__(self, root):
        self.root = root
        self.root.title("Interest Calculator")
        self.root.geometry("560x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f7fb")

        self.principal_var = tk.StringVar()
        self.rate_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.result_var = tk.StringVar(
            value="Enter values and choose Simple Interest or Compound Interest."
        )

        self.build_ui()

    def build_ui(self):
        """Create the widgets for the calculator."""
        title = tk.Label(
            self.root,
            text="Interest Calculator",
            font=("Segoe UI", 20, "bold"),
            bg="#f4f7fb",
            fg="#1f3c88",
        )
        title.pack(pady=(18, 8))

        subtitle = tk.Label(
            self.root,
            text="Calculate Simple Interest and Compound Interest in Python",
            font=("Segoe UI", 10),
            bg="#f4f7fb",
            fg="#4a5568",
        )
        subtitle.pack(pady=(0, 12))

        form_frame = tk.Frame(self.root, bg="white", bd=1, relief="solid")
        form_frame.pack(padx=20, pady=10, fill="x")

        self.create_input_row(form_frame, "Principal Amount (P)", self.principal_var, 0)
        self.create_input_row(form_frame, "Rate of Interest (R %)", self.rate_var, 1)
        self.create_input_row(form_frame, "Time Period (T years)", self.time_var, 2)

        button_frame = tk.Frame(self.root, bg="#f4f7fb")
        button_frame.pack(pady=14)

        tk.Button(
            button_frame,
            text="Simple Interest",
            width=18,
            font=("Segoe UI", 10, "bold"),
            bg="#2b6cb0",
            fg="white",
            activebackground="#1f4e87",
            command=self.show_simple_interest,
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            button_frame,
            text="Compound Interest",
            width=18,
            font=("Segoe UI", 10, "bold"),
            bg="#2f855a",
            fg="white",
            activebackground="#276749",
            command=self.show_compound_interest,
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            button_frame,
            text="Clear",
            width=12,
            font=("Segoe UI", 10, "bold"),
            bg="#e2e8f0",
            fg="#1a202c",
            command=self.clear_all,
        ).grid(row=0, column=2, padx=8)

        result_frame = tk.LabelFrame(
            self.root,
            text="Result",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            padx=12,
            pady=12,
        )
        result_frame.pack(padx=20, pady=8, fill="x")

        tk.Label(
            result_frame,
            textvariable=self.result_var,
            justify="left",
            anchor="w",
            bg="white",
            fg="#1a202c",
            font=("Consolas", 11),
        ).pack(fill="x")

        growth_frame = tk.LabelFrame(
            self.root,
            text="Yearly Growth",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            padx=10,
            pady=10,
        )
        growth_frame.pack(padx=20, pady=10, fill="both", expand=True)

        columns = ("year", "amount")
        self.growth_table = ttk.Treeview(growth_frame, columns=columns, show="headings", height=8)
        self.growth_table.heading("year", text="Year")
        self.growth_table.heading("amount", text="Amount")
        self.growth_table.column("year", width=100, anchor="center")
        self.growth_table.column("amount", width=220, anchor="center")
        self.growth_table.pack(fill="both", expand=True)

    def create_input_row(self, parent, label_text, variable, row):
        """Create one label-entry row."""
        label = tk.Label(
            parent,
            text=label_text,
            font=("Segoe UI", 11),
            bg="white",
            fg="#2d3748",
        )
        label.grid(row=row, column=0, sticky="w", padx=16, pady=12)

        entry = tk.Entry(
            parent,
            textvariable=variable,
            font=("Segoe UI", 11),
            width=25,
            relief="solid",
            bd=1,
        )
        entry.grid(row=row, column=1, padx=16, pady=12, sticky="ew")

        parent.grid_columnconfigure(1, weight=1)

    def read_values(self):
        """Validate and return numeric input values."""
        try:
            principal = float(self.principal_var.get().strip())
            rate = float(self.rate_var.get().strip())
            time = float(self.time_var.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values.")
            return None

        if principal < 0 or rate < 0 or time < 0:
            messagebox.showerror("Invalid Input", "Values cannot be negative.")
            return None

        return principal, rate, time

    def clear_growth_table(self):
        """Remove old rows from the growth table."""
        for item in self.growth_table.get_children():
            self.growth_table.delete(item)

    def show_simple_interest(self):
        """Calculate and display simple interest."""
        values = self.read_values()
        if values is None:
            return

        principal, rate, time = values
        interest = calculate_simple_interest(principal, rate, time)
        total_amount = principal + interest

        self.result_var.set(
            f"Calculation Type : Simple Interest\n"
            f"Interest Amount  : {interest:.2f}\n"
            f"Total Amount     : {total_amount:.2f}"
        )
        self.clear_growth_table()

    def show_compound_interest(self):
        """Calculate and display compound interest with yearly growth."""
        values = self.read_values()
        if values is None:
            return

        principal, rate, time = values
        interest = calculate_compound_interest(principal, rate, time)
        total_amount = principal + interest

        self.result_var.set(
            f"Calculation Type : Compound Interest\n"
            f"Interest Amount  : {interest:.2f}\n"
            f"Total Amount     : {total_amount:.2f}"
        )

        self.clear_growth_table()
        for year, amount in get_yearly_growth(principal, rate, time):
            self.growth_table.insert("", "end", values=(year, f"{amount:.2f}"))

    def clear_all(self):
        """Clear all input and output fields."""
        self.principal_var.set("")
        self.rate_var.set("")
        self.time_var.set("")
        self.result_var.set(
            "Enter values and choose Simple Interest or Compound Interest."
        )
        self.clear_growth_table()


def main():
    """Start the tkinter application."""
    root = tk.Tk()
    app = InterestCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
