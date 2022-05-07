import requests
from bs4 import BeautifulSoup
import sys

account = "@tm_ink2"
my_weapon = "Bloblobber"

ignore_list = [""]
main_url = "https://stat.ink"
marumisa_list = []


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
        
    
def scan_sp(sub_url):
    i = 1
    ka_max = 0
    kill_max = 0
    assist_max = 0
    death_max = 0
    sp_max = 0
    inked_max = 0
    urls = ["ka","kill","assist","death","sp","inked"]
    
    # while i < 30:
    while True:
        url = main_url + sub_url
        res = requests.get(url,headers=headers)

        #res_text = res.text.replace('<tr class="its-me ">','<tr class="target">')
        soup = BeautifulSoup(res.text, "html.parser")

        a = soup.find("a" , class_="btn btn-default")
        tr = soup.find("tr", class_="its-me")

        #<td class="col-weapon">
        results = tr.find("td",class_="col-weapon").find("span").text
        weapon = results.strip()

        # <td class="col-kasp text-center">9 (1) / 2</td>
        results = tr.find("td",class_="col-kasp text-center").text
        ka = int(results.split(" ")[0])
        sp = int(results.split(" ")[-1])
        assist = int(results.split("(")[-1].split(")")[0])
        kill = ka - assist

        # <td class="col-kd text-center">6 / 3</td>
        results = tr.find("td",class_="col-kd text-center").text
        death = int(results.split(" ")[-1])

        tr_all = soup.find_all("tr")
        rule = ""
        for tra in tr_all:
            if not tra.find("th") == None and not tra.find("td") == None:
                if tra.find("th").text == "Mode":
                    rule = tra.find("td").text.strip()
                elif tra.find("th").text == "Turf Inked":
                    inked = int(tra.find("td").text.strip().replace(",","").replace("P",""))

        # 特定のブキかつガチマの時にのみスコアを更新
        if my_weapon in weapon and "Ranked Battle" in rule:  
            if ka > ka_max:
                ka_max = ka
                urls[0] = url
            
            if kill > kill_max:
                kill_max = kill
                urls[1] = url
            
            if assist > assist_max:
                assist_max = assist
                urls[2] = url
            
            if death > death_max:
                death_max = death
                urls[3] = url
            
            if sp > sp_max:
                sp_max = sp
                urls[4] = url
            
            if inked > inked_max:
                inked_max = inked
                urls[5] = url
        

        if not a.text=="Prev. Battle" or a.text=="次のバトル":
            print(" 最終ページ ", sub_url, a.text)
            print("ka_max:\t", ka_max, urls[0])
            print("kill_max:\t", kill_max, urls[1])
            print("assist_max:\t", assist_max, urls[2])
            print("death_max:\t", death_max, urls[3])
            print("sp_max:\t", sp_max, urls[4])
            print("inked_max:\t", inked_max, urls[5])
            break

        sub_url = a.get("href")

        if i% 100 ==0:
            print(i)
            print("ka_max:\t", ka_max, urls[0])
            print("kill_max:\t", kill_max, urls[1])
            print("assist_max:\t", assist_max, urls[2])
            print("death_max:\t", death_max, urls[3])
            print("sp_max:\t", sp_max, urls[4])
            print("inked_max:\t", inked_max, urls[5])
            
        i=i+1
        

def get_player_id(sub_url, player):
    url = main_url + "/" + account + "/spl2"
    res = requests.get(url)
    
    soup = BeautifulSoup(res.text, "html.parser")
    a = soup.find("a" , class_="btn btn-primary btn-xs")
    
    if account in a.get("href"):
        print(url)
        return a.get("href")
    else:
        sys.exit()

        
def main():
    sub_url = get_sub_url()
    # sub_url = "/@tm_ink2/spl2/4576820"
    scan_sp(sub_url)


if __name__ == "__main__":
    main()
    
