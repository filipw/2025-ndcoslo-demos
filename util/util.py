from collections import Counter
from itertools import product
import plotly.graph_objects as go
from qsharp import Result

def plot(
    results: list,
    title: str,
    hide_empty: bool = False,
    basis: str = "Z"
) -> None:
    first = results[0] if results else None
    if isinstance(first, (list, tuple)):
        n_qubits = len(first)
        
        if basis.upper() == "Z":
            bitstrings = [
                "".join("0" if r == Result.Zero else "1" for r in shot)
                for shot in results
            ]
        elif basis.upper() == "X":
            bitstrings = [
                "".join("+" if r == Result.Zero else "-" for r in shot)
                for shot in results
            ]
        else:
            raise ValueError(f"Unsupported basis: {basis}. Use 'Z' or 'X'.")
        
        counts = Counter(bitstrings)
        
        symbols = "01" if basis.upper() == "Z" else "+-"
        all_strs = ["".join(p) for p in product(symbols, repeat=n_qubits)]
        
        for bs in all_strs:
            counts.setdefault(bs, 0)
            
        if hide_empty:
            all_strs = [bs for bs in all_strs if counts[bs] > 0]
            
        display_outcomes = [f"|{bs}⟩" for bs in all_strs]
        freqs = [counts[bs] for bs in all_strs]
    else:
        if basis.upper() == "Z":
            labels = ["0" if r == Result.Zero else "1" for r in results]
            counts = Counter(labels)
            for key in ("0", "1"):
                counts.setdefault(key, 0)
                
            if hide_empty:
                keys = [k for k in ("0", "1") if counts[k] > 0]
                display_outcomes = [f"|{k}⟩" for k in keys]
                freqs = [counts[k] for k in keys]
            else:
                display_outcomes = ["|0⟩", "|1⟩"]
                freqs = [counts["0"], counts["1"]]
        elif basis.upper() == "X":
            labels = ["+" if r == Result.Zero else "-" for r in results]
            counts = Counter(labels)
            for key in ("+", "-"):
                counts.setdefault(key, 0)
                
            if hide_empty:
                keys = [k for k in ("+", "-") if counts[k] > 0]
                display_outcomes = [f"|{k}⟩" for k in keys]
                freqs = [counts[k] for k in keys]
            else:
                display_outcomes = ["|+⟩", "|-⟩"]
                freqs = [counts["+"], counts["-"]]
        else:
            raise ValueError(f"Unsupported basis: {basis}. Use 'Z' or 'X'.")

    fig = go.Figure(
        data=go.Bar(
            x=display_outcomes,
            y=freqs,
            text=freqs
        ),
        layout=go.Layout(
            title=title,
            xaxis=dict(
                tickfont=dict(
                    size=16
                )
            )
        )
    )
    fig.show()