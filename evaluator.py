#!/usr/bin/env python3
"""Recursive-descent evaluator: binary ops, parentheses, non-negative numbers only. No unary minus or implicit multiply."""

from __future__ import annotations

import os
import sys
from typing import Any


def tokenize(expression: str) -> list[tuple[str, Any]]:
    tokens: list[tuple[str, Any]] = []
    i, expr = 0, expression.strip()
    while i < len(expr):
        ch = expr[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit() or (ch == "." and i + 1 < len(expr) and expr[i + 1].isdigit()):
            buf, has_dot = "", False
            while i < len(expr) and (expr[i].isdigit() or (expr[i] == "." and not has_dot)):
                if expr[i] == ".":
                    has_dot = True
                buf += expr[i]
                i += 1
            tokens.append(("NUM", float(buf) if has_dot else int(buf)))
            continue
        if ch in "+-*/":
            tokens.append(("OP", ch))
            i += 1
            continue
        if ch == "(":
            tokens.append(("LPAREN", "("))
            i += 1
            continue
        if ch == ")":
            tokens.append(("RPAREN", ")"))
            i += 1
            continue
        raise ValueError(f"Unexpected character {ch!r} at {i}")
    tokens.append(("END", None))
    return tokens


def format_tokens(tokens: list[tuple[str, Any]]) -> str:
    parts = []
    for kind, val in tokens:
        if kind == "NUM":
            parts.append(f"[NUM:{int(val)}]" if isinstance(val, float) and val == int(val) else f"[NUM:{val}]")
        elif kind == "OP":
            parts.append(f"[OP:{val}]")
        elif kind == "LPAREN":
            parts.append("[LPAREN:(]")
        elif kind == "RPAREN":
            parts.append("[RPAREN:)]")
        elif kind == "END":
            parts.append("[END]")
    return " ".join(parts)


def parse_expression(tokens: list[tuple[str, Any]], pos: int) -> tuple[Any, int]:
    left, pos = parse_term(tokens, pos)
    while pos < len(tokens) and tokens[pos][0] == "OP" and tokens[pos][1] in "+-":
        op = tokens[pos][1]
        pos += 1
        right, pos = parse_term(tokens, pos)
        left = (op, left, right)
    return left, pos


def parse_term(tokens: list[tuple[str, Any]], pos: int) -> tuple[Any, int]:
    left, pos = parse_factor(tokens, pos)
    while pos < len(tokens) and tokens[pos][0] == "OP" and tokens[pos][1] in "*/":
        op = tokens[pos][1]
        pos += 1
        right, pos = parse_factor(tokens, pos)
        left = (op, left, right)
    return left, pos


def parse_factor(tokens: list[tuple[str, Any]], pos: int) -> tuple[Any, int]:
    if pos >= len(tokens):
        raise ValueError("Unexpected end of input")
    kind, val = tokens[pos]
    if kind == "NUM":
        return val, pos + 1
    if kind == "LPAREN":
        pos += 1
        tree, pos = parse_expression(tokens, pos)
        if pos >= len(tokens) or tokens[pos][0] != "RPAREN":
            raise ValueError("Missing ')'")
        return tree, pos + 1
    if kind == "OP" and val == "+":
        raise ValueError("Unary plus is not allowed")
    raise ValueError(f"Unexpected token: {tokens[pos]}")


def parse(tokens: list[tuple[str, Any]]) -> Any:
    tree, pos = parse_expression(tokens, 0)
    if pos < len(tokens) and tokens[pos][0] != "END":
        raise ValueError("Trailing input")
    return tree


def format_tree(tree: Any) -> str:
    if isinstance(tree, tuple):
        op, a, b = tree[0], tree[1], tree[2]
        return f"({op} {format_tree(a)} {format_tree(b)})"
    if isinstance(tree, float) and tree == int(tree):
        return str(int(tree))
    return str(tree)


def evaluate_tree(tree: Any) -> float | int:
    if isinstance(tree, tuple):
        op, L, R = tree[0], tree[1], tree[2]
        x, y = evaluate_tree(L), evaluate_tree(R)
        if op == "+":
            return x + y
        if op == "-":
            return x - y
        if op == "*":
            return x * y
        if op == "/":
            if y == 0:
                raise ValueError("Division by zero")
            return x / y
        raise ValueError(op)
    return tree


def _format_result_line(val: float) -> str:
    return str(int(val)) if val == int(val) else f"{val:.4f}"


def _one_line(line: str) -> dict[str, Any]:
    try:
        toks = tokenize(line)
        tree = parse(toks)
        num = float(evaluate_tree(tree))
        return {"input": line, "tree": format_tree(tree), "tokens": format_tokens(toks), "result": num}
    except Exception:
        return {"input": line, "tree": "ERROR", "tokens": "ERROR", "result": "ERROR"}


def _write_output(records: list[dict[str, Any]], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for i, r in enumerate(records):
            f.write(f"Input: {r['input']}\n")
            if r["result"] == "ERROR":
                f.write("Tree: ERROR\nTokens: ERROR\nResult: ERROR\n")
            else:
                f.write(f"Tree: {r['tree']}\nTokens: {r['tokens']}\nResult: {_format_result_line(r['result'])}\n")
            if i < len(records) - 1:
                f.write("\n")


def evaluate_file(input_path: str) -> list[dict]:
    """Read expressions from input_path; write output.txt in the same directory; return one dict per line."""
    input_path = os.path.abspath(input_path)
    if not os.path.isfile(input_path):
        raise FileNotFoundError(input_path)
    out = os.path.join(os.path.dirname(input_path), "output.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    records = [_one_line(ln) for ln in lines]
    _write_output(records, out)
    return records


def main() -> None:
    base = os.path.dirname(os.path.abspath(__file__))
    inp = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base, "sample_input.txt")
    if not os.path.isfile(inp):
        print(f"Missing: {inp}")
        return
    evaluate_file(inp)
    print("Done.")


if __name__ == "__main__":
    main()
