#!/usr/bin/env python
"""
Imprime un árbol ASCII + contenido de archivos (respetando .gitignore)
y guarda todo en skeleton.txt en texto plano.
"""
import os
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parent.parent
output_file = root / "skeleton.txt"

def is_ignored(path: Path) -> bool:
    """Devuelve True si `git check-ignore` marca este path como ignorado."""
    try:
        return subprocess.run(
            ["git", "check-ignore", "-q", str(path)],
            cwd=root
        ).returncode == 0
    except Exception:
        return False

def write_tree(f, base: Path, prefix: str = ""):
    """Escribe el árbol de directorios en ASCII."""
    entries = [p for p in sorted(base.iterdir()) 
               if not (p.name.startswith('.') and p.name not in {'.env.example'})
               and not is_ignored(p)
               and ".git" not in p.relative_to(root).parts]
    for i, path in enumerate(entries):
        connector = "└── " if i == len(entries)-1 else "├── "
        f.write(f"{prefix}{connector}{path.name}\n")
        if path.is_dir():
            extension = "    " if i == len(entries)-1 else "│   "
            write_tree(f, path, prefix + extension)

def write_files(f, base: Path):
    """Recurre todos los archivos y escribe su contenido."""
    for file in sorted(base.rglob('*')):
        if not file.is_file():
            continue
        if is_ignored(file) or ".git" in file.relative_to(root).parts:
            continue
        try:
            content = file.read_text()
        except Exception:
            continue
        f.write("\n" + "="*80 + "\n")
        f.write(f"FILE: {file.relative_to(root)}\n")
        f.write("="*80 + "\n")
        f.write(content)

def main():
    with output_file.open("w", encoding="utf-8") as f:
        f.write("project\n")
        write_tree(f, root)
        write_files(f, root)
    print(f"Skeleton guardado en {output_file}")

if __name__ == "__main__":
    main()
