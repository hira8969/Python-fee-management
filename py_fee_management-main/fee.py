import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

class FeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fee Management System")
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title = tk.Label(self.root, text="Fee Management System", fg="white", bg="darkblue",
                         font=("Arial", 40, "bold"), bd=5, relief="ridge")
        title.pack(side="top", fill="x")

        # Main Form Frame
        self.mainFrame = tk.Frame(self.root, bg="lightblue", bd=4, relief="ridge")
        self.mainFrame.place(x=80, y=120, width=self.width / 3, height=self.height - 200)

        # Input fields
        tk.Label(self.mainFrame, text="Roll No:", bg="lightblue", font=("Arial", 15)).grid(row=0, column=0, padx=10, pady=30)
        self.rollEntry = tk.Entry(self.mainFrame, font=("Arial", 18), width=20)
        self.rollEntry.grid(row=0, column=1, padx=10, pady=30)

        tk.Label(self.mainFrame, text="Enter Fee:", bg="lightblue", font=("Arial", 15)).grid(row=1, column=0, padx=10, pady=30)
        self.feeEntry = tk.Entry(self.mainFrame, font=("Arial", 18), width=20)
        self.feeEntry.grid(row=1, column=1, padx=10, pady=30)

        tk.Button(self.mainFrame, text="Submit Fee", command=self.submitFee, bg="green", fg="white",
                  font=("Arial", 15, "bold")).grid(row=2, column=0, columnspan=2, pady=40)

        tk.Button(self.mainFrame, text="Show All Records", command=self.showAll,
                  bg="orange", font=("Arial", 15, "bold")).grid(row=3, column=0, columnspan=2, pady=10)

        # Table Frame
        self.tableFrame = tk.Frame(self.root, bg="lightgreen", bd=4, relief="ridge")
        self.tableFrame.place(x=self.width / 3 + 150, y=120, width=self.width / 2, height=self.height - 200)

        tk.Label(self.tableFrame, text="Fee Details", bg="lightgreen", font=("Arial", 25, "bold")).pack(side="top", fill="x")

        self.createTable()

    def connect_db(self):
        """Create MySQL connection"""
        return pymysql.connect(host="localhost", user="root", password="Hira2006@", database="REC2")

    def createTable(self):
        """Create TreeView Table"""
        frame = tk.Frame(self.tableFrame, bg="white")
        frame.place(x=10, y=60, width=self.width / 2 - 60, height=self.height - 300)

        x_scroll = tk.Scrollbar(frame, orient="horizontal")
        y_scroll = tk.Scrollbar(frame, orient="vertical")

        self.table = ttk.Treeview(frame, columns=("roll", "name", "total", "paid", "remaining"),
                                  xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)

        x_scroll.pack(side="bottom", fill="x")
        y_scroll.pack(side="right", fill="y")
        x_scroll.config(command=self.table.xview)
        y_scroll.config(command=self.table.yview)

        self.table.heading("roll", text="Roll No")
        self.table.heading("name", text="Name")
        self.table.heading("total", text="Total Fee")
        self.table.heading("paid", text="Paid Fee")
        self.table.heading("remaining", text="Remaining Fee")

        self.table["show"] = "headings"
        for col in ("roll", "name", "total", "paid", "remaining"):
            self.table.column(col, width=150, anchor="center")

        self.table.pack(fill="both", expand=True)

    def submitFee(self):
        """Submit fee and update record"""
        try:
            rn = self.rollEntry.get().strip()
            amt = self.feeEntry.get().strip()

            if rn == "" or amt == "":
                messagebox.showwarning("Input Error", "Please fill all fields!")
                return

            rn, amt = int(rn), int(amt)

            con = self.connect_db()
            cur = con.cursor()
            cur.execute("SELECT name, paid_fee, remaining FROM fee WHERE rollNo=%s", (rn,))
            row = cur.fetchone()

            if not row:
                messagebox.showerror("Error", "Roll number not found in database!")
                return

            name, paid, remaining = row
            new_paid = paid + amt
            new_remain = remaining - amt

            if new_remain < 0:
                messagebox.showerror("Error", "Fee entered exceeds remaining amount!")
                return

            cur.execute("UPDATE fee SET paid_fee=%s, remaining=%s WHERE rollNo=%s",
                        (new_paid, new_remain, rn))
            con.commit()

            messagebox.showinfo("Success", f"Fee updated successfully for {name}")
            self.showAll()

        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}")
        finally:
            try:
                cur.close()
                con.close()
            except:
                pass

    def showAll(self):
        """Fetch and display all records"""
        try:
            con = self.connect_db()
            cur = con.cursor()
            cur.execute("SELECT * FROM fee")
            data = cur.fetchall()

            self.table.delete(*self.table.get_children())
            for row in data:
                self.table.insert("", tk.END, values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}")
        finally:
            try:
                cur.close()
                con.close()
            except:
                pass


# Run App
root = tk.Tk()
app = FeeApp(root)
root.mainloop()
