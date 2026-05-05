"""
Flask-based NLP demo for Task 9.

The app provides an end-to-end word-frequency workflow:
- browser form for text input
- optional file upload
- bundled sample input fallback
- HTML results page
- JSON API endpoint for programmatic use
"""

from collections import Counter
import re
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename


app = Flask(__name__)
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SAMPLE_PATH = SCRIPT_DIR / 'sample_input.txt'
MAX_TOP_N = 50


def load_sample_text():
    try:
        return DEFAULT_SAMPLE_PATH.read_text(encoding='utf-8')
    except FileNotFoundError:
        return (
            'Natural language processing lets computers work with human language. '
            'This fallback sample is used when sample_input.txt is missing.'
        )


def word_frequency(text: str, top_n: int = 10) -> list[tuple[str, int]]:
    tokens = re.findall(r"\b[a-zA-Z']{2,}\b", text.lower())
    return Counter(tokens).most_common(top_n)


def parse_top_n(raw_value: Any) -> int:
    try:
        return max(1, min(MAX_TOP_N, int(raw_value)))
    except (TypeError, ValueError):
        return 10


def get_uploaded_text(uploaded_file: Any) -> str:
    if not uploaded_file or not uploaded_file.filename:
        return ''
    filename = secure_filename(uploaded_file.filename)
    if not filename:
        return ''
    try:
        return uploaded_file.read().decode('utf-8')
    except UnicodeDecodeError:
        uploaded_file.stream.seek(0)
        return uploaded_file.read().decode('latin-1', errors='ignore')


def build_analysis_payload(text_input: str, top_n: int) -> dict[str, Any]:
    tokens = re.findall(r"\b[a-zA-Z']{2,}\b", text_input.lower())
    result = word_frequency(text_input, top_n)
    return {
        'result': result,
        'top_n': top_n,
        'text_input': text_input,
        'text_length': len(text_input),
        'token_count': len(tokens),
        'unique_count': len(set(tokens)),
    }


@app.get('/health')
def health():
    return jsonify({'status': 'ok'})


@app.route('/', methods=['GET', 'POST'])
def index():
    sample_text = load_sample_text()
    text_input = sample_text
    top_n = 10

    if request.method == 'POST':
        submitted_text = request.form.get('text_input', '').strip()
        uploaded_text = get_uploaded_text(request.files.get('input_file'))
        text_input = submitted_text or uploaded_text or sample_text
        top_n = parse_top_n(request.form.get('top_n', '10'))

    payload = build_analysis_payload(text_input, top_n)
    return render_template(
        'index.html',
        sample_text=sample_text,
        **payload,
    )


@app.post('/api/analyze')
def api_analyze():
    text_input = request.form.get('text_input', '').strip()
    uploaded_text = get_uploaded_text(request.files.get('input_file'))
    sample_text = load_sample_text()
    top_n = parse_top_n(request.form.get('top_n', '10'))
    effective_text = text_input or uploaded_text or sample_text
    payload = build_analysis_payload(effective_text, top_n)
    return jsonify(payload)


if __name__ == '__main__':
    app.run(debug=True)
