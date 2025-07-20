#!/usr/bin/env python3
"""Basic structure test for the Lake Constance Storm Checker integration."""

import os
import json

def test_file_structure():
    """Test that all required files exist."""
    required_files = [
        "custom_components/lake_constance_storm_checker/__init__.py",
        "custom_components/lake_constance_storm_checker/manifest.json",
        "custom_components/lake_constance_storm_checker/config_flow.py",
        "custom_components/lake_constance_storm_checker/const.py",
        "custom_components/lake_constance_storm_checker/sensor.py",
        "custom_components/lake_constance_storm_checker/binary_sensor.py",
        "custom_components/lake_constance_storm_checker/services.py",
        "custom_components/lake_constance_storm_checker/translations/en.json",
        "custom_components/lake_constance_storm_checker/translations/de.json",
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✓ {file_path} exists")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✓ All required files exist")
    return True

def test_manifest():
    """Test that the manifest.json is valid."""
    try:
        with open("custom_components/lake_constance_storm_checker/manifest.json", "r") as f:
            manifest = json.load(f)
        
        required_fields = ["domain", "name", "documentation", "requirements", "version", "config_flow", "iot_class"]
        missing_fields = []
        
        for field in required_fields:
            if field not in manifest:
                missing_fields.append(field)
            else:
                print(f"✓ manifest.json has {field}: {manifest[field]}")
        
        if missing_fields:
            print(f"❌ Missing manifest fields: {missing_fields}")
            return False
        
        # Check specific values
        if manifest["domain"] != "lake_constance_storm_checker":
            print("❌ manifest.json domain should be 'lake_constance_storm_checker'")
            return False
        
        if not manifest["config_flow"]:
            print("❌ manifest.json config_flow should be true")
            return False
        
        print("✓ manifest.json is valid")
        return True
        
    except Exception as e:
        print(f"❌ Error reading manifest.json: {e}")
        return False

def test_translations():
    """Test that translation files are valid JSON."""
    translation_files = [
        "custom_components/lake_constance_storm_checker/translations/en.json",
        "custom_components/lake_constance_storm_checker/translations/de.json",
    ]
    
    for file_path in translation_files:
        try:
            with open(file_path, "r") as f:
                json.load(f)
            print(f"✓ {file_path} is valid JSON")
        except Exception as e:
            print(f"❌ {file_path} is not valid JSON: {e}")
            return False
    
    return True

def test_python_syntax():
    """Test that Python files have valid syntax."""
    python_files = [
        "custom_components/lake_constance_storm_checker/__init__.py",
        "custom_components/lake_constance_storm_checker/config_flow.py",
        "custom_components/lake_constance_storm_checker/const.py",
        "custom_components/lake_constance_storm_checker/sensor.py",
        "custom_components/lake_constance_storm_checker/binary_sensor.py",
        "custom_components/lake_constance_storm_checker/services.py",
    ]
    
    for file_path in python_files:
        try:
            with open(file_path, "r") as f:
                compile(f.read(), file_path, "exec")
            print(f"✓ {file_path} has valid Python syntax")
        except Exception as e:
            print(f"❌ {file_path} has syntax errors: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("Testing Lake Constance Storm Checker integration structure...\n")
    
    success = True
    success &= test_file_structure()
    success &= test_manifest()
    success &= test_translations()
    success &= test_python_syntax()
    
    if success:
        print("\n✅ All structure tests passed!")
        print("The integration should now work properly in Home Assistant.")
        print("\nTo install in Home Assistant:")
        print("1. Copy the custom_components folder to your Home Assistant config directory")
        print("2. Restart Home Assistant")
        print("3. Go to Settings > Devices & Services > Add Integration")
        print("4. Search for 'Lake Constance Storm Checker'")
    else:
        print("\n❌ Some structure tests failed. Please check the errors above.")
        exit(1) 