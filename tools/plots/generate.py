import matplotlib.pyplot as plt
import pandas as pd

def main():
    df = pd.read_parquet("data/processed/features.parquet")
    plt.figure()
    plt.plot(df.incidents)
    plt.savefig("reports/figures/incidents.png")

if __name__ == "__main__":
    main()
