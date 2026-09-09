print("Hello World!")
print("Testing import...")

try:
    import requests
    print("✅ requests imported")
except ImportError as e:
    print(f"❌ requests error: {e}")

try:
    from bs4 import BeautifulSoup
    print("✅ BeautifulSoup imported")
except ImportError as e:
    print(f"❌ BeautifulSoup error: {e}")

print("Done!")