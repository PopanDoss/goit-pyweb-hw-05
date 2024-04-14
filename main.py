import platform
import sys

import aiohttp
import asyncio
import aiofiles

import json
from datetime import datetime, timedelta

async def main(days):

    async with aiohttp.ClientSession() as session:
        
        course = []

        if 0< days <= 10:

            for i in range(0, days):

                date = (datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y')
                url = (f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date}")

                try:
                    async with session.get(url) as response:
                        
                        if response.status == 200:

                            content_type = response.headers.get('Content-Type')

                            if content_type == 'application/json':

                                result = await response.json()
                                course_data = {date: {'EUR': {'sale': result['exchangeRate'][1]['saleRateNB'], 'purchase': result['exchangeRate'][1]['purchaseRateNB']}, 
                                'USD': {'sale':  result['exchangeRate'][6]['saleRateNB'], 'purchase': result['exchangeRate'][6]['saleRateNB']}}}
                            
                                course.append(course_data)
                            
                            else:
                                print(f"Error content type: {content_type} for {url}")
                                quit()         
                        else:
                            print(f"Error status: {response.status} for {url}")
                            quit()
                
                except aiohttp.ClientConnectorError as err:
                    print(f"Connection error: {err} for {url}")
                        
            async with aiofiles.open("course.json", 'w') as file:
        
                json_data = json.dumps(course, indent=2)  
                await file.write(json_data)
                print("Course ready")
            
        else:
            print("The number of days cannot be more than 10 and less than 0")
            


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    days = int ( sys.argv[1])
    asyncio.run(main(days))
    
    
 