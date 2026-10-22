"""One-command runner: generate synthetic dataset and build all outputs."""
from src.generate_data import generate_data, DATA_DIR
from src.run_analysis import run

if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    generate_data().to_csv(DATA_DIR / "synthetic_prospects.csv", index=False)
    print("Synthetic dataset generated.")
    run()
