import requests
import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import os


def analyze_corpus(corpus_name, source, source_type="url"):
    if source_type == "url":
        text = fetch_corpus_from_url(source)
    elif source_type == "file":
        text = fetch_corpus_from_file(source)
    elif source_type == "text":
        text = source
    else:
        raise ValueError("source_type must be 'url', 'file', or 'text'")

    tokens = tokenize(text)
    token_count, type_count, word_freq = compute_counts(tokens)

    plot_zipf(word_freq, corpus_name)

    top_7 = get_top_n_words(word_freq, 7)
    top_7_coverage = compute_top_n_coverage(word_freq, 7, token_count)
    hapax_stats = compute_hapax_statistics(word_freq, token_count, type_count)

    print_results(
        corpus_name, token_count, type_count, top_7, top_7_coverage, hapax_stats
    )

    return {
        "corpus_name": corpus_name,
        "token_count": token_count,
        "type_count": type_count,
        "top_7": top_7,
        "top_7_coverage": top_7_coverage,
        "hapax_stats": hapax_stats,
        "word_freq": word_freq,
    }


def fetch_corpus_from_url(url):
    try:
        response = requests.get(url, timeout=30)
        response.encoding = response.apparent_encoding
        return response.text
    except Exception as e:
        print(f"Error fetching from URL: {e}")
        raise


def fetch_corpus_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def tokenize(text):
    text = text.lower()
    words = re.findall(r"\b[a-zăâîșțîâ]+\b", text)
    return words


def compute_counts(tokens):
    word_freq = Counter(tokens)
    token_count = len(tokens)
    type_count = len(word_freq)
    return token_count, type_count, word_freq


def plot_zipf(word_freq, corpus_name):
    frequencies = sorted(word_freq.values(), reverse=True)[:200]

    if not frequencies:
        print("No data to plot")
        return

    ranks = np.arange(1, len(frequencies) + 1)

    plt.figure(figsize=(10, 6))
    plt.plot(ranks, frequencies, "b-", linewidth=2)
    plt.xlabel("Rank")
    plt.ylabel("Frequency")

    plt.xlim(0, 200)
    plt.xticks(range(0, 201, 25))

    plt.title(f"Zipf's Law - {corpus_name}")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_dir = "."
    os.makedirs(output_dir, exist_ok=True)

    filename = f"zipf_{corpus_name.lower().replace(' ', '_')}.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=100, bbox_inches="tight")
    print(f"Graph saved to: {filepath}")
    plt.close()


def get_top_n_words(word_freq, n):
    return word_freq.most_common(n)


def compute_top_n_coverage(word_freq, n, token_count):
    top_n = word_freq.most_common(n)
    top_n_tokens = sum(count for _, count in top_n)
    return (top_n_tokens / token_count) * 100


def compute_hapax_statistics(word_freq, token_count, type_count):
    hapax_legomena = [word for word, count in word_freq.items() if count == 1]
    hapax_count = len(hapax_legomena)

    hapax_as_tokens_percent = (hapax_count / token_count) * 100
    hapax_as_types_percent = (hapax_count / type_count) * 100

    return {
        "count": hapax_count,
        "tokens_percent": hapax_as_tokens_percent,
        "types_percent": hapax_as_types_percent,
    }


def print_results(
    corpus_name, token_count, type_count, top_7, top_7_coverage, hapax_stats
):
    print(f"\n{corpus_name}:")
    print(f"{token_count} tokens, {type_count} types\n")

    print("Top 7 most freq words (in order):")
    words_str = ", ".join([f'("{word}":{count})' for word, count in top_7])
    print(f"{corpus_name}: {words_str}\n")

    print("Percent of the tokens in the corpus covered by the most freq. 7 words:")
    print(f"{corpus_name}: {top_7_coverage:.2f}%\n")

    print("Percent of the words in the corpus covered by words that appear once:")
    print("- as types")
    print("- as tokens\n")
    print(f"{corpus_name}:")
    print(f"{hapax_stats['count']},")
    print(
        f"{hapax_stats['tokens_percent']:.2f}% of the tokens, "
        f"{hapax_stats['types_percent']:.2f}% of the types"
    )


CORPUS_URLS = {
    "Hamlet": "https://www.gutenberg.org/files/1524/1524-0.txt",
    "Don_Quixote": "https://www.gutenberg.org/files/996/996-0.txt",
}

if __name__ == "__main__":
    for name, url in CORPUS_URLS.items():
        try:
            result = analyze_corpus(name, url, "url")
            print(f"\nCompleted analysis for {name}")
        except Exception as e:
            print(f"Failed to analyze {name}: {e}")
