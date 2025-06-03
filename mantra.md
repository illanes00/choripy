🌀 Mantra de ChoriPy 🌀

1. **KISS** – “Keep It Simple, Santiago”  
   Lo más simple suele ser lo más robusto. Evita el over-engineering.

2. **“Un paso = un output”**  
   Cada etapa del ETL produce un único artefacto cacheable (.stamp). Repetible y predecible.

3. **Config jerárquica, no if-else dispersos**  
   Hydra + .env hacen tu código limpio: todo viene de YAML y vars, no hard-code.

4. **Python-only, sin drama npm/docker-overload**  
   Sass via `libsass`, Celery sobre Redis local, Postgres nativo: pip install y listo, sin Node ni Docker.

5. **Monitorea o muere**  
   Expon `/metrics` + `/monitor` y usa Flower (opcional). Si no ves tus tasks, idk qué haces.

6. **YAGNI • DRY • Test-First**  
   No implementes lo que no usas, no repitas, y escribe tests antes de codear.

7. **Async si y sólo si**  
   Usa async/await pa’ I/O heavy; por lo demás, síncrono y legible.

8. **Documenta con Quarto**  
   QMD = código + docs + referencias bibliográficas. Mantén tu paper al día sin copiar/pegar.

9. **CLI es alma de proyecto**  
   Un solo `run.py` con Typer + Rich: init, up, serve, report… todo desde un entry-point.

10. **Legibilidad > Cleverness**  
   Nada de one-liners obscuros. Si tu colega-no-sabe-python late dice “wtf?”, refact.

✨ Afaict, si sigues esto, ChoriPy será un stack zen-ready: fluido, reproducible y con sabor chileno. 🚀```
