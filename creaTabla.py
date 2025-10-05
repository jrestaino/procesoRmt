import os
import ast
import re

BASE_DIR = "."  # directorio base donde están las carpetas 0, 1, 2, ...
OUTPUT_FILE = "tabla_resultados.tex"

def leer_entero(path):
    """Lee un entero desde un archivo de texto."""
    try:
        with open(path, "r") as f:
            return int(f.readline().strip())
    except Exception:
        return "-"

def leer_lista_y_len(path):
    """Lee una lista tipo [1,2,3] y devuelve su longitud."""
    try:
        with open(path, "r") as f:
            contenido = f.read().strip()
            lista = ast.literal_eval(contenido)
            return len(lista)
    except Exception:
        return "-"

def leer_entero_resumen(path):
    """Lee el primer número entero antes de ':' en resumenClases.txt."""
    try:
        with open(path, "r") as f:
            line = f.readline().strip()
            match = re.match(r"(\d+)", line)
            return int(match.group(1)) if match else "-"
    except FileNotFoundError:
        return "-"

def leer_float_top10(path):
    """Lee el primer float del archivo top10Clases.txt."""
    try:
        with open(path, "r") as f:
            line = f.readline().strip()
            return float(line) if re.match(r"^[0-9.]+$", line) else "-"
    except FileNotFoundError:
        return "-"

def main():
    filas = []

    for d in sorted(os.listdir(BASE_DIR), key=lambda x: int(x) if x.isdigit() else float('inf')):
        if not d.isdigit():
            continue

        dir_path = os.path.join(BASE_DIR, d)

        cantidad_asbr = leer_entero(os.path.join(dir_path, "cantidadAsbr.txt"))
        ixp_len = leer_lista_y_len(os.path.join(dir_path, "asbrTotalesIxp.txt"))
        carriers_len = leer_lista_y_len(os.path.join(dir_path, "asbrTotalesCarriers.txt"))
        default_len = leer_lista_y_len(os.path.join(dir_path, "asbrTotalesDefault.txt"))
        resumen = leer_entero_resumen(os.path.join(dir_path, "resumenClases.txt"))
        top10 = leer_float_top10(os.path.join(dir_path, "top10Clases.txt"))

        filas.append((d, resumen, top10, cantidad_asbr, ixp_len, carriers_len, default_len))

    # --- Crear tabla LaTeX ---
    with open(OUTPUT_FILE, "w") as f:
        f.write("\\begin{longtable}{c c c c c c c}\n")
        f.write("\\caption{Resultados de las pruebas} \\\\\n")
        f.write("\\hline\n")
        f.write("Prueba & Clases & Top10 & CantidadASBR & IxpLen & CarriersLen & DefaultLen \\\\\n")
        f.write("\\hline\n")
        f.write("\\endfirsthead\n")

        f.write("\\hline\nPrueba & Clases & Top10 & CantidadASBR & IxpLen & CarriersLen & DefaultLen \\\\\n\\hline\n")
        f.write("\\endhead\n")

        f.write("\\hline\n\\multicolumn{7}{r}{\\textit{Continúa en la siguiente página}} \\\\\n\\hline\n")
        f.write("\\endfoot\n")

        f.write("\\hline\n\\endlastfoot\n")

        for fila in filas:
            f.write(" & ".join(map(str, fila)) + " \\\\\n")

        f.write("\\end{longtable}\n")

    print(f"✅ Tabla completa generada en {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
