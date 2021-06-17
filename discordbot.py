#! /usr/bin/env python3
from discord.ext import tasks
from stockcheck import StockCheck

import discord

class MyClient(discord.Client):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # an attribute we can access from our task
    self.stores = [StockCheck('https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149'), StockCheck('https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161'), StockCheck('https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5-digital-edition/11108141.html'), StockCheck('https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html')]
    self.role = "<@&855138343095631912>"
    # start the task to run in the background
    self.my_background_task.start()

  async def on_ready(self):
    print(f'Logged in as {self.user} (ID: {self.user.id})')
    print('------')

  @tasks.loop(seconds=60) # task runs every 60 seconds
  async def my_background_task(self):
    channel = self.get_channel(285648978115166209) # channel ID goes here
    instock = False
    for store in self.stores:
      if store.checkStock():
        instock = True
        await channel.send(f"{self.role} Item in stock at {store.getUrl()}")
    if not instock:
      await channel.send(f"Item not in stock")

  @my_background_task.before_loop
  async def before_my_task(self):
    await self.wait_until_ready() # wait until the bot logs in



client = MyClient()
client.run('Bot Key')
