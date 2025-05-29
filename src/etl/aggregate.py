def run(src, dst):
    import pandas as pd
    df = pd.read_parquet(src)
    # ... agregación ...
    df.to_parquet(dst)
