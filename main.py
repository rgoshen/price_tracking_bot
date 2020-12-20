import requests
import lxml
from bs4 import BeautifulSoup
import smtplib

BUY_PRICE = 200
MY_EMAIL = "novusterra6@gmail.com"
MY_PASSWORD = "pflyers88"
EMAIL_SERVER = "smtp.gmail.com"
PORT = 587

product_url = "https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B07W55DDFB/ref=sr_1_1?qid=1597662463"

amazon_headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

# get amazon price
response = requests.get(url=product_url, headers=amazon_headers)

soup = BeautifulSoup(response.content, "lxml")

price = soup.find(id="priceblock_ourprice").get_text()
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)
print(price_as_float)

title = soup.find(id="productTitle").get_text().strip()
print(title)

# compare amazon price to target price and send email when amazon price is below target price
if price_as_float < BUY_PRICE:
    message = f"{title} is now {price}"

    with smtplib.SMTP(EMAIL_SERVER, PORT) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n{message.encode('utf-8')}\n{product_url}"
        )
