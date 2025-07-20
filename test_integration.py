#!/usr/bin/env python3
"""Simple test to verify the Lake Constance Storm Checker integration can be loaded."""

import sys
import os

# Add the custom_components directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_components'))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from lake_constance_storm_checker import const
        print("✓ const.py imported successfully")
        
        from lake_constance_storm_checker import config_flow
        print("✓ config_flow.py imported successfully")
        
        from lake_constance_storm_checker import sensor
        print("✓ sensor.py imported successfully")
        
        from lake_constance_storm_checker import binary_sensor
        print("✓ binary_sensor.py imported successfully")
        
        from lake_constance_storm_checker import services
        print("✓ services.py imported successfully")
        
        from lake_constance_storm_checker import __init__
        print("✓ __init__.py imported successfully")
        
        print("\n🎉 All modules imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_constants():
    """Test that required constants are defined."""
    try:
        from lake_constance_storm_checker.const import DOMAIN, AREAS, CONF_BASE_URL, CONF_API_CODE
        
        assert DOMAIN == "lake_constance_storm_checker"
        assert "west" in AREAS
        assert "center" in AREAS
        assert "east" in AREAS
        assert CONF_BASE_URL == "base_url"
        assert CONF_API_CODE == "api_code"
        
        print("✓ All required constants are properly defined")
        return True
        
    except Exception as e:
        print(f"❌ Constants test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Lake Constance Storm Checker integration...\n")
    
    success = True
    success &= test_imports()
    success &= test_constants()
    
    if success:
        print("\n✅ All tests passed! The integration should load properly.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1) 