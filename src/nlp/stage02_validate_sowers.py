# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging

from bs4 import BeautifulSoup

# ============================================================
# Section 2. Define Run Validate Function
# ============================================================


def run_validate(
    html_content: str,
    LOG: logging.Logger,
) -> BeautifulSoup:
    """Inspect and validate HTML structure.

    Args:
        html_content (str): The raw HTML content from the Extract stage.
        LOG (logging.Logger): The logger instance.

    Returns:
        BeautifulSoup: The validated BeautifulSoup object.
    """
    LOG.info("========================")
    LOG.info("STAGE 02: VALIDATE starting...")
    LOG.info("========================")

    # ============================================================
    # INSPECT HTML STRUCTURE
    # ============================================================

    LOG.info("HTML STRUCTURE INSPECTION:")

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Log the type of the top-level HTML structure.
    LOG.info(f"Top-level type: {type(soup).__name__}")

    # Log the top-level elements in the HTML document
    LOG.info(
        f"Top-level elements: {[element.name for element in soup.find_all(recursive=False)]}"
    )

    # ============================================================
    # VALIDATE EXPECTATIONS
    # ============================================================

    # Check for expected structural elements on the KISS homepage
    title = soup.find("h1")
    if title is None:
        title = soup.find("h2")

    subtitle = soup.find(
        string=lambda text: (
            isinstance(text, str) and "Improving Stroke Outcomes Across Kansas" in text
        )
    )
    map_heading = soup.find("h3")
    capability_levels = soup.find_all("h5")

    LOG.info("VALIDATE: Title found: %s", title is not None)
    LOG.info("VALIDATE: Subtitle found: %s", subtitle is not None)
    LOG.info("VALIDATE: Map heading found: %s", map_heading is not None)
    LOG.info("VALIDATE: Capability levels found: %s", len(capability_levels) > 0)

    missing = []
    if not title:
        missing.append("title")
    if not subtitle:
        missing.append("subtitle")
    if not map_heading:
        missing.append("map_heading")
    if not capability_levels:
        missing.append("capability_levels")

    if missing:
        raise ValueError(
            f"VALIDATE: Required elements missing: {missing}. "
            "Page structure may have changed."
        )

    LOG.info("VALIDATE: HTML structure is valid.")
    LOG.info("Sink: validated BeautifulSoup object")

    # Return the validated BeautifulSoup object for use in the next stage.
    return soup
