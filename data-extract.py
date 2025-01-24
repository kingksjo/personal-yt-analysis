import pandas as pd
from bs4 import BeautifulSoup

# Step 1: Load and parse the HTML file
with open(r"Takeout/YouTube and YouTube Music/history/watch-history.html", "r", encoding="utf-8") as file:
    html_content = file.read()
print("Read")
soup = BeautifulSoup(html_content, "lxml")
print("Parsed")
# Step 2: Find all relevant divs
divs = soup.find_all("div", class_="outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp")

# Step 3: Initialize a list to store the extracted data
data = []

# Step 4: Iterate over divs and extract data
for div in divs:
    # Extract service (YouTube or YouTube Music)
    service_tag = div.find("p", class_="mdl-typography--title")
    service = service_tag.text.strip().replace("<br>", "").strip() if service_tag else None

    # Extract title and its link
    title_link = div.find("a", href=lambda href: href and "watch?v=" in href)
    title = title_link.text.strip() if title_link else None
    title_url = title_link["href"] if title_link else None

    # Extract channel name or identify Ads
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

    # Extract date watched
    date_tag = div.find("div", class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1")
    if date_tag:
        date_watched = date_tag.text.split("\n")[-1].strip()
    else:
        date_watched = None

    # Combine all relevant links
    links = [url for url in [title_url] if url]

    # Append to data list
    data.append({
        "service": service,
        "title": title,
        "channel": channel,
        "date_watched": date_watched,
        "links": links
    })

# Step 5: Convert to DataFrame and save as CSV
df = pd.DataFrame(data)
df.to_csv("watch_history.csv", index=False)

print("Data extraction complete! CSV saved as 'watch_history.csv'")
