import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc
from datetime import date, datetime
from decimal import Decimal

def center_window(window, width=800, height=600):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def connect_db():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=GTD\\SQLEXPRESS;"
        "DATABASE=EvidentaConsulatiilor;"
        "Trusted_Connection=yes;"
    )

def format_row(row):
    return [
        value.strftime("%Y-%m-%d %H:%M:%S") if isinstance(value, datetime) else
        value.strftime("%Y-%m-%d") if isinstance(value, date) else
        f"{value:.2f}" if isinstance(value, Decimal) else
        value.strip() if isinstance(value, str) else
        "" if value is None else str(value)
        for value in row
    ]

def execute_query(query, params=None):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        for widget in root.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(root, columns=columns, show="headings")
        tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center", width=200)

        for row in rows:
            tree.insert("", "end", values=format_row(row))

        ttk.Button(root, text="Inapoi", command=lambda: open_predefined_queries()).pack(pady=10)
        conn.close()
    except Exception as e:
        messagebox.showerror("Eroare", f"A aparut o problema: {e}")

def add_entry(table, values, columns):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Verificam coloanele IDENTITY si le excludem din inserare daca sunt goale
        identity_columns = []

        query_identity = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' AND COLUMNPROPERTY(object_id(TABLE_NAME), COLUMN_NAME, 'IsIdentity') = 1"
        cursor.execute(query_identity)
        identity_columns = [row[0] for row in cursor.fetchall()]

        final_columns = []
        final_values = []

        for col, val in zip(columns, values):
            if col in identity_columns and not val.strip():
                # Daca coloana este IDENTITY si valoarea este goala, o excludem
                continue
            final_columns.append(col)
            final_values.append(val)

        placeholders = ', '.join(['?'] * len(final_values))
        column_names = ', '.join(final_columns)
        query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
        cursor.execute(query, final_values)

        conn.commit()
        conn.close()
        messagebox.showinfo("Succes", "Intrarea a fost adaugata cu succes.")
    except Exception as e:
        messagebox.showerror("Eroare", f"Nu s-a putut adauga intrarea: {e}")

def delete_entry(table, condition):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = f"DELETE FROM {table} WHERE {condition}"
        cursor.execute(query)
        conn.commit()
        conn.close()
        messagebox.showinfo("Succes", "Intrarea a fost stearsa cu succes.")
    except Exception as e:
        messagebox.showerror("Eroare", f"Nu s-a putut sterge intrarea: {e}")

def delete_selected_entry(tree, table, primary_key):
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item, 'values')
        condition = f"{primary_key} = '{values[0]}'"
        delete_entry(table, condition)
        open_table(table)
    else:
        messagebox.showwarning("Atentie", "Selectati o intrare pentru a sterge.")

def update_entry(table, updates, condition):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = f"UPDATE {table} SET {updates} WHERE {condition}"
        cursor.execute(query)
        conn.commit()
        conn.close()
        messagebox.showinfo("Succes", "Intrarea a fost actualizata cu succes.")
    except Exception as e:
        messagebox.showerror("Eroare", f"Nu s-a putut actualiza intrarea: {e}")

def open_table(table):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = f"SELECT * FROM {table}"
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        for widget in root.winfo_children():
            widget.destroy()

        # Calculam latimea totala a ferestrei in functie de numarul si latimea coloanelor
        column_width = 200
        total_width = max(1024, len(columns) * column_width + 40)  # Adaugam un offset pentru margini
        total_height = max(768, len(rows) * 25 + 200)  # Ajustam inaltimea pentru a include datele si butoanele
        center_window(root, width=total_width, height=total_height)

        tree = ttk.Treeview(root, columns=columns, show="headings")
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        for col in columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center", width=column_width)

        for row in rows:
            tree.insert("", "end", values=format_row(row))

        # Buttons for add, delete, update
        ttk.Button(root, text="Adauga", command=lambda: open_add_entry(table, columns), style="TButton").pack(pady=10)
        ttk.Button(root, text="Sterge", command=lambda: delete_selected_entry(tree, table, columns[0]), style="TButton").pack(pady=10)
        ttk.Button(root, text="Actualizeaza", command=lambda: open_update_entry(tree, table, columns), style="TButton").pack(pady=10)
        ttk.Button(root, text="Inapoi", command=lambda: initialize_main_window(root), style="TButton").pack(pady=10)

        conn.close()
    except Exception as e:
        messagebox.showerror("Eroare", f"A aparut o problema: {e}")

def open_add_entry(table, columns):
    for widget in root.winfo_children():
        widget.destroy()

    entries = []
    ttk.Label(root, text=f"Adaugare in tabelul {table}", font=("Helvetica", 16)).pack(pady=10)

    for col in columns:
        ttk.Label(root, text=col).pack()
        entry = tk.Entry(root)
        entry.pack(pady=5)
        entries.append(entry)

    def submit_add():
        values = [entry.get() for entry in entries]
        add_entry(table, values, columns)
        open_table(table)

    ttk.Button(root, text="Adauga", command=submit_add).pack(pady=10)
    ttk.Button(root, text="Inapoi", command=lambda: open_table(table)).pack(pady=10)

