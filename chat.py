import bot

chatr = bot.Showdown_Bot()
chatr.threaded_chat_forever()
chatr.ws.run_forever()
