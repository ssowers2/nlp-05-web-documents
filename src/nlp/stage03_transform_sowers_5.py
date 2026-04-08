"""
src/nlp/stage03_transform_sowers_5.py

Source: validated BeautifulSoup object
Sink: Pandas DataFrame

NOTE: We use Pandas here to contrast with Polars (from Module 4).
You may use Polars or another library if you prefer:
the pipeline pattern is identical; only the DataFrame API differs.

Pandas vs. Polars:
- Pandas is widely used and has a larger ecosystem.
- Polars is faster, more memory efficient, handles larger datasets,
  and is better suited for production pipelines and complex
  transformations.

Purpose

  Transform validated BeautifulSoup object into a structured format.

Analytical Questions

- Which fields are needed from the HTML data?
- How can records be normalized into tabular form?
- What derived fields would support analysis?

How to find the fields you want to extract from the web page:

  1. Open the web page in your browser.
  2. Right-click anywhere on the page and select "View Page Source".
  3. Use Ctrl+F to search for text you can see on the page,
     e.g. the page title or a subtitle.
  4. Find the HTML tag and class that wraps it.
  5. Use soup.find(...) or soup.find_all(...) to locate the associated tag(s).
  6. Use .get_text(strip=True) to extract the visible text from inside the tag.
  7. If the tag is not found, soup.find() returns None which is not a string.
     To avoid errors, use a conditional expression to return "unknown" as a safe fallback:
       value = tag.get_text(strip=True) if tag else "unknown"

Apply this process for each field you want to extract for analysis.
The same approach works for any web page.

Example: For the KISS homepage at https://www.kissnetwork.us/,
we can extract the following fields using BeautifulSoup:

- title from <h1> or <h2> (string)
- subtitle from visible page text (string)
- map heading from <h3> (string)
- capability levels from <h5> (string)
- page description from <meta> tag (string)

we can calculate derived fields like:
- title word count (integer)
- capability count (integer)

IMPORTANT: Getting information from a web page is not as simple as it looks.
Web pages are designed for human consumption, not for data extraction.
The HTML structure can be complex and inconsistent, and may require careful inspection and handling to extract the desired information.
This stage requires careful inspection of the HTML structure and thoughtful handling of edge cases to ensure we extract clean, structured data for analysis.
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging

from bs4 import BeautifulSoup, Tag
import pandas as pd

# ============================================================
# Section 2. Define Run Transform Function
# ============================================================


def run_transform(
    soup: BeautifulSoup,
    LOG: logging.Logger,
) -> pd.DataFrame:
    """Transform HTML into a structured DataFrame.

    Args:
        soup (BeautifulSoup): Validated BeautifulSoup object.
        LOG (logging.Logger): The logger instance.

    Returns:
        pd.DataFrame: The transformed dataset.
    """
    LOG.info("========================")
    LOG.info("STAGE 03: TRANSFORM starting...")
    LOG.info("========================")

    LOG.info("Extracting metadata from HTML")
    LOG.info(
        "We must manually inspect the HTML structure to identify the fields we want to extract."
    )
    LOG.info(
        "For this KISS page, we can extract:"
        "\n- Title from <h1> or <h2>"
        "\n- Subtitle from visible page text"
        "\n- Map heading from <h3>"
        "\n- Capability levels from <h5>"
        "\n- Page description from page text"
    )
    LOG.info("Replace any missing content with `unknown` to ensure all are strings.")

    LOG.info("========================")
    LOG.info("STAGE 03a: Extract key page fields")
    LOG.info("========================")

    # By reading the KISS homepage source, we can extract key page content.

    # Main title from <h1> or fallback to <h2>
    title_tag: Tag | None = soup.find("h1")
    if title_tag is None:
        title_tag = soup.find("h2")

    # Subtitle text appears near the main heading
    subtitle_tag: Tag | None = soup.find("title")

    subtitle: str = subtitle_tag.get_text(strip=True) if subtitle_tag else "unknown"

    # Section heading for the treatment map area
    map_heading_tag: Tag | None = soup.find("h3")

    # Get all capability headings
    capability_heading_tags: list[Tag] = soup.find_all("h5")

    # Extract clean text with safe fallbacks
    title: str = title_tag.get_text(strip=True) if title_tag else "unknown"
    subtitle: str = subtitle_tag.get_text(strip=True) if subtitle_tag else "unknown"

    map_heading: str = (
        map_heading_tag.get_text(strip=True) if map_heading_tag else "unknown"
    )

    # Turn the capability heading tags into a clean comma-separated string
    capability_levels: str = (
        ", ".join(
            [
                tag.get_text(strip=True).replace(":", "")
                for tag in capability_heading_tags
            ]
        )
        if capability_heading_tags
        else "unknown"
    )

    # Extract page description or fallback to unknown
    description_tag = soup.find("meta", attrs={"name": "description"})
    description = (
        description_tag.get("content", "unknown").strip()
        if description_tag
        else "unknown"
    )

    # Log the extracted values for debugging
    LOG.info(f"Extracted title: {title}")
    LOG.info(f"Extracted subtitle: {subtitle}")
    LOG.info(f"Extracted map heading: {map_heading}")
    LOG.info(f"Extracted capability levels: {capability_levels}")
    LOG.info(f"Extracted page description: {description}")

    LOG.info("========================")
    LOG.info("STAGE 03b: Calculate derived fields")
    LOG.info("========================")

    # Phase 4: Added derived field (title_word_count)
    # Calculate derived field: title word count
    title_word_count: int = len(title.split()) if title != "unknown" else 0
    LOG.info(f"Calculated title word count: {title_word_count}")

    # Calculate derived field: capability count
    capability_count: int = (
        len([c.strip() for c in capability_levels.split(",")])
        if capability_levels != "unknown"
        else 0
    )
    LOG.info(f"Calculated capability count: {capability_count}")

    LOG.info("========================")
    LOG.info("STAGE 03c: Build record and create DataFrame")
    LOG.info("========================")

    record = {
        "title": title,
        "subtitle": subtitle,
        "map_heading": map_heading,
        "capability_levels": capability_levels,
        "description": description,
        "title_word_count": title_word_count,
        "capability_count": capability_count,
    }

    df = pd.DataFrame([record])
    LOG.info(f"Created DataFrame with {len(df)} row and {len(df.columns)} columns")
    LOG.info(f"Columns: {list(df.columns)}")

    LOG.info("DataFrame Details")
    LOG.info(f"  Title: {title}")
    LOG.info(f"  Capability count: {record['capability_count']}")
    LOG.info(f"  Title word count: {record['title_word_count']}")
    LOG.info(f"  DataFrame preview:\n{df.head()}")

    LOG.info("Sink: Pandas DataFrame created")
    LOG.info("Transformation complete.")

    # Return the transformed DataFrame for use in the Load stage.
    return df
