import requests
from bs4 import BeautifulSoup
from worker.tools.registry import register_tool

def fetch_and_summarize(url: str) -> str:
    """
    Fetches the contents of a web page and returns the first 1000 characters of extracted text.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text[:1000]  # Trimmed output
    except Exception as e:
        return f"Error fetching or summarizing the page: {e}"

# Register the tool in the global registry
register_tool(
    name="fetch_and_summarize",
    func=fetch_and_summarize,
    description="Use this to summarize the content of a public web page by providing its URL."
)
