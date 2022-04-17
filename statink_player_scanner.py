import requests
from bs4 import BeautifulSoup
import sys

account = "@YOUR_STATINK_ACCOUNT"
name_list = ["hoge","fuga","ほげ","ふが"]
ignore_list = ["foo","bar","フー","バー"]
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
        
        tds = soup.select("td.col-name > div > span > a")
        tds = tds + soup.select("td.col-name > div > span > span")

        players_temp=[]
        for player in tds:
            try:
                player_dict={"name":"","id":"","url":""}
                player_dict["name"] = player.get_text().strip()
                player_dict["id"] = player.find("img", alt="").get("title")
                player_dict["url"] = main_url + "/" + account + "/spl2?filter%5Bfilter%5D=with%3A" + player_dict["id"].replace("ID: ","")
                if len(player_dict["name"]) > 0 :
                    # print(i, player.get_text().strip())
                    players_temp.append(player_dict)
            except:
                pass
            
        for player in players_temp: # 部分一致
            for name in name_list:
                if name in player["name"] and not player["name"] in ignore_list:
                    print(i, name, ">", player["name"], url)
                    rep = input("\n[?] 探しているのはこの人？[Y:終了,N:除外リスト入り,S:skip]：")
                    if rep == "Y" or rep == "y":
                       print("[+] 終了")
                       print("\t", player["name"])
                       print("\t", player["url"])
                       sys.exit()
                    elif rep == "N" or rep == "n":
                       ignore_list.append(player["name"])
                       print("[+] 除外リストに追加\n",ignore_list)
                    elif rep == "S" or rep == "s":
                       print("[+] Skip")

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
    
