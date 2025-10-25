# doc2beat

Convert technical documentation into easy-to-understand songs of different styles to help communicate content in a fun way.

## Installation

```bash
pip install -e .
```

## Configuration

1. Copy `example_creds.yaml` to `creds.yaml` and add your OpenRouter API key:
```yaml
openrouter_api_key: "your-api-key-here"
```

2. Configure the LLM model in `config.yaml` (defaults are provided):
```yaml
lyric_model: "openai/gpt-4"
```

## Usage

### Command Line Interface

Process a single document:
```bash
doc2beat --url "https://example.com/docs"
```

Process a single document with a specific song style:
```bash
doc2beat --url "https://example.com/docs" --style "upbeat pop"
```

Process multiple documents from a CSV file:
```bash
doc2beat --input input.csv
```

The input CSV should have columns:
- `document_url` (required): URL of the documentation
- `song_style` (optional): Specific song style to use

### Output

The tool generates an `output.csv` file with the following columns:
- `document_url`: The input documentation URL
- `song_style`: The generated or provided song style
- `song_lyrics`: The generated song lyrics

## Workflow

1. If song_style is not provided, the LLM generates a random song style prompt (up to 1000 characters)
2. The document content is retrieved from the URL
3. The LLM generates song lyrics based on the document content and song style (up to 5000 characters, but can be shorter based on content)
4. Results are saved to `output.csv`
