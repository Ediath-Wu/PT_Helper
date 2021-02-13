import requests
from bencode import decode,encode

url="https://pt.btschool.club/announce.php?passkey=1ebee67fac0b737cd7295cfa9eb38ea5?info_hash=%06%9a%3e%8c%ae%fd%9a%b0%88%7d%3f%3a%11%c6%a4%08%0e%a0I%26&peer_id=-qB4250-3ZN_N4C0Gh.*&port=64325&uploaded=0&downloaded=0&left=144260086380&corrupt=0&key=A94190FB&event=started&numwant=200&compact=1&no_peer_id=1&supportcrypto=1&redundant=0"

headers={
    "User-Agent":"uTorrent/2210(25130)",
    "Accept-Encoding":"gzip",
    "Connection"     :"Close"
}

res= requests.get(url=url,headers=headers)
print(res.text().decode())
while(1):
    pass