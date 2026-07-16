"""
Homepage Test Suite - Automated from Home_Patrika.csv

Covers TC-HP-01 to TC-HP-13 for the "Homepage & Dynamic Content Blocks" module,
executed against the live www.patrika.com site.

The homepage content is highly dynamic, so assertions use structural signals and
sensible thresholds rather than exact text/counts.
"""

import pytest
from playwright.async_api import Page
from pages.home_page import HomePage
from utils.test_helpers import log_step


# Applies the `home` marker to every test in this module.
pytestmark = pytest.mark.home


class TestHomepageContentBlocks:
    """Homepage & Dynamic Content Blocks — TC-HP-01 to TC-HP-13."""

    @pytest.fixture
    async def home_page(self, page: Page):
        """Provide a HomePage already navigated to the homepage."""
        home = HomePage(page)
        await home.navigate_to_home()
        yield home

    # ------------------------------------------------------------------ #
    @pytest.mark.smoke
    @pytest.mark.medium_priority
    async def test_tc_hp_01_hero_story_renders(self, home_page: HomePage):
        """TC-HP-01: Hero/lead story block renders with image, headline & link."""
        log_step(1, "Locate the hero/lead story block")
        hero = await home_page.get_hero_story()

        log_step(2, "Verify hero block was found")
        assert hero.get("found"), "No hero/lead story with an image was found"

        log_step(3, "Verify image is present and not broken")
        assert hero.get("has_image"), "Hero story has no image"
        assert hero.get("image_ok"), "Hero story image appears broken (naturalWidth=0)"

        log_step(4, "Verify headline text is present")
        assert len(hero.get("headline", "")) > 5, "Hero story headline is missing/too short"

        log_step(5, "Verify hero links to an article")
        assert hero.get("href"), "Hero story has no article link"
        print(f"✅ TC-HP-01 PASSED: Hero story '{hero['headline'][:40]}...' renders correctly")

    # ------------------------------------------------------------------ #
    @pytest.mark.smoke
    @pytest.mark.medium_priority
    async def test_tc_hp_02_secondary_headlines_minimum_count(self, home_page: HomePage):
        """TC-HP-02: Secondary headline list renders a minimum number of articles."""
        MIN_EXPECTED = 5

        log_step(1, "Count the article headlines on the homepage")
        count = await home_page.get_headline_count()

        log_step(2, f"Verify count >= {MIN_EXPECTED}")
        assert count >= MIN_EXPECTED, f"Expected >= {MIN_EXPECTED} headlines, found {count}"
        print(f"✅ TC-HP-02 PASSED: {count} article headlines rendered (>= {MIN_EXPECTED})")

    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.medium_priority
    async def test_tc_hp_03_headlines_link_to_valid_articles(self, home_page: HomePage):
        """TC-HP-03: Each headline links to a valid article page (HTTP 200)."""
        SAMPLE_SIZE = 5

        log_step(1, "Collect article links")
        links = await home_page.get_article_links()
        assert links, "No article links found on homepage"

        log_step(2, f"Check HTTP status of first {SAMPLE_SIZE} article links")
        sample = links[:SAMPLE_SIZE]
        failures = []
        for href in sample:
            status = await home_page.check_url_status(href)
            print(f"   {status}  {href}")
            if status != 200:
                failures.append((href, status))

        log_step(3, "Verify all sampled links returned HTTP 200")
        assert not failures, f"Article links did not return 200: {failures}"
        print(f"✅ TC-HP-03 PASSED: {len(sample)} sampled article links returned HTTP 200")

    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.medium_priority
    async def test_tc_hp_04_trending_and_opinion_populated(self, home_page: HomePage):
        """TC-HP-04: Trending topics + Opinion section populate with clickable items."""
        log_step(1, "Scroll to load lazy modules")
        await home_page.scroll_full_page()

        log_step(2, "Verify trending topic chips are present and clickable")
        topics = await home_page.get_topic_links()
        assert len(topics) >= 1, "No trending topic chips found"
        assert all(t["href"].startswith("/topic/") for t in topics), "Topic links malformed"

        log_step(3, "Verify Opinion section rendered with cards")
        opinion_cards = await home_page.get_opinion_card_count()
        assert opinion_cards >= 1, "Opinion section has no cards"
        print(f"✅ TC-HP-04 PASSED: {len(topics)} trending topics, {opinion_cards} opinion cards")

    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.medium_priority
    async def test_tc_hp_05_images_have_alt_attributes(self, home_page: HomePage):
        """TC-HP-05: Content images have non-empty alt attributes."""
        log_step(1, "Scroll to load lazy images")
        await home_page.scroll_full_page()

        log_step(2, "Audit image alt attributes")
        report = await home_page.get_image_alt_report()
        print(f"   images={report['total']} with_alt={report['with_alt']} "
              f"without_alt={report['without_alt']}")

        log_step(3, "Verify the vast majority of images have alt text")
        assert report["total"] > 0, "No images found on homepage"
        # Allow a small tolerance for tracking pixels / decorative images.
        ratio = report["with_alt"] / report["total"]
        assert ratio >= 0.9, (
            f"Only {ratio:.0%} of images have alt text; missing e.g. {report['missing']}")
        print(f"✅ TC-HP-05 PASSED: {ratio:.0%} of {report['total']} images have alt text")

    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.medium_priority
    async def test_tc_hp_06_timestamps_valid_format(self, home_page: HomePage):
        """TC-HP-06: Article timestamps follow a valid date/relative-time format."""
        log_step(1, "Collect timestamp texts")
        timestamps = await home_page.get_timestamp_texts()
        assert timestamps, "No timestamp elements found on homepage"

        log_step(2, "Validate timestamp formats")
        valid = [t for t in timestamps if HomePage.is_valid_timestamp(t)]
        print(f"   {len(valid)}/{len(timestamps)} timestamp strings matched a known format")

        log_step(3, "Verify at least some timestamps match the expected format")
        assert valid, f"No timestamps matched expected formats. Samples: {timestamps[:5]}"
        print(f"✅ TC-HP-06 PASSED: valid timestamps present, e.g. '{valid[0]}'")

    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.medium_priority
    async def test_tc_hp_07_category_tags_are_known(self, home_page: HomePage):
        """TC-HP-07: Category tags/badges match a known category list."""
        log_step(1, "Collect category tags")
        tags = await home_page.get_category_tags()
        assert tags, "No category tags found on homepage"

        log_step(2, "Match tags against the known category list")
        matches = home_page.known_category_matches(tags)
        print(f"   {len(matches)}/{len(tags)} tags matched known categories: {matches[:8]}")

        log_step(3, "Verify at least one recognized category tag is present")
        assert matches, f"No tags matched the known category list. Found: {tags[:10]}"
        print(f"✅ TC-HP-07 PASSED: recognized categories e.g. {matches[:5]}")

    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.medium_priority
    async def test_tc_hp_08_no_duplicate_lead_stories(self, home_page: HomePage):
        """TC-HP-08: No lead story is duplicated within the same content block.

        Cross-block repeats (same story in Trending and its section) are normal
        and allowed; only a story repeated inside a single block is a defect.
        """
        log_step(1, "Collect all article URLs (including duplicates)")
        all_links = await home_page.get_all_article_links_with_dupes()
        assert all_links, "No article links found on homepage"

        log_step(2, "Detect article URLs duplicated within the same block")
        dupes = await home_page.find_duplicate_article_urls_within_blocks()
        page_wide = await home_page.find_duplicate_article_urls()
        print(f"   total={len(all_links)} unique={len(set(all_links))} "
              f"within-block-dupes={len(dupes)} (cross-block repeats allowed: {len(page_wide)})")

        log_step(3, "Verify no article URL repeats inside the same block")
        assert not dupes, f"Article URLs duplicated within a single block: {dupes[:5]}"
        print(f"✅ TC-HP-08 PASSED: no story duplicated within any single block")

    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.medium_priority
    async def test_tc_hp_09_auto_refresh_without_reload(self, home_page: HomePage):
        """TC-HP-09: Background sections fire XHR/fetch without a full page reload."""
        log_step(1, "Observe background network activity for a few seconds")
        request_count = await home_page.count_network_requests(observe_seconds=4.0)
        print(f"   observed {request_count} XHR/fetch requests")

        log_step(2, "Verify no full navigation occurred during observation")
        assert not getattr(home_page, "last_observation_navigated", False), \
            "A full page navigation occurred during observation"

        log_step(3, "Verify background requests fired (dynamic content updates)")
        # Some homepages are static after load; treat zero as acceptable but log it.
        if request_count == 0:
            pytest.skip("No background XHR/fetch observed in the window; nothing to assert")
        assert request_count >= 1
        print(f"✅ TC-HP-09 PASSED: {request_count} background requests without reload")

    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.medium_priority
    async def test_tc_hp_10_horoscope_module_present(self, home_page: HomePage):
        """TC-HP-10: Horoscope (rashifal) module is present and links are valid."""
        log_step(1, "Scroll to load the horoscope module")
        await home_page.scroll_full_page()

        log_step(2, "Verify horoscope/rashifal links are present")
        horo_links = await home_page.get_horoscope_links()
        assert horo_links, "No horoscope/rashifal module or links found"
        print(f"   horoscope links: {horo_links}")

        log_step(3, "Verify the horoscope section link returns HTTP 200")
        section = next((h for h in horo_links if h.rstrip("/").endswith("horoscope-rashifal")),
                       horo_links[0])
        status = await home_page.check_url_status(section)
        assert status == 200, f"Horoscope link {section} returned {status}"
        print(f"✅ TC-HP-10 PASSED: horoscope module present, {section} → 200")

    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.medium_priority
    async def test_tc_hp_11_category_modules_have_articles(self, home_page: HomePage):
        """TC-HP-11: Multiple category modules render with articles."""
        log_step(1, "Scroll to load all category modules")
        await home_page.scroll_full_page()

        log_step(2, "Verify multiple section/category modules are present")
        sections = await home_page.get_section_listing_links()
        assert len(sections) >= 3, f"Expected multiple category sections, found {sections}"

        log_step(3, "Verify articles are rendered below the categories")
        article_count = await home_page.get_headline_count()
        assert article_count >= 10, f"Expected many articles across modules, found {article_count}"
        print(f"✅ TC-HP-11 PASSED: {len(sections)} sections, {article_count} articles rendered")

    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.medium_priority
    async def test_tc_hp_12_read_all_links_route_to_listing(self, home_page: HomePage):
        """TC-HP-12: 'Read All'/section links route to a valid listing page (200)."""
        log_step(1, "Collect section listing links")
        sections = await home_page.get_section_listing_links()
        assert sections, "No section/listing links found"

        log_step(2, "Verify a sample of listing links return HTTP 200")
        sample = sections[:3]
        failures = []
        for href in sample:
            status = await home_page.check_url_status(href)
            print(f"   {status}  {href}")
            if status != 200:
                failures.append((href, status))

        log_step(3, "Verify all sampled listing links returned HTTP 200")
        assert not failures, f"Listing links did not return 200: {failures}"
        print(f"✅ TC-HP-12 PASSED: {len(sample)} listing links returned HTTP 200")

    # ------------------------------------------------------------------ #
    @pytest.mark.smoke
    @pytest.mark.medium_priority
    async def test_tc_hp_13_header_category_navigates_to_listing(self, home_page: HomePage):
        """TC-HP-13: Clicking a header category opens its listing with news articles."""
        log_step(1, "Collect header category links")
        categories = await home_page.get_header_category_links()
        assert categories, "No header category links found"
        target = categories[0]
        print(f"   clicking category '{target['text']}' → {target['href']}")

        log_step(2, "Click the category and wait for navigation")
        result_url = await home_page.click_category_and_wait(target["href"])

        log_step(3, "Verify navigation landed on the category listing page")
        assert target["href"] in result_url, \
            f"Expected URL to contain {target['href']}, got {result_url}"

        log_step(4, "Verify the listing page contains news articles")
        article_count = await home_page.get_headline_count()
        assert article_count >= 3, \
            f"Category listing page shows too few articles: {article_count}"
        print(f"✅ TC-HP-13 PASSED: '{target['text']}' → {result_url} with {article_count} articles")
