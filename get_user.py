import requests
import time

USER_AGENT = "Strange_Buffalo_7001"
headers = {"User-Agent": USER_AGENT}

def save(data):
    usernames = data 
    with open("users.txt", "a", encoding="utf-8") as f:
        for u in usernames:
            f.write(u + "\n")
    print(f"Saved {len(usernames)} usernames to users.txt")

def fetch_users(subreddit="all", max_users=1000):
    number_user_get = 0
    dicts = {}
    users = set()
    after = None
    url = f"https://www.reddit.com/r/{subreddit}/new.json"

    while number_user_get < max_users:
        params = {"limit": 100}
        if after:
            params["after"] = after

        try:
            r = requests.get(url, headers=headers, params=params)
        except:
            continue
        if r.status_code != 200:
            print("Lỗi:", r.status_code, r.text)
            save(list(users))
            users = set()
            time.sleep(120)
            continue

        data = r.json()["data"]
        children = data["children"]

        for child in children:
            author = child["data"]["author"]
            if author not in ("[deleted]", "AutoModerator") and author not in dicts:  
                users.add(author)
                dicts[author] = 1
                number_user_get += 1

        # after = data.get("after")
        # if not after:  
        #     break

        print(f"Got {number_user_get} users...")
        time.sleep(1)  

    save(list(users))

if __name__ == "__main__":
    fetch_users(max_users=10000)
    
