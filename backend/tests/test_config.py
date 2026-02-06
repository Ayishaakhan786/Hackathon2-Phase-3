from src.core.config import settings

def test_config_loading():
    """Test that configuration is loaded correctly"""
    try:
        print(f"Database URL loaded: {'Yes' if settings.DATABASE_URL else 'No'}")
        print(f"Database URL: {settings.DATABASE_URL[:50]}...")
        print(f"API Host: {settings.API_HOST}")
        print(f"API Port: {settings.API_PORT}")
        print(f"Log Level: {settings.LOG_LEVEL}")
        print("Configuration loaded successfully!")
        return True
    except Exception as e:
        print(f"Configuration loading failed: {e}")
        return False

if __name__ == "__main__":
    test_config_loading()