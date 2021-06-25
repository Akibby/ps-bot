#! /usr/bin/env python3
from discord.ext import tasks
from stockcheck import StockCheck
from secrets import BOT_KEY, CHANNEL_KEY, XBOX_ROLE_KEY, PS4_ROLE_KEY, GPU_ROLE_KEY, TEST_CHANNEL_KEY

import discord

class MyClient(discord.Client):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # an attribute we can access from our task
    self.stores = [StockCheck('https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149'), 
                    StockCheck('https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161'), 
                    StockCheck('https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5-digital-edition/11108141.html'), 
                    StockCheck('https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html'),
                    StockCheck('https://www.gamestop.com/video-games/xbox-series-x/consoles/products/xbox-series-x/B224744V.html'),
                    StockCheck('https://www.gamestop.com/video-games/xbox-series-x/consoles/products/xbox-series-x/B224744V.html'),
                    StockCheck('https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440')]
    self.psrole = PS4_ROLE_KEY
    self.xbrole = XBOX_ROLE_KEY
    self.gpurole = GPU_ROLE_KEY
    self.counter = 0
    self.instock = False
    # start the task to run in the background
    self.my_background_task.start()

  async def on_ready(self):
    print(f'Logged in as {self.user} (ID: {self.user.id})')
    print('------')
    f = open("log", "w")
    f.write(f'Logged in as {self.user} (ID: {self.user.id})\n')
    f.close()

  @tasks.loop(seconds=90) # task runs every 90 seconds
  async def my_background_task(self):
    channel = self.get_channel(CHANNEL_KEY) # channel ID goes here
    instock = False
    for store in self.stores:
      if store.checkStock():
        self.instock = True
        if "playstation" in store.getUrl():
          await channel.send(f"{self.psrole} Item in stock at {store.getUrl()}")
        elif "xbox" in store.getUrl():
          await channel.send(f"{self.xbrole} Item in stock at {store.getUrl()}")
        elif "nvidia" in store.getUrl():
          await channel.send(f"{self.gpurole} Item in stock at {store.getUrl()}")
        else:
          await channel.send(f"{self.xbrole} {self.psrole} {self.gpurole} Item in stock at {store.getUrl()}")
    if self.counter == 1440:
      self.counter = 0
      if not self.instock:
        await channel.send(f"No stock in the last 24 hours")
      else:
        self.instock = False
    else:
      self.counter+=1

  @my_background_task.before_loop
  async def before_my_task(self):
    await self.wait_until_ready() # wait until the bot logs in



client = MyClient()
client.run(BOT_KEY)
