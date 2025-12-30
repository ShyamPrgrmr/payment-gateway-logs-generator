import pandas as pd

def load_csv(component):
    df = pd.read_csv(
        f"csv/{component}.csv",
        header=None,
        names=["component", "log", "level"]
    )
    return df