def open_update_entry(tree, table, columns):
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item, 'values')
        for widget in root.winfo_children():
            widget.destroy()

        entries = []
        ttk.Label(root, text=f"Actualizare in tabelul {table}", font=("Helvetica", 16)).pack(pady=10)

        for i, col in enumerate(columns):
            ttk.Label(root, text=col, style="TLabel").pack()
            entry = tk.Entry(root)
            if "ID" not in col:  # Skip ID fields for updates
                entry.insert(0, values[i])
            else:
                entry.insert(0, values[i])
                entry.configure(state="disabled")  # Disable ID fields
            entry.pack(pady=5)
            entries.append((col, entry))

        def submit_update():
            new_values = [f"{col} = '{entry.get()}'" for col, entry in entries if not entry.cget("state") == "disabled"]
            updates = ", ".join(new_values)
            condition = f"{columns[0]} = '{values[0]}'"
            update_entry(table, updates, condition)
            open_table(table)

        ttk.Button(root, text="Actualizeaza", command=submit_update, style="TButton").pack(pady=10)
        ttk.Button(root, text="Inapoi", command=lambda: open_table(table), style="TButton").pack(pady=10)
    else:
        messagebox.showwarning("Atentie", "Selectati o intrare pentru a actualiza.")

def open_predefined_queries():
    for widget in root.winfo_children():
        widget.destroy()

    ttk.Label(root, text="Interogari Predefinite", font=("Helvetica", 16)).pack(pady=10)

    def show_simple_queries():
        simple_queries = [
            ("Consultatii si Medici cu Specialitati",
             "SELECT c.ConsultatieID, m.Nume AS Medic, sp.Nume AS Specialitate "
             "FROM Consultatii c "
             "INNER JOIN Medici m ON c.MedicID = m.MedicID "
             "INNER JOIN Specialitati sp ON m.SpecialitateID = sp.SpecialitateID"),
            ("Pacienti si Servicii Medicale",
             "SELECT p.Nume AS Pacient, c.DataConsultatie, s.Nume AS Serviciu "
             "FROM Pacienti p INNER JOIN Consultatii c ON p.PacientID = c.PacientID "
             "INNER JOIN ConsultatieServicii cs ON c.ConsultatieID = cs.ConsultatieID "
             "INNER JOIN ServiciiMedicale s ON cs.ServiciuID = s.ServiciuID"),
            ("Medici cu Specialitati si Pacienti",
             "SELECT m.Nume AS Medic, sp.Nume AS Specialitate, p.Nume AS Pacient "
             "FROM Medici m INNER JOIN Specialitati sp ON m.SpecialitateID = sp.SpecialitateID "
             "INNER JOIN Consultatii c ON m.MedicID = c.MedicID "
             "INNER JOIN Pacienti p ON c.PacientID = p.PacientID"),
            ("Consultatii recente si costuri",
             "SELECT c.ConsultatieID, c.DataConsultatie, c.Cost, p.Nume AS Pacient "
             "FROM Consultatii c "
             "INNER JOIN Pacienti p ON c.PacientID = p.PacientID "
             "WHERE c.DataConsultatie > DATEADD(DAY, -30, GETDATE())"),
            ("Servicii utilizate de Pacienti",
             "SELECT s.Nume AS Serviciu, COUNT(DISTINCT cs.ConsultatieID) AS NrConsultatii "
             "FROM ServiciiMedicale s "
             "INNER JOIN ConsultatieServicii cs ON s.ServiciuID = cs.ServiciuID "
             "GROUP BY s.Nume"),
            ("Pacienti si numar consultatii",
             "SELECT p.Nume AS Pacient, COUNT(c.ConsultatieID) AS NrConsultatii "
             "FROM Pacienti p "
             "LEFT JOIN Consultatii c ON p.PacientID = c.PacientID "
             "GROUP BY p.Nume"),
        ]
        show_queries("Interogari Simple", simple_queries)

    def show_complex_queries():
        complex_queries = [
            ("Pacienti cu mai mult de X consultatii",
             "SELECT p.Nume "
             "FROM Pacienti p "
             "WHERE ("
             "      SELECT COUNT(*) "
             "      FROM Consultatii c "
             "      WHERE c.PacientID = p.PacientID) > ?"),
            ("Medici cu consultatii peste media costurilor",
             "SELECT m.Nume "
             "FROM Medici m "
             "WHERE EXISTS ("
             "      SELECT 1 "
             "      FROM Consultatii c "
             "      WHERE c.MedicID = m.MedicID AND c.Cost > ("
             "              SELECT AVG(Cost) FROM Consultatii))"),
            ("Consultatii si servicii sub media costurilor",
             "SELECT c.ConsultatieID, s.Nume AS Serviciu "
             "FROM Consultatii c "
             "INNER JOIN ConsultatieServicii cs ON c.ConsultatieID = cs.ConsultatieID "
             "INNER JOIN ServiciiMedicale s ON cs.ServiciuID = s.ServiciuID "
             "WHERE c.Cost < ("
             "      SELECT AVG(Cost) "
             "      FROM Consultatii) "
             "AND "
             "      s.Pret < ("
             "      SELECT AVG(Pret) "
             "      FROM ServiciiMedicale)"),
            ("Pacienti care folosesc mai mult de 3 servicii unice",
             "SELECT p.Nume "
             "FROM Pacienti p "
             "WHERE ("
             "      SELECT COUNT(DISTINCT cs.ServiciuID) "
             "      FROM Consultatii c "
             "      INNER JOIN ConsultatieServicii cs ON c.ConsultatieID = cs.ConsultatieID "
             "      WHERE c.PacientID = p.PacientID) > 3"),
        ]
        show_queries("Interogari Complexe", complex_queries)

    ttk.Button(root, text="Interogari Simple", command=show_simple_queries, style="TButton").pack(pady=10)
    ttk.Button(root, text="Interogari Complexe", command=show_complex_queries, style="TButton").pack(pady=10)
    ttk.Button(root, text="Inapoi", command=lambda: initialize_main_window(root), style="TButton").pack(pady=10)

