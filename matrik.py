import tkinter as tk
from tkinter import messagebox, simpledialog

# ==== FUNGSI MATEMATIKA ====

def kali_matriks(M1, M2):
    n = len(M1)
    m = len(M2[0])
    p = len(M2)
    hasil = []
    for i in range(n):
        baris = []
        for j in range(m):
            total = 0
            for k in range(p):
                total += M1[i][k] * M2[k][j]
            baris.append(total)
        hasil.append(baris)
    return hasil

def determinant_3x3(M):
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    return (a * (e * i - f * h)
            - b * (d * i - f * g)
            + c * (d * h - e * g))

def cofactor(M, row, col):
    minor = []
    for i in range(3):
        if i == row:
            continue
        baris = []
        for j in range(3):
            if j == col:
                continue
            baris.append(M[i][j])
        minor.append(baris)
    return minor[0][0] * minor[1][1] - minor[0][1] * minor[1][0]

def inverse_3x3(M):
    det = determinant_3x3(M)
    if det == 0:
        return None
    cofaktor_matrix = []
    for i in range(3):
        baris = []
        for j in range(3):
            c = ((-1) ** (i + j)) * cofactor(M, i, j)
            baris.append(c)
        cofaktor_matrix.append(baris)
    adjoint = list(zip(*cofaktor_matrix))
    inv = []
    for i in range(3):
        baris = []
        for j in range(3):
            baris.append(adjoint[i][j] / det)
        inv.append(baris)
    return inv

def solve_linear_3x3(A, B, jenis):
    inv_A = inverse_3x3(A)
    if inv_A is None:
        return None
    if jenis == 'APB':
        hasil = kali_matriks(inv_A, B)
    elif jenis == 'PAB':
        hasil = kali_matriks(B, inv_A)
    else:
        return None
    return hasil


# ==== FUNGSI BANTU GUI ====

def input_matrix(rows=3, cols=3, nama="A"):
    """Popup untuk input elemen matriks"""
    M = []
    for i in range(rows):
        while True:
            row_str = simpledialog.askstring("Input",
                f"Masukkan baris ke-{i+1} matriks {nama} (pisahkan dengan spasi):")
            if row_str is None:
                return None
            parts = row_str.strip().split()
            if len(parts) != cols:
                messagebox.showerror("Error", f"Baris harus punya {cols} elemen.")
                continue
            try:
                row = [float(x) for x in parts]
                M.append(row)
                break
            except ValueError:
                messagebox.showerror("Error", "Input harus berupa angka.")
    return M

def show_matrix(M):
    return "\n".join(" ".join(f"{x:.2f}" for x in row) for row in M)


# ==== OPERASI GUI ====

def do_multiply():
    try:
        n1 = int(simpledialog.askstring("Input", "Masukkan jumlah baris matriks A:"))
        m1 = int(simpledialog.askstring("Input", "Masukkan jumlah kolom matriks A:"))
        n2 = int(simpledialog.askstring("Input", "Masukkan jumlah baris matriks B:"))
        m2 = int(simpledialog.askstring("Input", "Masukkan jumlah kolom matriks B:"))
    except (TypeError, ValueError):
        messagebox.showerror("Error", "Masukkan angka yang valid.")
        return

    if m1 != n2:
        messagebox.showerror("Error", "Kolom A harus sama dengan baris B.")
        return

    A = input_matrix(n1, m1, "A")
    if not A: return
    B = input_matrix(n2, m2, "B")
    if not B: return

    hasil = kali_matriks(A, B)
    messagebox.showinfo("Hasil Perkalian", show_matrix(hasil))


def do_determinant():
    M = input_matrix(3, 3, "A")
    if M:
        det = determinant_3x3(M)
        messagebox.showinfo("Hasil Determinan", f"Determinan A = {det:.2f}")


def do_inverse():
    M = input_matrix(3, 3, "A")
    if M:
        inv = inverse_3x3(M)
        if inv is None:
            messagebox.showerror("Hasil", "Matriks tidak memiliki invers (det = 0)")
        else:
            messagebox.showinfo("Hasil Invers", show_matrix(inv))


def do_linear_solver():
    M = input_matrix(3, 3, "A")
    if not M: return

    jenis_pilihan = simpledialog.askstring(
        "Jenis Persamaan",
        "Pilih jenis:\n1 = A·P = B\n2 = P·A = B"
    )

    if jenis_pilihan == "1":
        jenis = "APB"
        B = input_matrix(3, 1, "B")
        rumus = "P = A⁻¹ · B"
    elif jenis_pilihan == "2":
        jenis = "PAB"
        B = input_matrix(1, 3, "B")
        rumus = "P = B · A⁻¹"
    else:
        messagebox.showerror("Error", "Pilihan tidak valid.")
        return

    hasil = solve_linear_3x3(M, B, jenis)
    if hasil is None:
        messagebox.showerror("Hasil", "Matriks A tidak invertible (det = 0).")
    else:
        messagebox.showinfo("Hasil", f"{rumus}\n\n{show_matrix(hasil)}")


# ==== GUI UTAMA ====

root = tk.Tk()
root.geometry("600x500")
root.title("Kalkulator Operasi Matriks")

title_label = tk.Label(root, text="Kalkulator Operasi Matriks", font=('Arial', 20, 'bold'))
title_label.pack(pady=20)

btn_mul = tk.Button(root, text="Perkalian Matriks", font=('Arial', 14), width=25, command=do_multiply)
btn_mul.pack(pady=10)

btn_det = tk.Button(root, text="Determinan 3x3", font=('Arial', 14), width=25, command=do_determinant)
btn_det.pack(pady=10)

btn_inv = tk.Button(root, text="Invers 3x3", font=('Arial', 14), width=25, command=do_inverse)
btn_inv.pack(pady=10)

btn_lin = tk.Button(root, text="Penyelesaian Linear", font=('Arial', 14), width=25, border=2, command=do_linear_solver)
btn_lin.pack(pady=10)

exit_btn = tk.Button(root, text="Keluar", font=('Arial', 14), width=20, bg="red", fg="white", command=root.quit)
exit_btn.pack(pady=30)

root.mainloop()
