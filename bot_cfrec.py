# Standard Libraries
import requests
import os
import datetime
import sqlite3
import time

# Non-standard Libraries installed with pip
import discord
from discord import app_commands
from discord.utils import get
from discord.ext import commands, tasks
from dotenv import load_dotenv


# Local Libraries
import Recommend
import duel

load_dotenv()

# BOT_ID = int(os.getenv('BOT_ID'))
BOT_TOKEN = os.getenv('BOT_TOKEN')
MY_ID = int(os.getenv('MY_ID'))

con = cursor = run_time = None

bot = commands.Bot(command_prefix='$', owner_id = MY_ID, intents=discord.Intents.all())

def start_bot():
	global con, cursor
	con = sqlite3.connect("users.db")
	cursor = con.cursor()
	cursor.row_factory = sqlite3.Row

	run_time = datetime.time(hour=16, minute=00)


	bot.run(BOT_TOKEN)



@bot.event
async def on_ready():
	print("-- Bot is starting up.")
	
	print(f"\tTime right now: {datetime.datetime.now()}")
	print(f"\tDaily task will run once per day at {run_time} UTC")
	
	daily_task.start()
	
	await bot.tree.sync()
	activity = discord.Activity(type=discord.ActivityType.competing, name="HackDavis 2024")
	await bot.change_presence(activity=activity)

	return


@tasks.loop(minutes=5)
async def daily_task():
	return


async def shutdown_aux():
	print("-- Bot Shutting Down")
	await bot.close()
	return

@bot.command()
@commands.dm_only()
async def sd(ctx):
	print(f"-- Direct message with {ctx.author.name}: `$sd` called by {ctx.author.name}")
	#Check to see if it was called by owner.    
	called_by_owner = await bot.is_owner(ctx.author)
   

	if called_by_owner == False:
		return

	await ctx.send("Shutting down. Until next time... :wave:")
	print()
	
	#Then close bot
	await shutdown_aux()
	print()
	return



@bot.tree.command(name="help", description="Shows descriptions for all commands and how to use the bot.")
async def help_command(interaction: discord.Interaction):
	on_command(interaction)

	embed = discord.Embed(title='Need help? Look no further!', color=discord.Color.dark_blue(), )

	link_desc = """- Links your Discord account to your Codeforces account. 
- Because of how Codeforces' API works, you must visit https://codeforces.com/problemset/problem/4/A and submit a Compile Error.	
- ❗**This command must be called before accessing any features of the bot, and will only work once you submit the Compile Error.**"""
	embed.add_field(name="__`/link`__", value=link_desc, inline=False)

	unlink_desc = """- Unlinks your Discord account and Codeforces account. Type CONFIRM to confirm this action."""
	embed.add_field(name="__`/unlink` <CONFIRM>__", value=unlink_desc, inline=False)


	recommend_desc = """- Recommends `count` problems for you to attempt, 5 by default. This is based on your profile and completed problems."""
	embed.add_field(name="__`/recommend <count>`__", value=recommend_desc, inline=False)


	await interaction.response.send_message(embed=embed)

	return


class FirstSetup(discord.ui.Modal, title='Let\'s get you set up!'):
	handle = discord.ui.TextInput(label='Your Codeforces Handle', required=True)

	understand = discord.ui.TextInput(label='Please submit a Compile Error to Problem 4A', 
									  placeholder='Then type \'CONFIRM\' and submit.', 
									  required=True)
	
	async def on_submit(self, interaction: discord.Interaction):
		await interaction.response.defer()


