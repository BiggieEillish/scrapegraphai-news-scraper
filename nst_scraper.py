from scrapegraphai.graphs import SmartScraperMultiGraph
import json
import os
from datetime import datetime

# Updated configuration based on README examples
graph_config = {
    "llm": {
        "model": "ollama/llama2",
        "model_tokens": 8192,
        "base_url": os.getenv('OLLAMA_HOST', 'http://host.docker.internal:11434')
    },
    "verbose": True,
    "headless": True  # Keep headless for Docker environment
}

def scrape_nst():
    url = "https://www.thestar.com.my/news"
    
    # Simplified prompt following documentation style
    smart_scraper_graph = SmartScraperMultiGraph(
        prompt = """You are to extract at least 10 latest news from the source URL. 
        The extracted news should include the title, summary, and URL of the news article. The output should be saved in a JSON file named nst_articles.json.""",
        source=[url],
        config=graph_config
    )

    try:
        result = smart_scraper_graph.run()
        
        os.makedirs('data', exist_ok=True)
        
        output = {
            "scrape_timestamp": datetime.now().isoformat(),
            "sections_scraped": [url],
            "articles": result.get("articles", []) if isinstance(result, dict) else []
        }
        
        with open('data/nst_articles.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=4, ensure_ascii=False)
            
        return output
    except Exception as e:
        print(f"Error during scraping: {e}")
        return None

if __name__ == "__main__":
    data = scrape_nst()
    if data:
        articles = data.get("articles", [])
        print(f"Successfully scraped {len(articles)} articles")
        print(f"Data saved to data/nst_articles.json")