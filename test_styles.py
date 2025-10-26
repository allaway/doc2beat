#!/usr/bin/env python3
"""Test script to generate only song styles for Synapse URLs."""

import pandas as pd
from doc2beat import Doc2Beat
import sys

def main():
    # Initialize Doc2Beat
    doc2beat = Doc2Beat(creds_path="creds.yaml", config_path="config.yaml")
    
    # Read the URLs
    df = pd.read_csv("final_synapse_urls.csv")
    urls = df['document_url'].tolist()
    
    print(f"🎵 Generating song styles for {len(urls)} Synapse URLs...")
    print("=" * 60)
    sys.stdout.flush()
    
    styles = []
    for i, url in enumerate(urls, 1):
        print(f"\n📄 {i}/{len(urls)}: {url}")
        print(f"Progress: {i}/{len(urls)} ({i/len(urls)*100:.1f}%)")
        sys.stdout.flush()
        
        try:
            print("  Generating style...")
            sys.stdout.flush()
            style = doc2beat.generate_song_style(url)
            styles.append(style)
            print(f"✅ Style: {style[:100]}...")
            sys.stdout.flush()
        except Exception as e:
            print(f"❌ Error: {e}")
            styles.append(f"Error: {e}")
            sys.stdout.flush()
    
    # Save results
    results_df = pd.DataFrame({
        'document_url': urls,
        'song_style': styles
    })
    results_df.to_csv("synapse_styles_only.csv", index=False)
    
    print(f"\n🎉 Style generation complete!")
    print(f"📊 Results saved to synapse_styles_only.csv")
    
    # Analyze diversity
    print(f"\n=== DIVERSITY ANALYSIS ===")
    genre_counts = {}
    for style in styles:
        style_lower = style.lower()
        if 'pop-rock' in style_lower or 'pop rock' in style_lower:
            genre_counts['Pop-Rock'] = genre_counts.get('Pop-Rock', 0) + 1
        elif 'r&b' in style_lower or 'rb' in style_lower:
            genre_counts['R&B'] = genre_counts.get('R&B', 0) + 1
        elif 'soul' in style_lower:
            genre_counts['Soul'] = genre_counts.get('Soul', 0) + 1
        elif 'country' in style_lower:
            genre_counts['Country'] = genre_counts.get('Country', 0) + 1
        elif 'jazz' in style_lower:
            genre_counts['Jazz'] = genre_counts.get('Jazz', 0) + 1
        elif 'blues' in style_lower:
            genre_counts['Blues'] = genre_counts.get('Blues', 0) + 1
        elif 'folk' in style_lower:
            genre_counts['Folk'] = genre_counts.get('Folk', 0) + 1
        elif 'indie' in style_lower:
            genre_counts['Indie'] = genre_counts.get('Indie', 0) + 1
        elif 'alternative' in style_lower:
            genre_counts['Alternative'] = genre_counts.get('Alternative', 0) + 1
        elif 'electronic' in style_lower or 'synth' in style_lower:
            genre_counts['Electronic'] = genre_counts.get('Electronic', 0) + 1
        elif 'reggae' in style_lower:
            genre_counts['Reggae'] = genre_counts.get('Reggae', 0) + 1
        elif 'funk' in style_lower:
            genre_counts['Funk'] = genre_counts.get('Funk', 0) + 1
        elif 'disco' in style_lower:
            genre_counts['Disco'] = genre_counts.get('Disco', 0) + 1
        elif 'gospel' in style_lower:
            genre_counts['Gospel'] = genre_counts.get('Gospel', 0) + 1
        else:
            genre_counts['Other'] = genre_counts.get('Other', 0) + 1
    
    print(f"Total unique genres: {len(genre_counts)}")
    for genre, count in sorted(genre_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{genre}: {count} ({count/len(styles)*100:.1f}%)")

if __name__ == "__main__":
    main()
