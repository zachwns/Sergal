import httpx
import asyncio

async def Metro_transit_data():
    async with httpx.AsyncClient() as client:
        url = f'https://svc.metrotransit.org/nextrip/1106'
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            route_id = [departure.get('route_id')for departure in data.get('departures',[])] 
            desc = [departure.get ('description')for departure in data.get('departures',[])]
            return route_id, desc
        else: 
            print('error')
            return[]


async def main():
    desc = await Metro_transit_data()
    route_id = await Metro_transit_data()
    print(route_id)
    print(desc)

asyncio.run(main())