@bot.tree.command(name="link", description="Link your Codeforces handle to your Discord account.")
async def link(interaction: discord.Interaction):
	on_command(interaction)
	

	check_exists = f"""
SELECT * FROM cf_users
WHERE discord_id='{interaction.user.id}'
"""
	cursor.execute(check_exists)
	user_before_update = cursor.fetchone()

	if user_before_update != None:	
		await interaction.response.send_message(f"Your Discord account is already linked to the handle {user_before_update['handle']}", ephemeral=True)
		return
	
	modal = FirstSetup()

	await interaction.response.send_modal(modal)

	errored = await modal.wait()

	print("View finished normally?", not errored)

	if str(modal.understand) != "CONFIRM":
		print(f"Modal response, {modal.understand = }")
		await interaction.followup.send("Please run `/link` again and ensure you submit a Compile Error to https://codeforces.com/problemset/problem/4/A and type \'CONFIRM\' in the popup.", ephemeral=True)
		return

	handle: str = str(modal.handle).strip()

	response = requests.get(f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=1")

	if not response.ok:
		print(f"Response errored, Code {response.status_code}")
		await interaction.followup.send("Ran into a HTTPS error, did you enter your handle correctly?", ephemeral=True)
		return
	
	rdict = response.json()['result']

	if len(rdict) != 1 or 'verdict' not in rdict[0]:
		await interaction.followup.send("It looks like you haven't solved any problems yet. Maybe Codeforces is still processing your submission?", ephemeral=True)
		return
	
	if rdict[0]['problem']['contestId'] != 4 or rdict[0]['problem']['index'] != "A" or rdict[0]['verdict'] != "COMPILATION_ERROR":
		verdict = rdict[0].get('verdict')
	
		print(f"Verdict Error, {verdict = }")
		await interaction.followup.send("Please run `/link` again and ensure you submit a Compile Error to https://codeforces.com/problemset/problem/4/A and type \'CONFIRM\' in the popup.", ephemeral=True)
		return

	c = f"""
SELECT * FROM cf_users
WHERE handle='{handle}'
"""
	cursor.execute(c)
	if cursor.fetchone() != None:
		# user with Handle exists, just update discord_id
		print(f"User with handle {handle} exists. Updating discord_id to {interaction.user.id}")
		update = f"""
UPDATE cf_users
SET discord_id='{interaction.user.id}'
WHERE handle='{handle}'
"""
		cursor.execute(update)
		con.commit()
	else:
		# handle not found, insert discord_id
		print(f"User with handle {handle} NOT FOUND. Inserting with discord_id: {interaction.user.id}")
		s = f"""
INSERT INTO cf_users (handle, discord_id)
VALUES ('{handle}', '{interaction.user.id}')
"""
		cursor.execute(s)

	verify_inserted = f"""
SELECT * FROM cf_users
WHERE handle='{handle}'
"""
	
	cursor.execute(verify_inserted)
	user_after_update = cursor.fetchone()
	print(f"{user_after_update['discord_id'] = }")
	if user_after_update['discord_id'] == str(interaction.user.id):
		await interaction.followup.send("Your account has been linked successfully!", ephemeral=True)
		con.commit()
	else:
		await interaction.followup.send("Something went wrong on our end. Please try again :(", ephemeral=True)
	
	return


@bot.tree.command(name="unlink", description="Unlinks your Codeforces account.")
@app_commands.describe(confirm="Type 'CONFIRM' to confirm this action.")
async def unlink(interaction: discord.Interaction, confirm: str):
	on_command(interaction)
	
	if confirm != "CONFIRM":
		await interaction.response.send_message("Please type `CONFIRM` in order to unlink.", ephemeral=True)
	check_exists = f"""
SELECT * FROM cf_users
WHERE discord_id='{interaction.user.id}'
"""
	cursor.execute(check_exists)
	user_before_update = cursor.fetchone()

	if user_before_update == None:	
		await interaction.response.send_message(f"Your Discord account is not linked yet! Do so by running `/link`", ephemeral=True)
		return

	delete = f"""
DELETE FROM cf_users
WHERE discord_id='{str(interaction.user.id)}'
"""
	cursor.execute(delete)

	check_exists = f"""
SELECT * FROM cf_users
WHERE discord_id='{interaction.user.id}'
"""
	cursor.execute(check_exists)
	user_before_update = cursor.fetchone()

	if user_before_update != None:
		await interaction.response.send_message("Something went wrong on our end, please try again :(", ephemeral=True)
	else:
		con.commit()
		await interaction.response.send_message("Your account has been unlinked successfully!", ephemeral=True)
	
	return
	


@bot.tree.command(name="recommend", description="Recommends a list of problems for you to try next.")
async def recommend(interaction: discord.Interaction):
	on_command(interaction)

	check_exists = f"""
SELECT * FROM cf_users
WHERE discord_id='{interaction.user.id}'
"""
	cursor.execute(check_exists)
	user = cursor.fetchone()

	if user == None:
		await interaction.response.send_message(f"Your Discord account doesn't seem to be linked yet, please do so by running `/link`", ephemeral=True)
		return
	handle = user['handle']
	recommended_problems = Recommend.smart_recommend(handle)
	if len(recommended_problems) == 0:
		await interaction.response.send_message(f"Looks like I don't have anything to recommend to you right now... Have you solved any problems yet?")
		return
	embed = discord.Embed(title="Here are some problems you should try!", color=discord.Color.blurple())
	for problem in recommended_problems:
		name = problem["name"]
		url = problem["url"]
		rating = problem["rating"]
		embed.add_field(name=f"__{name}__", value=f"*{url}*\nRating: **{rating}**", inline=False)
	
	await interaction.response.send_message(embed=embed)

	return


# Audits the current command running along with who called it and where it was called (guild channel/dm channel)
def on_command(interaction):
	if(interaction.guild is None):
		print(f"-- Direct Message with {interaction.user.name}: `/{interaction.command.name}` by {interaction.user.name}")
	else:
		print(f"-- {interaction.guild.name}({interaction.guild.id}): `/{interaction.command.name}` by {interaction.user.name}")

	return


@bot.tree.command(name="duel", description="Challenge an opponent to a duel.")
@app_commands.describe(handle="Your desired opponent's Codeforces Handle")
async def unlink(interaction: discord.Interaction, handle: str):
	on_command(interaction)
	check_exists = f"""
SELECT * FROM cf_users
WHERE discord_id='{interaction.user.id}'
"""
	cursor.execute(check_exists)
	user = cursor.fetchone()

	check_opponent_exists = f"""
SELECT * FROM cf_users
WHERE handle='{handle}'
"""
	cursor.execute(check_opponent_exists)
	opp = cursor.fetchone()


	if user == None:
		await interaction.response.send_message(f"Your Discord account doesn't seem to be linked yet, please do so by running `/link`", ephemeral=True)
		return
	
	if opp == None:
		await interaction.response.send_message(f"I couldn't find a user in my database named {handle}. Did they link their account with me yet?", ephemeral=True)
		return
	
	if user['handle'] == opp['handle']:
		await interaction.response.send_message(f"You can't duel yourself!")
		return

	user_handle = user['handle']
	opp_handle = opp['handle']
	print(f"{user_handle =}, {opp_handle =}")

	await interaction.response.defer()
	recommended_problems = duel.duel_init(user1=user_handle, user2=opp_handle)
	if len(recommended_problems) == 0:
		await interaction.response.send_message(f"Looks like I don't have anything to recommend to you right now... Have you solved any problems yet?")
		return
	
	embed = discord.Embed(title="Let the duel begin!", color=discord.Color.red())
	for num, problem in enumerate(recommended_problems):
		name = problem["name"]
		url = problem["url"]
		rating = problem["rating"]
		embed.add_field(name=f"{num + 1}. __{name}__", value=f"*{url}*\nRating: **{rating}**", inline=False)
	#embed.add_field(name="Erummm...", value=f"{solved}", inline=False)
	
	await interaction.followup.send(embed=embed)
	# duel_time(recommended_problems, user_handle, opp_handle, 1)
	mins = 0.2
	# channel = bot.get_channel(1234721887737745478)
	# channel = interaction.channel.id
	seconds = mins * 60
	max_time = mins * 60
	ids = []
	solved = []
	for p in recommended_problems:
		ids.append(str(p['contestId']) + str(p["index"]))
		solved.append(None)
	print("starting timer")
	start = time.time()
	# interval = 5
	while seconds > 0:
		time.sleep(1)
		if seconds % 2 == 0:
			prob, u = duel.duel_check(user_handle, opp_handle, ids, solved)
			print(f"{solved[prob]} = {u}")
			if prob != None and (u == 0 or u == 1) and solved[prob] != u:
				solved[prob] = u
				# await channel.send(f"{u} has solved the {prob}th problem! :)")
				await interaction.followup.send(f"{u} has solved the {prob}th problem! :)")
		# if interval == 0:
		# 	interval = 5
		# 	await channel.send(solved)
		# interval -= 1
		seconds -= 1
		curtime = time.time()
		if curtime - start > max_time:
			# print(curtime - start)
			break
	end = time.time()
	# print("contest done!")
	await interaction.followup.send(solved)
	print(end - start)

# async def duel_checker():
# 	await bot.wait_until_ready()
# 	counter = 0
# 	channel = bot.get_channel(id=1234721887737745478) # replace with channel_id
# 	while not bot.is_closed():
# 		counter += 1
# 		await channel.send(counter)
# 		await bot.sleep(60) # task runs every 60 seconds

# def duel_time(probs, user1, user2, mins):
# 	channel = bot.get_channel(id=1234721887737745478)
# 	seconds = mins * 60
# 	ids = []
# 	solved = []
# 	for p in probs:
# 		ids.append(str(p['contestId']) + str(p["index"]))
# 		solved.append(None)
	
# 	print("starting timer")
# 	interval = 5
# 	while seconds > 0:
# 		time.sleep(1)
# 		if interval == 0:
# 			interval = 5
# 			channel.send("hi")
# 		interval -= 1
# 		seconds -= 1
	
# 	solved = duel.duel_check(user1, user2, ids, solved)
# 	return solved

def main():
	start_bot()	

if __name__ == '__main__':
	main()