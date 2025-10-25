"""Core functionality for doc2beat."""

import os
import yaml
import requests
import pandas as pd
from typing import List, Dict, Optional
from openai import OpenAI


class Doc2Beat:
    """Main class for converting documentation to song lyrics."""

    def __init__(self, creds_path: str = "creds.yaml", config_path: str = "config.yaml"):
        """
        Initialize Doc2Beat with credentials and configuration.

        Args:
            creds_path: Path to credentials YAML file
            config_path: Path to configuration YAML file
        """
        # Load credentials
        with open(creds_path, 'r') as f:
            creds = yaml.safe_load(f)
        self.api_key = creds['openrouter_api_key']

        # Load configuration
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        self.lyric_model = config['lyric_model']

        # Initialize OpenAI client with OpenRouter
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )

    def generate_song_style(self, document_url: str) -> str:
        """
        Generate a random song style prompt for the given document.

        Args:
            document_url: URL of the documentation

        Returns:
            Song style prompt (under 1000 characters)
        """
        prompt = (
            "Generate a random song style prompt (not instrumental) for a song generation model. "
            "The style should be under 1000 characters. "
            "Output ONLY the song style prompt, nothing else. "
            "Examples: 'upbeat pop with electronic elements', 'soulful jazz ballad', 'energetic rock anthem'"
        )

        response = self.client.chat.completions.create(
            model=self.lyric_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates song style prompts."},
                {"role": "user", "content": prompt}
            ],
            temperature=1.0,  # High temperature for more randomness
        )

        song_style = response.choices[0].message.content.strip()
        # Ensure it's under 1000 characters
        if len(song_style) > 1000:
            song_style = song_style[:997] + "..."
        return song_style

    def fetch_document_content(self, document_url: str) -> str:
        """
        Fetch the content from the document URL.

        Args:
            document_url: URL of the documentation

        Returns:
            Document content as text
        """
        try:
            response = requests.get(document_url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Warning: Could not fetch content from {document_url}: {e}")
            return f"[Could not fetch content from {document_url}]"

    def generate_song_lyrics(self, document_content: str, song_style: str) -> str:
        """
        Generate song lyrics based on document content and style.

        Args:
            document_content: The text content of the documentation
            song_style: The style of song to generate

        Returns:
            Generated song lyrics (up to 5000 characters)
        """
        # Limit document content to prevent overly long lyrics
        content_for_prompt = document_content[:8000]
        
        prompt = f"""Based on the following technical documentation, create song lyrics in the style: "{song_style}"

The song should communicate the key concepts from the documentation in an easy-to-understand and fun way.
The lyrics should be no longer than 5000 characters, but can be shorter if the content is brief.

Documentation content:
{content_for_prompt}

Output ONLY the song lyrics, nothing else."""

        response = self.client.chat.completions.create(
            model=self.lyric_model,
            messages=[
                {"role": "system", "content": "You are a creative songwriter who transforms technical documentation into engaging song lyrics."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
        )

        lyrics = response.choices[0].message.content.strip()
        # Ensure lyrics don't exceed 5000 characters
        if len(lyrics) > 5000:
            lyrics = lyrics[:4997] + "..."
        return lyrics

    def process_single_input(
        self,
        document_url: str,
        song_style: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Process a single document URL.

        Args:
            document_url: URL of the documentation
            song_style: Optional predefined song style

        Returns:
            Dictionary with document_url, song_style, and song_lyrics
        """
        print(f"Processing: {document_url}")

        # Step 2: Generate song style if not provided
        if song_style is None:
            print("  Generating song style...")
            song_style = self.generate_song_style(document_url)
        print(f"  Song style: {song_style}")

        # Step 3: Fetch document content
        print("  Fetching document content...")
        document_content = self.fetch_document_content(document_url)

        # Step 3: Generate song lyrics
        print("  Generating song lyrics...")
        song_lyrics = self.generate_song_lyrics(document_content, song_style)

        return {
            'document_url': document_url,
            'song_style': song_style,
            'song_lyrics': song_lyrics
        }

    def process_multiple_inputs(
        self,
        inputs: List[Dict[str, str]],
        output_path: str = "output.csv"
    ) -> pd.DataFrame:
        """
        Process multiple document URLs.

        Args:
            inputs: List of dictionaries with 'document_url' and optional 'song_style'
            output_path: Path to save output CSV

        Returns:
            DataFrame with results
        """
        results = []

        for input_data in inputs:
            document_url = input_data['document_url']
            song_style = input_data.get('song_style')

            result = self.process_single_input(document_url, song_style)
            results.append(result)

        # Create DataFrame and save
        df = pd.DataFrame(results)
        df.to_csv(output_path, index=False)
        print(f"\nResults saved to {output_path}")

        return df

    def process_from_csv(
        self,
        input_path: str,
        output_path: str = "output.csv"
    ) -> pd.DataFrame:
        """
        Process documents from a CSV file.

        Args:
            input_path: Path to input CSV file
            output_path: Path to save output CSV

        Returns:
            DataFrame with results
        """
        # Read input CSV
        df = pd.read_csv(input_path)

        # Convert to list of dictionaries
        inputs = df.to_dict('records')

        return self.process_multiple_inputs(inputs, output_path)
