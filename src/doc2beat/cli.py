"""Command-line interface for doc2beat."""

import argparse
import sys
from .core import Doc2Beat


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Convert technical documentation into songs"
    )

    parser.add_argument(
        "--url",
        type=str,
        help="Single document URL to process"
    )

    parser.add_argument(
        "--style",
        type=str,
        help="Song style for single document (optional)"
    )

    parser.add_argument(
        "--input",
        type=str,
        help="Path to input CSV file with document_url and optional song_style columns"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="output.csv",
        help="Path to output CSV file (default: output.csv)"
    )

    parser.add_argument(
        "--creds",
        type=str,
        default="creds.yaml",
        help="Path to credentials YAML file (default: creds.yaml)"
    )

    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration YAML file (default: config.yaml)"
    )

    parser.add_argument(
        "--extra-creative",
        action="store_true",
        help="Enable extra creative and experimental style generation (default: False)"
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.url and not args.input:
        parser.error("Either --url or --input must be provided")

    if args.url and args.input:
        parser.error("Cannot use both --url and --input")

    try:
        # Initialize Doc2Beat
        doc2beat = Doc2Beat(creds_path=args.creds, config_path=args.config, extra_creative=args.extra_creative)

        # Process single URL
        if args.url:
            result = doc2beat.process_single_input(args.url, args.style)
            
            # Save to CSV
            import pandas as pd
            df = pd.DataFrame([result])
            df.to_csv(args.output, index=False)
            print(f"\nResults saved to {args.output}")

            # Display results
            print("\n" + "=" * 80)
            print(f"Document URL: {result['document_url']}")
            print(f"Song Style: {result['song_style']}")
            print("\nSong Lyrics:")
            print(result['song_lyrics'])
            print("=" * 80)

        # Process from CSV
        elif args.input:
            doc2beat.process_from_csv(args.input, args.output)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("\nMake sure creds.yaml and config.yaml exist.", file=sys.stderr)
        print("Copy example_creds.yaml to creds.yaml and add your API key.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
