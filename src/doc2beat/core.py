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
        import random
        
        # Comprehensive list of music genres from Wikipedia
        music_genres = [
            # Classical
            "Baroque", "Classical", "Romantic", "Modern Classical", "Opera", "Chamber Music", "Symphony", "Concerto",
            
            # Popular - Avant-garde & experimental
            "Avant-garde", "Experimental", "Noise", "Ambient", "Drone", "Minimalism",
            
            # Blues
            "Blues", "Delta Blues", "Chicago Blues", "Electric Blues", "Blues Rock", "Rhythm and Blues",
            
            # Country
            "Country", "Country Rock", "Bluegrass", "Honky-tonk", "Outlaw Country", "Country Pop", "Alt-Country", "Country Folk",
            
            # Easy listening
            "Easy Listening", "Lounge", "Smooth Jazz", "Adult Contemporary", "Soft Rock",
            
            # Electronic
            "Electronic", "House", "Techno", "Trance", "Ambient", "IDM", "Dubstep", "Drum and Bass", "Breakbeat", "Electro", "Synthwave", "Vaporwave", "Chillwave", "Future Bass", "Trap", "Lo-fi Hip Hop",
            
            # Folk
            "Folk", "Folk Rock", "Indie Folk", "Singer-Songwriter", "Acoustic Folk", "Celtic Folk", "Americana", "Roots Music",
            
            # Hip hop
            "Hip Hop", "Rap", "Trap", "Drill", "Boom Bap", "Alternative Hip Hop", "Conscious Rap", "Gangsta Rap", "Mumble Rap",
            
            # Jazz
            "Jazz", "Bebop", "Swing", "Big Band", "Cool Jazz", "Hard Bop", "Free Jazz", "Fusion", "Smooth Jazz", "Vocal Jazz", "Jazz Blues",
            
            # Pop
            "Pop", "Pop Rock", "Power Pop", "Bubblegum Pop", "Teen Pop", "Dance Pop", "Electropop", "Synthpop", "Indie Pop", "Art Pop", "Baroque Pop",
            
            # R&B & Soul
            "R&B", "Soul", "Motown", "Funk", "Disco", "Contemporary R&B", "Neo-Soul", "Gospel", "Spirituals",
            
            # Rock
            "Rock", "Rock and Roll", "Classic Rock", "Hard Rock", "Soft Rock", "Progressive Rock", "Psychedelic Rock", "Art Rock", "Alternative Rock", "Indie Rock", "Grunge", "Britpop", "Post-Rock", "Math Rock", "Shoegaze", "Dream Pop",
            
            # Metal
            "Heavy Metal", "Thrash Metal", "Death Metal", "Black Metal", "Power Metal", "Progressive Metal", "Nu Metal", "Metalcore", "Deathcore",
            
            # Punk
            "Punk", "Hardcore Punk", "Post-Punk", "New Wave", "Post-Hardcore", "Emo", "Pop Punk", "Ska Punk", "Crust Punk",
            
            # Regional - African
            "Afrobeat", "Highlife", "Mbalax", "Soukous", "Kwaito", "Afro-pop", "Afro-jazz",
            
            # Regional - Asian
            "J-pop", "K-pop", "C-pop", "Bollywood", "Enka", "Kayokyoku", "Mandopop", "Cantopop",
            
            # Regional - European
            "Europop", "Eurodance", "Italo Disco", "French Pop", "Schlager", "Fado", "Flamenco", "Celtic", "Folk Rock",
            
            # Regional - Latin & South American
            "Salsa", "Merengue", "Bachata", "Reggaeton", "Cumbia", "Bossa Nova", "Samba", "Tango", "Mariachi", "Latin Pop", "Latin Rock",
            
            # Regional - North American
            "Americana", "Bluegrass", "Cajun", "Zydeco", "Tejano", "Native American Music",
            
            # Religious
            "Gospel", "Christian Rock", "Christian Pop", "Contemporary Christian", "Spirituals", "Sacred Music", "Chant", "Hymns",
            
            # Traditional folk
            "Traditional Folk", "World Music", "Ethnic Music", "Indigenous Music", "Folk Revival", "Protest Songs",
            
            # Other
            "New Age", "Worldbeat", "Fusion", "Crossover", "Experimental Rock", "Art Rock", "Prog Rock", "Space Rock", "Krautrock", "Canterbury Scene"
        ]
        
        # Randomly shuffle the genre list for each generation
        random.shuffle(music_genres)
        selected_genres = music_genres[:5]  # Pick first 5 from shuffled list
        
        prompt = (
            f"Generate a CREATIVE and INVENTIVE VOCAL song description for Suno AI under 1000 characters. "
            f"RANDOM GENRE SELECTION: From this shuffled list, randomly pick ONE genre: {', '.join(selected_genres)}. "
            f"CRITICAL: Must be a VOCAL genre - no instrumental music. "
            f"BE INVENTIVE: Add unexpected sonic twists, unusual vocal effects, creative instrumentation choices, or genre fusions. Think outside the box - add experimental elements, unusual production techniques, or bold creative choices. "
            f"Include: genre/style with creative twists, tempo with variation, inventive vocal characteristics, unique instrumentation, mood/atmosphere, and lyrical themes. "
            f"Be specific, vivid, and CREATIVE. Make it memorable and interesting! Output ONLY the song style prompt, nothing else."
        )

        response = self.client.chat.completions.create(
            model=self.lyric_model,
            messages=[
                {"role": "system", "content": "You are a creative and inventive assistant that generates unique VOCAL song style prompts. Always specify vocal genres with singing - never instrumental music. Be highly creative: add unexpected sonic twists, unusual vocal effects, inventive instrumentation choices, experimental elements, and bold production techniques. You will be given a random selection of genres to choose from - pick ONE genre and build an inventive, memorable, and creative song style description around it. Be specific, vivid, and think outside the box!"},
                {"role": "user", "content": prompt}
            ],
            temperature=1.2,  # Even higher temperature for maximum randomness
        )

        song_style = response.choices[0].message.content.strip()
        # Ensure it's under 1000 characters
        if len(song_style) > 1000:
            song_style = song_style[:997] + "..."
        return song_style

    def fetch_document_content(self, document_url: str) -> str:
        """
        Fetch the content from the document URL and extract the actual documentation content.

        Args:
            document_url: URL of the documentation

        Returns:
            Cleaned documentation content as text
        """
        try:
            print(f"    Fetching from: {document_url}")
            response = requests.get(document_url, timeout=15)
            response.raise_for_status()
            html_content = response.text
            print(f"    Fetched {len(html_content)} characters")
            
            # Extract the actual documentation content
            doc_content = self.extract_documentation_content(html_content)
            print(f"    Extracted {len(doc_content)} characters of documentation content")
            return doc_content
        except Exception as e:
            print(f"Warning: Could not fetch content from {document_url}: {e}")
            return f"[Could not fetch content from {document_url}]"

    def extract_documentation_content(self, html_content: str) -> str:
        """
        Extract the actual documentation content from HTML, filtering out navigation, headers, footers, etc.
        
        Args:
            html_content: Raw HTML content from the page
            
        Returns:
            Cleaned documentation text content
        """
        try:
            from bs4 import BeautifulSoup
            import re
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['nav', 'header', 'footer', 'aside', 'script', 'style', 'meta', 'link']):
                element.decompose()
            
            # Look for common documentation content containers
            content_selectors = [
                'main', 'article', '.content', '.documentation', '.doc-content',
                '.main-content', '.page-content', '.post-content', '.entry-content',
                '#content', '#main', '#documentation', '.markdown-body'
            ]
            
            content_text = ""
            
            # Try to find the main content area
            for selector in content_selectors:
                content_element = soup.select_one(selector)
                if content_element:
                    content_text = content_element.get_text(separator=' ', strip=True)
                    break
            
            # If no specific content area found, try to extract from body but filter out common noise
            if not content_text:
                body = soup.find('body')
                if body:
                    # Remove common navigation and UI elements
                    for element in body.find_all(['nav', 'header', 'footer', 'aside', 'menu', 'ul', 'ol']):
                        if any(keyword in element.get_text().lower() for keyword in 
                              ['navigation', 'menu', 'sidebar', 'footer', 'header', 'breadcrumb', 'toc']):
                            element.decompose()
                    
                    content_text = body.get_text(separator=' ', strip=True)
            
            # Clean up the text
            if content_text:
                # Remove excessive whitespace
                content_text = re.sub(r'\s+', ' ', content_text)
                # Remove common website noise patterns
                noise_patterns = [
                    r'cookie\s+policy',
                    r'privacy\s+policy', 
                    r'terms\s+of\s+service',
                    r'follow\s+us\s+on',
                    r'subscribe\s+to',
                    r'newsletter',
                    r'social\s+media',
                    r'copyright.*?\d{4}',
                    r'all\s+rights\reserved',
                    r'last\s+updated.*?\d{4}',
                    r'page\s+\d+\s+of\s+\d+',
                    r'next\s+page',
                    r'previous\s+page',
                    r'home\s*>\s*.*?>\s*.*?>\s*.*?',  # Breadcrumbs
                ]
                
                for pattern in noise_patterns:
                    content_text = re.sub(pattern, '', content_text, flags=re.IGNORECASE)
                
                # Final cleanup
                content_text = re.sub(r'\s+', ' ', content_text).strip()
            
            return content_text if content_text else html_content
            
        except Exception as e:
            print(f"Warning: Could not extract documentation content: {e}")
            # Fallback to original content
            return html_content

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

