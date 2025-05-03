from collections import Counter
from itertools import product
import plotly.graph_objects as go
from qsharp import Result

def plot(
    results: list,
    title: str
) -> None:
    first = results[0] if results else None
    if isinstance(first, (list, tuple)):
        n_qubits = len(first)
        bitstrings = [
            "".join("0" if r == Result.Zero else "1" for r in shot)
            for shot in results
        ]
        counts = Counter(bitstrings)
        all_strs = ["".join(p) for p in product("01", repeat=n_qubits)]
        for bs in all_strs:
            counts.setdefault(bs, 0)
        outcomes = all_strs
    else:
        labels = ["Zero" if r == Result.Zero else "One" for r in results]
        counts = Counter(labels)
        for key in ("Zero", "One"):
            counts.setdefault(key, 0)
        outcomes = ["Zero", "One"]

    freqs = [counts[o] for o in outcomes]

    fig = go.Figure(
        data=go.Bar(
            x=outcomes,
            y=freqs,
            text=freqs,
        ),
        layout=go.Layout(
            title=title,
        )
    )
    fig.show()
