import json
from playwright.sync_api import sync_playwright

URLS = {
    "home": "https://wheedletechnologies.ai",
    "about": "https://wheedletechnologies.ai/about-us",
    "career": "https://wheedletechnologies.ai/career",
    "blog": "https://wheedletechnologies.ai/blog",
    "services": {
        "AI Web Engineering Agents": "https://wheedletechnologies.ai/our-service/ai-web-engineering-agents",
        "AI App Development Agent": "https://wheedletechnologies.ai/our-service/ai-app-development-agent",
        "Autonomous Digital Marketing Agents": "https://wheedletechnologies.ai/our-service/autonomous-digital-marketing-agents",
        "Software Development Agentic Platform": "https://wheedletechnologies.ai/our-service/software-development-agentic-platform",
        "Autonomous UI/UX Design Intelligence": "https://wheedletechnologies.ai/our-service/autonomous-ui-ux-design-intelligence",
        "AI Graphic Design Automation Agent": "https://wheedletechnologies.ai/our-service/ai-graphic-design-automation-agent",
        "Autonomous IT Consulting & Advisory Agent": "https://wheedletechnologies.ai/our-service/autonomous-it-consulting-and-advisory-agent",
        "AI Solutions & Intelligent Automation": "https://wheedletechnologies.ai/our-service/ai-solutions-and-intelligent-automation"
    }
}

def extract_text(page, url):
    print("Scraping:", url)

    try:
        # 🔥 fastest + most stable
        page.goto(url, timeout=60000)
    except:
        print("⚠ Load issue, continuing anyway...")

    # wait manually (DON’T depend on networkidle)
    page.wait_for_timeout(7000)

    # scroll to load content
    for _ in range(6):
        page.mouse.wheel(0, 1500)
        page.wait_for_timeout(1000)

    try:
        content = page.inner_text("body")
    except:
        return "Content not available"

    lines = content.split("\n")
    clean = []

    for line in lines:
        line = line.strip()

        if (
            len(line) > 50
            and "cookie" not in line.lower()
            and "privacy" not in line.lower()
            and "welcome to" not in line.lower()
            and "wheedletechnologies" not in line.lower()
        ):
            clean.append(line)

    return "\n\n".join(list(dict.fromkeys(clean))[:40])


def scrape_website():
    data = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # normal pages
        for key in ["home", "about", "career", "blog"]:
            try:
                data[key] = extract_text(page, URLS[key])
            except Exception as e:
                print("❌ Failed:", key, e)
                data[key] = "Content not available"

        # services
        data["services"] = {}
        for name, url in URLS["services"].items():
            try:
                data["services"][name] = extract_text(page, url)
            except Exception as e:
                print("❌ Failed service:", name, e)
                data["services"][name] = "Content not available"

        browser.close()

    return data


if __name__ == "__main__":
    website_data = scrape_website()

    with open("website_data.json", "w", encoding="utf-8") as f:
        json.dump(website_data, f, indent=2, ensure_ascii=False)

    print("✅ DONE — data stored")