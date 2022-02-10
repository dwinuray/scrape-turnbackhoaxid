from bs4 import BeautifulSoup
import requests, re
import pandas as pd


halaman = "https://turnbackhoax.id/"
tag = "covid-19"
pagination = 3

data = []

id = []
username = []
text = []
created_at = []

num = 1
for page in range(0, pagination):

    if page == 0:
        url = f"{halaman}tag/{tag}/"
    else:
        url = f"{halaman}tag/{tag}/page/{str(page + 1)}/"

    main = requests.get(url)
    soup = BeautifulSoup(main.content, "html.parser")

    contents = soup.find('div', class_='mh-loop mh-content')
    quotes = contents.find_all('article')

    # ------------------
    for q in quotes:
        # Header
        article = q.find('header', class_="mh-loop-header")

        title = article.find('a').text
        date = article.find('span', class_="mh-meta-date updated").text
        author = article.find('span', class_="mh-meta-author author vcard").text

        # data.append(title)

        cln = re.sub("\s+", ' ', title)
        split = cln.split(']')

        title = split[1]
        label = split[0].split("[")[1]

        if label == "SALAH":
            label = "false"
        else:
            label = "true"


        id.append(num)
        username.append(author)
        text.append(title)
        created_at.append(date)

        #increment id
        num += 1

dataFrame = pd.DataFrame({
    'id': id,
    'username': username,
    'dibuat_pada': created_at,
    'tweet': text
})

dataFrame.to_excel('hasil-crawling.xlsx', index=False)