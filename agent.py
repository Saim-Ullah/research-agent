#!/usr/bin/env python3
"""A small, transparent retrieve-and-compose agent. No model or network required."""
import argparse
import re
from pathlib import Path
from collections import Counter

STOP = set('a an and are as at be by for from how in is it of on or that the this to what with'.split())
def terms(text):
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]

def search(query, docs, limit=3):
    q = set(terms(query))
    if not q: return []
    ranked = []
    for name, text in docs.items():
        counts = Counter(terms(text))
        score = sum(min(counts[w], 3) for w in q)
        if score: ranked.append((score, name, text))
    return sorted(ranked, key=lambda x: (-x[0], x[1]))[:limit]

def run(question, docs):
    """Plan -> search tool -> evidence selection -> compose with source labels."""
    found = search(question, docs)
    if not found:
        return 'No matching evidence found. Add a relevant .txt or .md file and try again.'
    lines = ['Plan: search the local knowledge base and cite matching evidence.', '', 'Evidence:']
    q = set(terms(question))
    for _, name, text in found:
        sentences = re.split(r'(?<=[.!?])\s+|\n+', text)
        relevant = [s.strip() for s in sentences if q.intersection(terms(s)) and s.strip()]
        excerpt = (relevant[0] if relevant else text.strip())[:300]
        lines.append(f'- [{name}] {excerpt}')
    lines += ['', 'Answer: Review the evidence above; these are retrieved excerpts, not an AI-generated conclusion.']
    return '\n'.join(lines)

def load(folder):
    result = {}
    for path in sorted(folder.iterdir()):
        if path.is_file() and path.suffix.lower() in ('.md', '.txt'):
            if path.stat().st_size > 1_000_000: raise ValueError(f'File too large: {path.name}')
            result[path.name] = path.read_text(encoding='utf-8')
    return result

def main():
    parser = argparse.ArgumentParser(description='Local evidence-first research agent')
    parser.add_argument('question'); parser.add_argument('--docs', type=Path, default=Path(__file__).parent / 'knowledge')
    args = parser.parse_args()
    try: print(run(args.question, load(args.docs)))
    except (OSError, UnicodeError, ValueError) as exc: parser.exit(2, f'Error: {exc}\n')
if __name__ == '__main__': main()
