import re
import json
import requests
import pandas as pd

url = "https://shopee.vn/M%C3%A1y-T%C3%ADnh-Casio-FX-580VNX-Ch%C3%ADnh-H%C3%A3ng-Nh%E1%BA%ADp-Kh%E1%BA%A9u-Th%C3%A1i-Lan-521-T%C3%ADnh-N%C4%83ng-C%C3%B3-Th%E1%BB%83-Chuy%E1%BB%83n-%C4%90%E1%BB%95i-Ti%E1%BA%BFng-Vi%E1%BB%87t-TEZY-i.60242569.7365993114?sp_atk=69d40b91-f5c7-476e-b8d6-42f08c26b0e3&xptdk=69d40b91-f5c7-476e-b8d6-42f08c26b0e3"

r = re.search(r"i\.(\d+)\.(\d+)", url)
shop_id, item_id = r[1], r[2]
ratings_url = "https://shopee.vn/api/v2/item/get_ratings?filter=0&flag=1&itemid={item_id}&limit=20&offset={offset}&shopid={shop_id}&type=0"

offset = 0
d = {"rating": [], "comment": []}
while True:
    response = requests.get(ratings_url.format(shop_id=shop_id, item_id=item_id, offset=offset))
    data = response.json()

    if response.status_code != 200 or data is None or "ratings" not in data.get("data", {}):
        print("Failed to fetch ratings data. Check the API or URL parameters.")
        break

    ratings = data["data"]["ratings"]
    if not ratings:
        break

    for rating in ratings:
        if rating.get("comment"):
            d["rating"].append(rating["rating_star"])
            d["comment"].append(rating["comment"])

    if len(ratings) < 20:
        break

    offset += 20

df = pd.DataFrame(d)
print(df)
df.to_csv("data_5.csv", index=False)