CRITICAL REQUIREMENTS:
1. PRESERVE INSTRUCTIONAL CONTENT: Include specific steps, procedures, commands, and technical details from the documentation
2. CAPTURE GUIDANCE: Include how-to information, best practices, warnings, and troubleshooting tips
3. MAINTAIN ACCURACY: Don't generalize - use the actual technical terms, concepts, and processes described
4. EDUCATIONAL VALUE: The song should teach listeners the same information as the documentation

The song should communicate the key concepts, procedures, and instructions from the documentation in an easy-to-understand and engaging way.
The lyrics should be no longer than 5000 characters, but can be shorter if the content is brief.

IMPORTANT ACRONYM HANDLING:
- Avoid problematic acronyms that Suno mispronounces like "AI" (pronounced "a-eye"), "NIH" (pronounced "en-aye-aytch"), "ORCID" (pronounced "ork-id")
- Instead, use full words or alternative phrasing: "artificial intelligence" instead of "AI", "research institute" instead of "NIH", "researcher ID" instead of "ORCID"
- Acronyms that work well: "SSO", "NSF", "API", "URL", "HTML", "CSS", "JSON", "XML"
- When in doubt, spell out acronyms phonetically or use descriptive terms

Documentation content:
{content_for_prompt}

Output ONLY the song lyrics, nothing else."""

        print(f"    Generating lyrics with {self.lyric_model}...")
        response = self.client.chat.completions.create(
            model=self.lyric_model,
            messages=[
                {"role": "system", "content": "You are a creative songwriter who transforms technical documentation into engaging song lyrics. CRITICAL: Preserve all instructional content, procedures, commands, and technical details from the documentation. Include specific steps, how-to information, best practices, and warnings. Don't generalize - maintain accuracy of technical terms and processes. Always avoid problematic acronyms that Suno mispronounces (like AI, NIH, ORCID) and use full words or alternative phrasing instead."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
        )
        print(f"    Generated {len(response.choices[0].message.content)} characters of lyrics")

        lyrics = response.choices[0].message.content.strip()
        # Ensure lyrics don't exceed 5000 characters
        if len(lyrics) > 5000:
            lyrics = lyrics[:4997] + "..."
        return lyrics

    def process_single_input(
        self,
        document_url: str,
        song_style: Optional[str] = None,
        verbose: bool = True
    ) -> Dict[str, str]:
        """
        Process a single document URL.

        Args:
            document_url: URL of the documentation
            song_style: Optional predefined song style
            verbose: Whether to print detailed progress

        Returns:
            Dictionary with document_url, song_style, and song_lyrics
        """
        if verbose:
            print(f"Processing: {document_url}")

        # Step 2: Generate song style if not provided
        if song_style is None:
            if verbose:
                print("  Generating song style...")
            song_style = self.generate_song_style(document_url)
        if verbose:
            print(f"  Song style: {song_style}")

        # Step 3: Fetch document content
        if verbose:
            print("  Fetching document content...")
        document_content = self.fetch_document_content(document_url)

        # Step 3: Generate song lyrics
        if verbose:
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
        total_inputs = len(inputs)
        
        print(f"\n🎵 Starting batch processing of {total_inputs} documents...")
        print("=" * 60)
        import sys
        sys.stdout.flush()

        for i, input_data in enumerate(inputs, 1):
            document_url = input_data['document_url']
            song_style = input_data.get('song_style')

            print(f"\n📄 Processing {i}/{total_inputs}: {document_url}")
            print(f"Progress: {i}/{total_inputs} ({i/total_inputs*100:.1f}%)")
            sys.stdout.flush()
            
            try:
                result = self.process_single_input(document_url, song_style, verbose=False)
                results.append(result)
                print(f"✅ Completed {i}/{total_inputs}")
                sys.stdout.flush()
            except Exception as e:
                print(f"❌ Error processing {i}/{total_inputs}: {e}")
                sys.stdout.flush()
                # Add error result to maintain order
                results.append({
                    'document_url': document_url,
                    'song_style': song_style or 'Error',
                    'song_lyrics': f'Error processing: {e}'
                })

        # Create DataFrame and save
        df = pd.DataFrame(results)
        df.to_csv(output_path, index=False)
        print(f"\n🎉 Batch processing complete!")
        print(f"📊 Results saved to {output_path}")
        print(f"✅ Successfully processed: {len([r for r in results if not r['song_lyrics'].startswith('Error')])}/{total_inputs}")
        sys.stdout.flush()

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
