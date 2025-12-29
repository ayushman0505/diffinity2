def generate_summary(results):
    summary = []

    for r in results:
        if r["similarity"] < 0.85:
            summary.append(
                f"Significant change detected (similarity: {r['similarity']})"
            )

    if not summary:
        summary.append("No major changes detected.")

    return summary
