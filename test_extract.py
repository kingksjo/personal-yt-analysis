import pandas as pd
import re
from bs4 import BeautifulSoup

# Step 1: Load the HTML file in chunks (if needed)
with open(r"Takeout/YouTube and YouTube Music/history/watch-history.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "lxml")
print("Loaded")
# Step 2: Initialize data list
data = []

# Step 3: Restrict parsing to relevant divs
for div in soup.find_all("div", class_="outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp"):
    # Extract Service (YouTube or YouTube Music)
    service_tag = div.find("p", class_="mdl-typography--title")
    service = service_tag.text.strip().replace("<br>", "") if service_tag else None

    # Extract Title and its Link
    title_link = div.find("a", href=lambda href: href and "watch?v=" in href)
    title = title_link.text.strip() if title_link else None
    title_url = title_link["href"] if title_link else None

    # Extract Channel or Detect Ads
    channel_link = div.find("a", href=lambda href: href and "channel/" in href)
    if channel_link:
        channel = channel_link.text.strip()
        channel_url = channel_link["href"]
    elif "From Google Ads" in div.text:
        channel = "Ads"
        channel_url = None
    else:
        channel = None
        channel_url = None

    # Extract Date Watched
    date_tag = div.find("div", class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1")
    if date_tag:
        # Use a regular expression to match the date and time format
        match = re.search(r'\b\w{3,9} \d{1,2}, \d{4}, \d{1,2}:\d{2}:\d{2}(?: AM| PM)?', date_tag.text)
        date_watched = match.group(0) if match else None
    else:
        date_watched = None


    # Combine Links
    links = [url for url in [title_url] if url]

    # Append row to data
    data.append({
        "service": service,
        "title": title,
        "channel": channel,
        "date_watched": date_watched,
        "links": links
    })

# Step 4: Convert to DataFrame
df = pd.DataFrame(data)

# Step 5: Save to CSV
df.to_csv("youtube_watch_history.csv", index=False)
print("Parsing completed! Data saved as 'youtube_watch_history.csv'")
