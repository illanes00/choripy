def run(src, dst):
    import pandas as pd
    df = pd.read_csv(src)
    # ... limpieza ...
    df.to_parquet(dst)
