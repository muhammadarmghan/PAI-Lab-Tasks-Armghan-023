# Task 9 Report

## Chosen task
Word frequency analysis.

## Problem statement
Given a body of text, count the frequency of words and show the most frequent ones.

## Tools and libraries
- Python
- Flask
- `re` for tokenization
- `collections.Counter` for frequency counting

## System overview
The app has a browser UI, a `/health` route for checking the server, and a `/api/analyze` endpoint for JSON output. The frontend can send pasted text or upload a `.txt` file.

## Dataset / input
- Primary input: `sample_input.txt`
- The web app also accepts pasted text in the browser form

## How to run
1. Install dependencies from `requirements.txt`.
2. Run `python main.py`.
3. Open the local Flask server in a browser.

## Result
The app displays the top N words in the input text, supports file upload, and works immediately with the bundled sample text.