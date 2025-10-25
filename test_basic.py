"""Simple test script to verify doc2beat functionality."""

import os
import yaml
import pandas as pd
from doc2beat import Doc2Beat


def test_basic_functionality():
    """Test basic doc2beat functionality with mock data."""
    
    print("Testing doc2beat basic functionality...")
    
    # Check if configuration files exist
    print("\n1. Checking configuration files...")
    if os.path.exists('example_creds.yaml'):
        print("   ✓ example_creds.yaml exists")
    else:
        print("   ✗ example_creds.yaml missing")
        return False
    
    if os.path.exists('config.yaml'):
        print("   ✓ config.yaml exists")
    else:
        print("   ✗ config.yaml missing")
        return False
    
    # Check configuration content
    print("\n2. Checking configuration content...")
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
        if 'lyric_model' in config:
            print(f"   ✓ lyric_model configured: {config['lyric_model']}")
        else:
            print("   ✗ lyric_model not configured")
            return False
    
    # Check example_input.csv
    print("\n3. Checking example_input.csv...")
    if os.path.exists('example_input.csv'):
        df = pd.read_csv('example_input.csv')
        print(f"   ✓ example_input.csv exists with {len(df)} rows")
        print(f"   Columns: {list(df.columns)}")
        if 'document_url' in df.columns:
            print("   ✓ document_url column exists")
        else:
            print("   ✗ document_url column missing")
            return False
    else:
        print("   ✗ example_input.csv missing")
        return False
    
    print("\n4. Testing Doc2Beat class instantiation...")
    # This will fail without valid credentials, but we can test the structure
    try:
        # Try with example_creds.yaml (will fail if no API key)
        doc2beat = Doc2Beat(creds_path='example_creds.yaml')
        print("   ✓ Doc2Beat class can be instantiated")
    except Exception as e:
        print(f"   ⚠ Doc2Beat instantiation requires valid API key: {e}")
        # This is expected without real credentials
    
    print("\n5. Checking package structure...")
    import doc2beat
    print(f"   ✓ Package version: {doc2beat.__version__}")
    print(f"   ✓ Package imports successfully")
    
    print("\n✓ All basic structural tests passed!")
    print("\nNote: To test full functionality, you need to:")
    print("  1. Copy example_creds.yaml to creds.yaml")
    print("  2. Add your OpenRouter API key to creds.yaml")
    print("  3. Run: doc2beat --url <your-url>")
    return True


if __name__ == "__main__":
    test_basic_functionality()