def show_queries(title, queries):
    for widget in root.winfo_children():
        widget.destroy()

    ttk.Label(root, text=title, font=("Helvetica", 16)).pack(pady=10)

    for desc, query in queries:
        def run_query(q=query):
            if "?" in q:
                get_param_and_execute(q)
            else:
                execute_query(q)

        ttk.Button(root, text=desc, command=run_query, style="TButton").pack(pady=5)

    ttk.Button(root, text="Inapoi", command=open_predefined_queries, style="TButton").pack(pady=20)

def get_param_and_execute(query):
    for widget in root.winfo_children():
        widget.destroy()

    ttk.Label(root, text="Introduceti valoarea pentru X:", font=("Helvetica", 12)).pack(pady=10)
    param_entry = tk.Entry(root)
    param_entry.pack(pady=10)

    def execute_with_param():
        try:
            x = int(param_entry.get())
            execute_query(query, (x,))
        except ValueError:
            messagebox.showerror("Eroare", "Introduceti un numar valid pentru X!")

    ttk.Button(root, text="Executa", command=execute_with_param, style="TButton").pack(pady=10)
    ttk.Button(root, text="Inapoi", command=open_predefined_queries, style="TButton").pack(pady=10)

def initialize_main_window(main_window):
    for widget in main_window.winfo_children():
        widget.destroy()

    ttk.Label(main_window, text="Meniu Principal", font=("Helvetica", 16)).pack(pady=10)
    tables = ["ConsultatieServicii", "Consultatii", "Medici", "Pacienti", "ServiciiMedicale", "Specialitati"]

    for table in tables:
        ttk.Button(main_window, text=table, command=lambda t=table: open_table(t), style="TButton").pack(pady=5)

    ttk.Button(main_window, text="Interogari Predefinite", command=open_predefined_queries, style="TButton").pack(pady=20)
    ttk.Button(main_window, text="Exit", command=main_window.destroy, style="TButton").pack(pady=10)

def login_window():
    for widget in root.winfo_children():
        widget.destroy()

    ttk.Label(root, text="Autentificare", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

    ttk.Label(root, text="Utilizator:", style="TLabel").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    username_entry = tk.Entry(root)
    username_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(root, text="Parola:", style="TLabel").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    password_entry = tk.Entry(root, show="*")
    password_entry.grid(row=2, column=1, padx=10, pady=5)

    def validate_login(event=None):
        username = username_entry.get()
        password = password_entry.get()
        try:
            conn = connect_db()
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM Users WHERE Username = ? AND Password = ?"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            conn.close()

            if result[0] == 1:
                initialize_main_window(root)
            else:
                messagebox.showerror("Eroare", "Nume de utilizator sau parola incorecta!")
        except Exception as e:
            messagebox.showerror("Eroare", f"A aparut o problema: {e}")

    ttk.Button(root, text="Login", command=validate_login, style="TButton").grid(row=3, column=0, columnspan=2, pady=10)
    ttk.Button(root, text="Exit", command=root.destroy, style="TButton").grid(row=4, column=0, columnspan=2, pady=10)

    root.bind("<Return>", validate_login)

root = tk.Tk()
root.title("Aplicatie Evidenta Consultatiilor")
center_window(root, width=1024, height=768)

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 12), padding=5)

login_window()

root.mainloop()