import requests
from bs4 import BeautifulSoup
import sys

account = "@YOUR_STATINK_ACCOUNT"
name_list = ["hoge","fuga","ほげ","ふが"]
ignore_list = []
main_url = "https://stat.ink"


def get_sub_url():
    url = main_url + "/" + account + "/spl2"
    res = requests.get(url)
    
    soup = BeautifulSoup(res.text, "html.parser")
    a = soup.find("a" , class_="btn btn-primary btn-xs")
    
    if account in a.get("href"):
        print(url)
        return a.get("href")
    else:
        sys.exit()

    
def scan_name(name_list, sub_url):
    i = 1
   #  while i < 30:
    while True:
        url = main_url + sub_url
        res = requests.get(url)

        soup = BeautifulSoup(res.text, "html.parser")
        a = soup.find("a" , class_="btn btn-default")

        trs = soup.find_all("td", class_="col-name")
        players=[]
        for player in trs:
            players.append(player.text.strip())

        for name in name_list:
            for player in players: # 部分一致
                if name in player:
                    if not player in ignore_list:
                        print(i, name, ">", player, url)
                        rep = input("[?] 探しているのはこの人？[Y:終了, N:除外リスト入り, S:skip]：")
                        if rep == "Y" or rep == "y":
                           print("[+] 終了")
                           sys.exit()
                        elif rep == "N" or rep == "n":
                           ignore_list.append(player)
                           print("[+] 除外リストに追加", ignore_list)
                        elif rep == "S" or rep == "s":
                           print("[+] Skip")
               
            # if name in players: # 完全一致
            #     print(i, name, ">",player, url)

        if i% 100 == 0:
            print("*", end="")
        if i% 1000 == 0:
            print(" ", url)
        if not a.text=="Prev. Battle" or a.text=="次のバトル":
            print(" 最終ページ ", sub_url, a.text)
            break

        i = i + 1
        sub_url = a.get("href")
        

def main():
    # sub_url = "/@tm_ink2/spl2/4518781"
    sub_url = get_sub_url()
    scan_name(name_list, sub_url)


if __name__ == "__main__":
    main()
    
