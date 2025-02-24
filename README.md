# kindle-character-dictionary

# Kindle Character Dictionary Generator

## MVP Phase: Overview

### Goal
This MVP will allow users to:
- Enter a book title and fetch character and plot data from Wikipedia.
- Use an LLM to structure character relationships.
- Generate a Kindle dictionary that allows character lookup while reading.

## Project Workflow

The MVP consists of a **four-step pipeline**:

### 1️⃣ Step 1: Scrape Wikipedia for Book Data

**Objective:** Extract the book's plot summary and character list from Wikipedia.

This step:
- Searches for the correct Wikipedia page using the Wikipedia API.
- Extracts plot information if available.
- Extracts character names from the Characters section if available.
- Saves this information in a structured JSON format.

**File:** `src/scrape_wikipedia.py`

### 2️⃣ Step 2: Use an LLM to Extract Character Relationships

**Objective:** Structure the extracted data into a knowledge graph-style format.

This step:
- Sends the plot summary and character names to an LLM.
- Analyzes relationships such as friends, family, and enemies.
- Returns structured character descriptions and relationships.

**File:** `src/llm_character_extraction.py`

### 3️⃣ Step 3: Convert Data to Kindle Dictionary Format

**Objective:** Convert the structured data into a Kindle-compatible dictionary format.

This step:
- Takes structured character information.
- Formats it into a Kindle dictionary text format.
- Exports it as a MOBI or PRC file.

**File:** `src/kindle_generator.py`

### 4️⃣ Step 4: Automate the Full Process

**Objective:** Create a CLI tool that runs all steps automatically.

This step:
- Takes a book title as input from the user.
- Runs the Wikipedia scraper to fetch book data.
- Calls the LLM to structure character relationships.
- Generates the Kindle dictionary and saves it.

**File:** `generate_dictionary.py`

## Next Steps

Once the MVP is complete, the next steps include:
- Handling missing Wikipedia pages by implementing a fallback to Wikidata or Fandom scraping.
- Improving LLM accuracy by refining prompts and structuring relationships more effectively.
- Building a simple UI or API to allow non-technical users to generate Kindle dictionaries.

## Running the MVP

### Installation