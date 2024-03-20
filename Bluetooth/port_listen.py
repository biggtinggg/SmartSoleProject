import asyncio
from bleak import BleakClient
 
UID_1 = "19b10001-e8f2-537e-4f6c-d104768a1214"
UID_2 = "19b10001-e8f2-537e-4f6c-d104768a1215"
  
  
async def read_data(address):
    async with BleakClient(address) as client:
        await client.start_notify(UID_1, notification_handler) 
        await client.start_notify(UID_2, notification_handler)  
        while True:
            await asyncio.sleep(1)
  
  
async def notification_handler(sender, data):
    print("Sender:", sender)
    values = data    
    print(values.decode("utf-8"))

  
  
async def main(address):
    await read_data(address)
  
asyncio.run(main("D5:B6:C5:1E:71:4B"))