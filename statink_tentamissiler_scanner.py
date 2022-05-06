import requests
from bs4 import BeautifulSoup
import sys

account = "@tm_ink2"

ignore_list = [""]
main_url = "https://stat.ink"
marumisa_list = []
threthold = 5

"""
<tr class=" ">  <td class="bg-my text-center"></td>
  <td class="col-name"><div style="display:flex;align-items:center;justify-content:space-between"><span><span><img class="auto-tooltip" src="https://jdenticon.stat.ink/ffef93db08b2b6161bb686b6331dedba38bea641.svg" alt="" title="ID: 13531f4026ca992b" style="width:1.2em;height:auto">  き</span></span><span><span style="display:inline-block;line-height:1;padding:1px;background:#333;border-radius:4px"><img class="auto-tooltip" src="/assets/20220407-163/lxewnqyyhjsl3j7s/inkling.png?v=1649348864" alt="イカ" title="イカ" style="height:calc(1.2em - 2px);width:auto"></span></span></div></td>
  <td class="col-weapon"> <span class="auto-tooltip" title="サブ: キューバンボム / スペシャル: マルチミサイル"><img class="w-auto h-em" src="/assets/20220407-163/mmgsnf6xmcd3p44i/variableroller_foil.png?v=1649348864" alt=""> ヴァリアブルローラーフォイル</span></td>
  <td class="col-level text-right">80</td>
  <td class="col-rank text-center">X</td>
  
  <td class="col-point text-right"><span class="col-point-inked">917</span></td>
  <td class="col-kasp text-center">10 (4) / 4</td>
  <td class="col-kd text-center">6 / 3</td>
  <td class="col-kd text-right">2.00<br><small class="text-muted">66.67%</small></td></tr>
"""


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
    marumisa_num = 0
    i = 1
    
    # while i < 30:
    while True:
        url = main_url + sub_url
        res = requests.get(url)
        
        # <tr class=" ">をスクレイピングで捉えられないので変換
        res_text = res.text.replace('<tr class=" ">','<tr class="target">')
        res_text = res_text.replace('<tr class="its-me ">','<tr class="target">')
        soup = BeautifulSoup(res_text, "html.parser")

        a = soup.find("a" , class_="btn btn-default")
        trs = soup.find_all("tr", class_="target")

        sp_times = []
        sp_kinds = []
        kill_times = []
        player_names = []

        for tr in trs:
            sub_sp = tr.find("span",class_="auto-tooltip").get("title")
            # title="Sub: Suction Bomb / Special: Tenta Missiles"
            if sub_sp.startswith("Sub:"):
                sp_kind = sub_sp.split("Special:")[-1].strip()
            # title="サブ: キューバンボム / スペシャル: マルチミサイル"
            elif sub_sp.startswith("サブ:"):
                sp_kind = sub_sp.split("スペシャル:")[-1].strip()

            sp_kinds.append(sp_kind)

            # <td class="col-kasp text-center">9 (1) / 2</td>
            results = tr.find("td",class_="col-kasp text-center").text
            ka = int(results.split(" ")[0])
            sp = int(results.split(" ")[-1])
            assist = int(results.split("(")[-1].split(")")[0])
            kill = ka - assist
            sp_times.append(sp)
            kill_times.append(kill)
            
            # <td class="col-name"><div style="display:flex;align-items:center;justify-content:space-between"><span><span><img class="auto-tooltip" src="https://jdenticon.stat.ink/ffef93db08b2b6161bb686b6331dedba38bea641.svg" alt="" title="ID: 13531f4026ca992b" style="width:1.2em;height:auto">  き</span></span><span><span style="display:inline-block;line-height:1;padding:1px;background:#333;border-radius:4px"><img class="auto-tooltip" src="/assets/20220407-163/lxewnqyyhjsl3j7s/inkling.png?v=1649348864" alt="イカ" title="イカ" style="height:calc(1.2em - 2px);width:auto"></span></span></div></td>
            player = tr.find("td",class_="col-name").text.strip()
            player = player.replace(" ","")
            player = player.replace("'","")
            player = player.replace('"',"")
            player_names.append(player)

        sp_max = max(sp_times)
        for t,k,i,p in zip(sp_times,sp_kinds,kill_times,player_names):
            # if t >= threthold and i < 1 and k == "Tenta Missiles":
            if t >= threthold and k == "Tenta Missiles":
                print("[+] ミサイルマン発見:"+str(t)+"\t"+k+"\t"+str(i)+"キル"+"\t"+p)
                marumisa_list.append(url + " " + p + " " + str(t) + " " + str(i))
                marumisa_num += 1

                if marumisa_num % 100 ==0:
                    print(marumisa_list)
                
            if t == sp_max:
                #print("[+] Max:"+str(t)+"\t"+k+"\t"+p)
                if t > 20:
                    print(url)
                    input()

        if not a.text=="Prev. Battle" or a.text=="次のバトル":
            print(" 最終ページ ", sub_url, a.text)
            print(marumisa_list)
            break
        sub_url = a.get("href")
        

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
    # sub_url = "/@tm_ink2/spl2/4518781"
    scan_sp(sub_url)


if __name__ == "__main__":
    main()
    
