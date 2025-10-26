# doc2beat

Convert technical documentation into easy-to-understand songs of different styles to help communicate content in a fun way.

## Features

- 🎵 **Diverse Musical Styles**: Randomly selects from comprehensive genre lists
- 📚 **Content Extraction**: Intelligently extracts documentation content, filtering out navigation and website noise
- 🎓 **Educational Preservation**: Maintains technical accuracy, preserving procedures, commands, and instructional guidance
- 🔧 **Flexible Configuration**: Supports various documentation sources (API docs, tutorials, references)
- 🎨 **Optional Creative Mode**: Enable experimental and inventive style generation

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
lyric_model: "anthropic/claude-haiku-4.5"
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

Process a single document with a specific music genre:
```bash
doc2beat --url "https://example.com/docs" --genre "jazz"
doc2beat --url "https://example.com/docs" --genre "electronic"
doc2beat --url "https://example.com/docs" --genre "folk"
```

Process multiple documents from a CSV file:
```bash
doc2beat --input input.csv
```

Enable extra creative and experimental style generation:
```bash
doc2beat --url "https://example.com/docs" --extra-creative
```

### Input CSV Format

The input CSV should have columns:
- `document_url` (required): URL of the documentation
- `song_style` (optional): Specific song style to use

### Output

The tool generates an `output.csv` file with the following columns:
- `document_url`: The input documentation URL
- `song_style`: The generated or provided song style
- `song_lyrics`: The generated song lyrics

## Workflow

1. **Style Generation**: If song_style is not provided, the LLM randomly selects from a comprehensive list of music genres and generates a song style description (up to 1000 characters)
2. **Content Extraction**: The document content is retrieved and intelligently parsed, removing navigation, headers, footers, and website noise
3. **Lyric Generation**: The LLM generates song lyrics based on the cleaned document content and song style, preserving instructional details and technical accuracy (up to 5000 characters)
4. **Results**: Output is saved to the specified CSV file (default: `output.csv`)

## Advanced Features

### Content Extraction

The tool uses BeautifulSoup to extract clean documentation content from HTML pages, filtering out:
- Navigation menus and sidebars
- Headers and footers
- Script tags and styles
- Common website noise patterns
- Breadcrumbs and pagination

This ensures that only the actual documentation content is used for lyric generation.

### Genre Diversity

By default, doc2beat randomly selects from a comprehensive list of music genres including:
- Classical (Baroque, Romantic, Opera, etc.)
- Blues and Folk genres
- Electronic (House, Techno, Synthwave, etc.)
- Hip Hop and Rap styles
- Jazz variations
- Pop and Rock styles
- Regional genres (Afrobeat, K-pop, J-pop, etc.)
- And many more...

Each generation presents 5 random genres for the LLM to choose from, ensuring diversity across documentations.

### Extra Creative Mode

The `--extra-creative` flag enables additional creativity in style generation:
- **Standard Mode**: Clean, straightforward genre descriptions with standard instrumentation
- **Extra Creative Mode**: Experimental styles with unexpected sonic twists, unusual vocal effects, inventive instrumentation choices, genre fusions, and bold production techniques

Example with extra creative mode enabled might generate styles like:
- "Glitchy Jazz-Funk Protest Anthem with Vocal Distortion"
- "Kayokyoku Noir Dreamscape"
- "Conscious Rap with Ethereal Vocal Layers"
