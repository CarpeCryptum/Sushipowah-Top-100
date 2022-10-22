import pandas as pd
import requests
import json
from web3 import Web3, HTTPProvider
from pprint import pprint as pp
import time
import numpy as np

url_xSUSHI="https://api.ethplorer.io/getTopTokenHolders/0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272?apiKey=freekey&limit=100"
page_xS=requests.get(url_xSUSHI)
data_xS=(page_xS.text)
xs=[]
xsd=json.loads(data_xS)
xsl=xsd['holders']
for i in xsl:
    xs.append(i['address'])

url_tSUSHI="https://api.ethplorer.io/getTopTokenHolders/0xf49764c9C5d644ece6aE2d18Ffd9F1E902629777?apiKey=freekey&limit=10"
page_tS=requests.get(url_tSUSHI)
data_tS=(page_tS.text)
ts=[]
tsd=json.loads(data_tS)
tsl=tsd['holders']
for i in tsl:
    ts.append(i['address'])
time.sleep(2)
url_axSUSHI="https://api.ethplorer.io/getTopTokenHolders/0xF256CC7847E919FAc9B808cC216cAc87CCF2f47a?apiKey=freekey&limit=30"
page_axS=requests.get(url_axSUSHI)
data_axS=(page_axS.text)
axs=[]
axsd=json.loads(data_axS)
axsl=axsd['holders']
for i in axsl:
    axs.append(i['address'])

url_meow='https://api.ethplorer.io/getTopTokenHolders/0x650F44eD6F1FE0E1417cb4b3115d52494B4D9b6D?apiKey=freekey&limit=10'
page_meow=requests.get(url_meow)
data_meow=(page_meow.text)
meow=[]
meowd=json.loads(data_meow)
meowl=meowd['holders']
for i in meowl:
  meow.append(i['address'])

time.sleep(2)
url_slp='https://api.ethplorer.io/getTopTokenHolders/0x795065dcc9f64b5614c407a6efdc400da6221fb0?apiKey=freekey&limit=10'
page_slp=requests.get(url_slp)
data_slp=(page_slp.text)
slp=[]
slpd=json.loads(data_slp)
slpl=slpd['holders']
for i in slpl:
    slp.append(i['address'])

url_Bento='https://api.thegraph.com/subgraphs/name/matthewlilley/bentobox-ethereum'
query = '''{
    userTokens (
      first: 10,
      where: {token:"0x8798249c2e607446efb7ad49ec89dd1865ff4272"},
      orderBy: share,
      orderDirection: desc
    ) {
    user {
      id
    }
  }
}
'''
r = requests.post(url_Bento, json={'query': query})
data_bento = json.loads(r.text)
bl=data_bento['data']['userTokens']
bento=[]
n=0
for i in bl:
    bento.append(bl[n]['user']['id'])
    n+=1
url_farm='https://api.thegraph.com/subgraphs/name/jiro-ono/masterchef-staging'
query='''
{
 users(first:25, where:{pool:"12"}, orderBy:amount,
orderDirection:desc)
  {
  id
  }
}'''
r=requests.post(url_farm, json={'query': query})
data_farm=json.loads(r.text)
lfarm=data_farm['data']['users']
farm=[]
for i in lfarm:
    farm.append(i['id'][3:])

b=xs+ts+axs+bento+meow+farm+slp
time.sleep(5)
b2=[Web3.toChecksumAddress(i) for i in b]
b2.remove('0xF256CC7847E919FAc9B808cC216cAc87CCF2f47a')
b2.remove('0x650F44eD6F1FE0E1417cb4b3115d52494B4D9b6D')
b2.remove('0xF5BCE5077908a1b7370B9ae04AdC565EBd643966')
b2.remove('0xc2EdaD668740f1aA35E4D8f227fB8E17dcA888Cd')

b3=[*set(b2)]

url = 'YOUR API KEY'
w3=Web3(Web3.HTTPProvider(url))
SP_address="0x62d11bc0652e9D9B66ac0a4c419950eEb9cFadA6"
SP_abi=json.loads('[{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"powah","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"total","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"}]')
contract=w3.eth.contract(address=SP_address, abi=SP_abi)

SP=contract.functions.totalSupply().call()
TSP=(SP/1000000000000000000)

voters=[]
for i in b3:
    p=w3.eth.contract(address=SP_address, abi=SP_abi)
    voters.append(
       [ i, p.functions.balanceOf(i).call()]
    )
def from_wei(_n: int):
  return Web3.fromWei(_n, 'ether')

df = pd.DataFrame (voters, columns = ['voter', 'powah'])
df['powah'] = df['powah'].map(from_wei)
df.sort_values(by=['powah'], inplace=True, ascending=False)
df['powah']=df['powah'].astype('float')
r_df=df.round(2)
r_df['share']=r_df['powah']/TSP*100
final=r_df.reset_index(drop=True)
pp(final.head(100).to_csv("NAME.csv"))
