import requests
import wikipediaapi
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get user-agent from environment variables
USER_AGENT = os.getenv("USER_AGENT", "KindleCharacterDictionary/1.0 (default@example.com)")


def get_original_language(book_title):
    """Fetches the original language code (e.g., 'en', 'fr') of the book using Wikidata"""
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&titles={book_title.replace(' ', '_')}&sites=enwiki&props=claims&format=json"
    
    try:
        response = requests.get(url).json()
        entities = response.get('entities', {})
        
        for entity in entities.values():
            if 'claims' in entity:
                for prop in ['P364', 'P407']:  # P364 = Original Language, P407 = Language of Work
                    if prop in entity['claims']:
                        language_qid = entity['claims'][prop][0]['mainsnak']['datavalue']['value']['id']
                        return resolve_language_qid(language_qid)
        
        print(f"[WARNING] No language found for '{book_title}', defaulting to English.")
    
    except (KeyError, requests.exceptions.RequestException) as e:
        print(f"[ERROR] Failed to retrieve language for '{book_title}', defaulting to English. Error: {e}")

    return "en"  # Default to English if lookup fails

def resolve_language_qid(qid):
    """Resolves a Wikidata Q-ID (e.g., Q1860) to an actual language code (e.g., 'en')"""
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&props=claims&format=json"
    
    try:
        response = requests.get(url).json()
        claims = response['entities'][qid]['claims']
        
        if 'P424' in claims:  # ISO 639-1 language code
            return claims['P424'][0]['mainsnak']['datavalue']['value']
        
        print(f"[WARNING] No ISO code found for Q-ID '{qid}', defaulting to English.")
    
    except (KeyError, requests.exceptions.RequestException) as e:
        print(f"[ERROR] Failed to resolve Q-ID '{qid}', defaulting to English. Error: {e}")

    return "en"  # Default to English if lookup fails

def get_wikipedia_title_in_language(book_title, lang_code):
    """Finds the correct Wikipedia page title in the target language using Wikidata"""
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&titles={book_title.replace(' ', '_')}&sites=enwiki&props=sitelinks&format=json"
    response = requests.get(url).json()

    try:
        entities = response['entities']
        for entity in entities.values():
            sitelinks = entity.get('sitelinks', {})
            wiki_key = f"{lang_code}wiki"
            if wiki_key in sitelinks:
                return sitelinks[wiki_key]['title']  # Return Wikipedia page title in the correct language
    except KeyError:
        pass

    return book_title  # If no translation is found, return the original title


def get_wikipedia_text(book_title, section_title=None):
    """Get a specific section or the full Wikipedia page in the book's original language"""
    lang_code = get_original_language(book_title)  # Get original language (e.g., 'es' for Spanish)
    correct_title = get_wikipedia_title_in_language(book_title, lang_code)  # Get correct title in that language
    
    # Initialize Wikipedia API with user-agent
    wiki = wikipediaapi.Wikipedia(language=lang_code, user_agent=USER_AGENT)
    page = wiki.page(correct_title)  # Fetch correct Wikipedia page
    
    if page.exists():
        if section_title:
            section = page.section_by_title(section_title)
            if section:
                return section.text
        
        return page.text  # If section is missing, return full page
    
    print(f"[WARNING] Wikipedia page for '{correct_title}' not found in {lang_code}, defaulting to English.")
    
    # Fallback to English Wikipedia if the page doesn't exist
    if lang_code != "en":
        wiki_en = wikipediaapi.Wikipedia(language="en", user_agent=USER_AGENT)
        page_en = wiki_en.page(book_title)
        if page_en.exists():
            return page_en.text
    
    return "Wikipedia page not found."

if __name__ == "__main__":
    book = "The Moon and the Bonfires"
    original_language = get_original_language(book)
    print(f"Original language: {original_language}")
    print(get_wikipedia_title_in_language(book, original_language))



# you should hide your email address in the user_agent parameter