"""
Home Page Object
Contains selectors and methods for the patrika.com homepage.

Selectors/logic verified against the LIVE patrika.com DOM (2026-07). The homepage
is a Next.js/MUI app in Hindi with highly dynamic content, so most helpers extract
data structurally (article URLs end in "-<digits>", section pages are "/<name>-news",
topic pages are "/topic/<slug>") rather than relying on volatile CSS class names.
"""

import re
from typing import Any, Dict, List
from playwright.async_api import Page
from pages.base_page import BasePage


class HomePage(BasePage):
    """Home page object containing selectors and page-specific methods."""

    # ---- Structural selectors ----
    HEADER_LOCATOR = "header"
    LOGO_LOCATOR = 'a[href="/"]'
    NAVIGATION_MENU_LOCATOR = "nav"
    CONTENT_LOCATOR = "main"
    # Header category links point at section listing pages ("/state-news", ...).
    HEADER_CATEGORY_LOCATOR = "header a[href$='-news'], header a[href='/opinion'], header a[href='/patrika-special']"
    # Trending / topic chips.
    TOPIC_LINK_LOCATOR = "a[href*='/topic/']"
    # Opinion module cards.
    OPINION_CARD_LOCATOR = "[class*='opinion-story-item']"
    # Horoscope module.
    HOROSCOPE_LINK_LOCATOR = "a[href*='horoscope'], a[href*='rashifal']"

    # Known Patrika categories — Hindi header labels + section slugs. Used to
    # validate that article category tags belong to a real section (TC-HP-07).
    KNOWN_CATEGORIES = {
        # Hindi labels
        "ताजा खबरें", "राज्य", "राष्ट्रीय", "बिजनेस", "मनोरंजन", "धर्म", "स्वास्थ्य",
        "खेल", "राजनीति", "विश्व", "विदेश", "शिक्षा", "ऑटोमोबाइल", "लाइफस्टाइल",
        "अपराध", "क्रिकेट", "फुटबॉल", "बॉलीवुड", "ओपिनियन", "पत्रिका स्पेशल",
        "जीवनशैली", "देश", "कारोबार",
        # Section slugs
        "state-news", "national-news", "business-news", "entertainment-news",
        "health-news", "sports-news", "political-news", "world-news",
        "education-news", "automobile-news", "lifestyle-news", "crime-news",
        "cricket-news", "football-news", "bollywood-news", "opinion",
        "astrology-and-spirituality", "dharma-karma", "horoscope-rashifal",
        "patrika-special",
    }

    def __init__(self, page: Page):
        """
        Initialize the Home Page object.

        Args:
            page: Playwright Page object
        """
        super().__init__(page)

    # ------------------------------------------------------------------ #
    # Navigation & load
    # ------------------------------------------------------------------ #
    async def navigate_to_home(self) -> None:
        """Navigate to the home page and wait for content to render."""
        await self.goto("/")
        await self.wait_for_page_load()

    async def wait_for_page_load(self) -> None:
        """Wait for the homepage DOM to be ready (the site never truly idles)."""
        try:
            await self.wait_for_load_state("domcontentloaded", timeout=20000)
        except Exception:
            pass

    async def scroll_full_page(self) -> None:
        """Scroll top-to-bottom to trigger lazy-loaded modules, then return to top."""
        await self.page.evaluate(
            """async () => {
                for (let y = 0; y < document.body.scrollHeight; y += 800) {
                    window.scrollTo(0, y);
                    await new Promise(r => setTimeout(r, 100));
                }
                window.scrollTo(0, 0);
            }"""
        )

    # ------------------------------------------------------------------ #
    # Basic visibility (kept for backward compatibility)
    # ------------------------------------------------------------------ #
    async def is_header_visible(self) -> bool:
        """Check if the header is visible."""
        return await self.is_visible(self.HEADER_LOCATOR)

    async def click_logo(self) -> None:
        """Click on the logo to navigate to home."""
        await self.click(self.LOGO_LOCATOR)

    async def get_header_text(self) -> str:
        """Get header text content."""
        return await self.get_text(self.HEADER_LOCATOR)

    async def is_navigation_visible(self) -> bool:
        """Check if navigation menu is visible."""
        return await self.is_visible(self.NAVIGATION_MENU_LOCATOR)

    async def is_content_visible(self) -> bool:
        """Check if main content area is visible."""
        return await self.is_visible(self.CONTENT_LOCATOR)

    # ------------------------------------------------------------------ #
    # TC-HP-01 : Hero / lead story block
    # ------------------------------------------------------------------ #
    async def get_hero_story(self) -> Dict[str, Any]:
        """
        Inspect the first prominent story card (image + headline + link).

        Returns:
            dict with keys: found, has_image, image_ok, headline, href
        """
        return await self.page.evaluate(
            """() => {
                const links = Array.from(document.querySelectorAll('a[href]'));
                // First article-style link (ends in -<digits>) that contains an image.
                const hero = links.find(a =>
                    /-\\d{5,}$/.test(a.getAttribute('href') || '') &&
                    a.querySelector('img'));
                if (!hero) return { found: false };
                const img = hero.querySelector('img');
                const headline = (hero.textContent || '').trim();
                return {
                    found: true,
                    has_image: !!img,
                    image_ok: !!img && img.naturalWidth > 0,
                    headline: headline.slice(0, 120),
                    href: hero.getAttribute('href'),
                };
            }"""
        )

    async def get_first_category_tag(self) -> str:
        """Return the text of the first visible category tag/badge, if any."""
        tags = await self.get_category_tags()
        return tags[0] if tags else ""

    # ------------------------------------------------------------------ #
    # TC-HP-02 / TC-HP-03 / TC-HP-08 : Article links
    # ------------------------------------------------------------------ #
    async def get_article_links(self) -> List[str]:
        """
        Return all homepage article URLs (hrefs ending in '-<digits>').

        Returns:
            De-duplicated list of article hrefs, in DOM order.
        """
        return await self.page.evaluate(
            """() => {
                const seen = new Set();
                const out = [];
                document.querySelectorAll('a[href]').forEach(a => {
                    const h = a.getAttribute('href') || '';
                    if (/-\\d{5,}$/.test(h) && !seen.has(h)) { seen.add(h); out.push(h); }
                });
                return out;
            }"""
        )

    async def get_headline_count(self) -> int:
        """Return the number of distinct article headlines on the homepage."""
        return len(await self.get_article_links())

    async def get_all_article_links_with_dupes(self) -> List[str]:
        """Return article hrefs INCLUDING duplicates (for uniqueness checks)."""
        return await self.page.evaluate(
            """() => Array.from(document.querySelectorAll('a[href]'))
                .map(a => a.getAttribute('href') || '')
                .filter(h => /-\\d{5,}$/.test(h))"""
        )

    async def find_duplicate_article_urls(self) -> List[str]:
        """Return article hrefs that appear more than once in the same page."""
        all_links = await self.get_all_article_links_with_dupes()
        seen, dupes = set(), set()
        for h in all_links:
            if h in seen:
                dupes.add(h)
            seen.add(h)
        return list(dupes)

    async def find_duplicate_article_urls_within_blocks(self) -> List[str]:
        """
        Return article hrefs that repeat WITHIN the same content block/module.

        A news homepage legitimately surfaces the same story in different modules
        (e.g. Trending and its section), so cross-block repeats are allowed. This
        only flags a story duplicated inside a single block — the real defect
        described by TC-HP-08 ("same lead story twice in the same block").
        """
        return await self.page.evaluate(
            """() => {
                const BLOCK = "section, [class*='section' i], [class*='block' i], "
                            + "[class*='widget' i], [class*='story-list' i]";
                const groups = new Map();
                document.querySelectorAll('a[href]').forEach(a => {
                    const h = a.getAttribute('href') || '';
                    if (!/-\\d{5,}$/.test(h)) return;
                    const block = a.closest(BLOCK) || document.body;
                    if (!groups.has(block)) groups.set(block, []);
                    groups.get(block).push(h);
                });
                const dupes = new Set();
                for (const hrefs of groups.values()) {
                    const seen = new Set();
                    for (const h of hrefs) {
                        if (seen.has(h)) dupes.add(h);
                        seen.add(h);
                    }
                }
                return Array.from(dupes);
            }"""
        )

    async def check_url_status(self, url: str) -> int:
        """
        Resolve a (possibly relative) URL and return its HTTP status code.

        Uses the browser context's request API so cookies/base URL apply and no
        full page render is needed.
        """
        try:
            response = await self.page.context.request.get(url, timeout=15000)
            return response.status
        except Exception:
            return 0

    # ------------------------------------------------------------------ #
    # TC-HP-04 / TC-HP-11 : Widgets & category modules
    # ------------------------------------------------------------------ #
    async def get_topic_links(self) -> List[Dict[str, str]]:
        """Return trending topic chips (text + href) pointing at /topic/ pages."""
        return await self.page.evaluate(
            """() => {
                const seen = new Set();
                const out = [];
                document.querySelectorAll("a[href*='/topic/']").forEach(a => {
                    const h = a.getAttribute('href');
                    if (h && !seen.has(h)) {
                        seen.add(h);
                        out.push({ text: (a.textContent || '').trim().slice(0, 40), href: h });
                    }
                });
                return out;
            }"""
        )

    async def has_opinion_section(self) -> bool:
        """Check whether the Opinion module rendered with at least one card."""
        count = await self.page.locator(self.OPINION_CARD_LOCATOR).count()
        return count > 0

    async def get_opinion_card_count(self) -> int:
        """Return the number of Opinion story cards."""
        return await self.page.locator(self.OPINION_CARD_LOCATOR).count()

    async def get_section_listing_links(self) -> List[str]:
        """Return distinct section/listing links ('/<name>-news', '/opinion', ...)."""
        return await self.page.evaluate(
            """() => {
                const seen = new Set();
                document.querySelectorAll('a[href]').forEach(a => {
                    const h = a.getAttribute('href') || '';
                    if (/^\\/[a-z-]+-news$/.test(h) ||
                        /^\\/(opinion|horoscope-rashifal|dharma-karma|astrology-and-spirituality|patrika-special)$/.test(h))
                        seen.add(h);
                });
                return Array.from(seen);
            }"""
        )

    # ------------------------------------------------------------------ #
    # TC-HP-05 : Image alt attributes
    # ------------------------------------------------------------------ #
    async def get_image_alt_report(self) -> Dict[str, Any]:
        """
        Audit alt attributes on content images.

        Returns:
            dict: total, with_alt, without_alt, missing (list of src fragments)
        """
        return await self.page.evaluate(
            """() => {
                const imgs = Array.from(document.querySelectorAll('main img, img'));
                const missing = [];
                let withAlt = 0;
                imgs.forEach(i => {
                    const alt = (i.getAttribute('alt') || '').trim();
                    if (alt) withAlt++;
                    else missing.push((i.getAttribute('src') || i.getAttribute('data-src') || '').slice(-40));
                });
                return {
                    total: imgs.length,
                    with_alt: withAlt,
                    without_alt: imgs.length - withAlt,
                    missing: missing.slice(0, 10),
                };
            }"""
        )

    # ------------------------------------------------------------------ #
    # TC-HP-06 : Timestamps
    # ------------------------------------------------------------------ #
    async def get_timestamp_texts(self) -> List[str]:
        """Return candidate timestamp strings found on the homepage."""
        return await self.page.evaluate(
            """() => {
                const els = Array.from(document.querySelectorAll(
                    "time, [class*='time'], [class*='date'], [class*='publish']"));
                const seen = new Set();
                els.forEach(e => {
                    const t = (e.textContent || '').trim();
                    if (t && t.length < 60) seen.add(t);
                });
                return Array.from(seen).slice(0, 40);
            }"""
        )

    @staticmethod
    def is_valid_timestamp(text: str) -> bool:
        """
        Validate a timestamp string against Patrika's formats:
          - Hindi date e.g. "16 जुलाई 2026" (optionally with weekday)
          - Relative English e.g. "10 Minutes Ago" / "2 Hours Ago"
          - Relative Hindi e.g. "10 मिनट पहले" / "2 घंटे पहले"
        """
        if not text:
            return False
        hindi_months = ("जनवरी|फरवरी|मार्च|अप्रैल|मई|जून|जुलाई|अगस्त|सितंबर|"
                        "अक्टूबर|नवंबर|दिसंबर")
        patterns = [
            rf"\d{{1,2}}\s*(?:{hindi_months})\s*\d{{4}}",          # 16 जुलाई 2026
            r"\d+\s*(?:Minute|Minutes|Hour|Hours|Day|Days)\s*Ago",  # 10 Minutes Ago
            r"\d+\s*(?:मिनट|घंटे|घंटा|दिन)\s*पहले",                  # 10 मिनट पहले
        ]
        return any(re.search(p, text, re.IGNORECASE) for p in patterns)

    # ------------------------------------------------------------------ #
    # TC-HP-07 : Category tags
    # ------------------------------------------------------------------ #
    async def get_category_tags(self) -> List[str]:
        """Return short category/tag/badge label texts from story cards."""
        return await self.page.evaluate(
            """() => {
                const els = Array.from(document.querySelectorAll(
                    "[class*='category' i], [class*='tag' i], [class*='badge' i], [class*='label' i]"));
                const seen = new Set();
                els.forEach(e => {
                    const t = (e.textContent || '').trim();
                    if (t && t.length > 0 && t.length < 25) seen.add(t);
                });
                return Array.from(seen).slice(0, 50);
            }"""
        )

    def known_category_matches(self, tags: List[str]) -> List[str]:
        """Return the subset of tags that belong to the known category list."""
        return [t for t in tags if t in self.KNOWN_CATEGORIES]

    # ------------------------------------------------------------------ #
    # TC-HP-09 : Auto-refresh / background network activity
    # ------------------------------------------------------------------ #
    async def count_network_requests(self, observe_seconds: float = 4.0) -> int:
        """
        Count XHR/fetch requests fired over an observation window WITHOUT reloading.

        Returns:
            Number of XHR/fetch requests observed.
        """
        import asyncio

        requests: List[str] = []

        def _on_request(req):
            if req.resource_type in ("xhr", "fetch"):
                requests.append(req.url)

        self.page.on("request", _on_request)
        start_url = self.page.url
        await asyncio.sleep(observe_seconds)
        self.page.remove_listener("request", _on_request)
        # Confirm no full navigation happened during observation.
        self.last_observation_navigated = self.page.url != start_url
        return len(requests)

    # ------------------------------------------------------------------ #
    # TC-HP-10 : Horoscope module
    # ------------------------------------------------------------------ #
    async def get_horoscope_links(self) -> List[str]:
        """Return distinct horoscope/rashifal links present on the homepage."""
        return await self.page.evaluate(
            """() => {
                const seen = new Set();
                document.querySelectorAll("a[href*='horoscope'], a[href*='rashifal']").forEach(a => {
                    const h = a.getAttribute('href');
                    if (h) seen.add(h);
                });
                return Array.from(seen);
            }"""
        )

    async def has_horoscope_module(self) -> bool:
        """Check whether a horoscope/rashifal module/link is present."""
        return len(await self.get_horoscope_links()) > 0

    # ------------------------------------------------------------------ #
    # TC-HP-12 / TC-HP-13 : Section & header-category navigation
    # ------------------------------------------------------------------ #
    async def get_header_category_links(self) -> List[Dict[str, str]]:
        """Return header category links (Hindi label + href)."""
        return await self.page.evaluate(
            """() => {
                const anchors = Array.from(document.querySelectorAll('a[href]'));
                const seen = new Set();
                const out = [];
                anchors.forEach(a => {
                    const h = a.getAttribute('href') || '';
                    const t = (a.textContent || '').trim();
                    if (/^\\/[a-z-]+-news$/.test(h) && t && !seen.has(h)) {
                        seen.add(h);
                        out.push({ text: t.slice(0, 30), href: h });
                    }
                });
                return out;
            }"""
        )

    async def click_category_and_wait(self, href: str) -> str:
        """
        Click a category/section link by its href and wait for navigation.

        Args:
            href: The href of the category link to click (e.g. '/national-news').

        Returns:
            The resulting page URL after navigation.
        """
        await self.page.click(f"a[href='{href}']")
        try:
            await self.page.wait_for_url(f"**{href}", timeout=15000)
        except Exception:
            await self.wait_for_load_state("domcontentloaded", timeout=15000)
        return self.page.url
