# Research Agent

A transparent, local research workflow: it plans a search, uses a local text-search tool, ranks matches and returns evidence with file citations. It is **not an LLM**, does not browse the web, and cannot autonomously take actions. A useful starter for exploring agent/tool orchestration without keys or costs.

Requires Python 3.10+. From this folder:

```sh
python agent.py "How do agents use tools?"
python agent.py "What helps automation?" --docs knowledge
python -m unittest discover -s tests -v
```

Put UTF-8 `.md` or `.txt` files in a folder and pass `--docs PATH`. Only top-level files are read; max 1 MB per file. Matches are lexical, so paraphrases may be missed. Check the cited evidence before relying on it. The sample files are illustrative.
