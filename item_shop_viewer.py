import requests
import re
import discord
import asyncio

client = discord.Client()


REGION = ""
Prefix = "" # Bot's Prefix
username = ""
password = ""
bot_token = ""
user_in_chat = False
msg = 0
author = 0
#it must be id!
ChannelToSentNotifications = int("")
#it must be id!
user_to_ping = int("")






reaction_list = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:",
                 ":keycap_ten:", ":red_circle:", ":blue_circle:", ":brown_circle:", ":purple_circle:", ":green_circle:", ":yellow_circle:", ":white_circle:", ":black_circle:"]
reaction_list_windows = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟","🔴","🔵","🟤","🟣","🟢","🟡","⚪","⚫"]

def emoji_gun_convert(emoji):
    weapon_list = []

    for weapon in data_weapons["data"]:
        weapon_list.append(weapon["displayName"])

    return weapon_list[reaction_list_windows.index(str(emoji))]



guild_count = 0
@client.event
async def on_ready():
    global client_ready
    global guild_count
    print(f'{client.user} is connected')
    for guild in client.guilds:
        guild_count += 1

    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name=f"servers {guild_count}/100"))


    # client_ready = True


    # await bot.change_presence(activity=discord.Game(name="Anything You Want"))

def webhook(first, valorant_points, radianite_points, item_name, item_image, price, color):
    global webhook_url







def getVersion():
    versionData = requests.get("https://valorant-api.com/v1/version")
    versionDataJson = versionData.json()['data']
    final = f"{versionDataJson['branch']}-shipping-{versionDataJson['buildVersion']}-{versionDataJson['version'][-6:]}"
    return final

def contentuuidconvert(contentuuid):
    content_tiers = requests.get("https://valorant-api.com/v1/contenttiers")
    content_tiers_data = content_tiers.json()
    for row in content_tiers_data["data"]:
        if contentuuid in row["uuid"]:
            return row


def priceconvert(skinUuid, offers_data):
    for row in offers_data["Offers"]:
        if row["OfferID"] == skinUuid:
            # print("a")
            for cost in row["Cost"]:
                # print(cost)
                # print(row)
                # print(row["Cost"][cost])
                return row["Cost"][cost]



def username_to_data(username, password):
    session = requests.session()
    data = {
        'client_id': 'play-valorant-web-prod',
        'nonce': '1',
        'redirect_uri': 'https://playvalorant.com/opt_in',
        'response_type': 'token id_token',
    }
    r = session.post('https://auth.riotgames.com/api/v1/authorization', json=data)

    # print(r.text)
    data = {
        'type': 'auth',
        'username': username,
        'password': password
    }
    r = session.put('https://auth.riotgames.com/api/v1/authorization', json=data)
    pattern = re.compile(
        'access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
    data = pattern.findall(r.json()['response']['parameters']['uri'])[0]
    access_token = data[0]
    # print('Access Token: ' + access_token)

    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    r = session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={})
    entitlements_token = r.json()['entitlements_token']
    # print('Entitlements Token: ' + entitlements_token)

    r = session.post('https://auth.riotgames.com/userinfo', headers=headers, json={})
    user_id = r.json()['sub']
    # print('User ID: ' + user_id)

    # main program done
    # access_token
    # entitlements_token
    # user_id
    session.close()
    return [access_token, entitlements_token, user_id]



def get_currency(entitlements_token, access_token, user_id):
    headers = {
        'X-Riot-Entitlements-JWT': entitlements_token,
        'Authorization': f'Bearer {access_token}',
    }
    r = requests.get(f'https://pd.{REGION}.a.pvp.net/store/v1/wallet/{user_id}', headers=headers)

    data = r.json()
    # print(f"""You have {data["Balances"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"]} valorant points and {data["Balances"]["e59aa87c-4cbf-517a-5983-6e81511be9b7"]} radiante points.""")
    valorant_points = data["Balances"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"]
    radianite_points = data["Balances"]["e59aa87c-4cbf-517a-5983-6e81511be9b7"]

def skins(entitlements_token, access_token, user_id):


    headers = {
        'X-Riot-Entitlements-JWT': entitlements_token,
        'Authorization': f'Bearer {access_token}',
    }

    r = requests.get(f'https://pd.{REGION}.a.pvp.net/store/v2/storefront/{user_id}', headers=headers)

    skins_data = r.json()
    single_skins = skins_data["SkinsPanelLayout"]["SingleItemOffers"]

    bundle_fetch = requests.get(f'https://valorant-api.com/v1/bundles')
    bundle_fetch = bundle_fetch.json()
    weapon_fetch = requests.get(f'https://valorant-api.com/v1/weapons/skinlevels')
    weapon_fetch = weapon_fetch.json()

    # with open("content.txt", "w", encoding="utf-8") as file:
    #     file.write(str(content_data))
    #     file.close()
    # print(content_data)
    # with open("assets.txt", "w") as file:
    #     file.write(str(data))

    all_weapons = requests.get("https://valorant-api.com/v1/weapons")
    data_weapons = all_weapons.json()

    single_skins_images = []
    single_skins_tiers_uuids = []

    # ['12683d76-48d7-84a3-4e09-6985794f0445', 'e046854e-406c-37f4-6607-19a9ba8426fc', '60bca009-4182-7998-dee7-b8a2558dc369', 'e046854e-406c-37f4-6607-19a9ba8426fc']
    # print(contentuuidconvert("e046854e-406c-37f4-6607-19a9ba8426fc"))


    # Récupération des image de skins
    for skin in single_skins:
        for weapons_list in data_weapons['data']:
            for skin1 in weapons_list['skins']:
                if skin in str(skin1):
                    # print(skin1)
                    # if skin1['displayIcon'] != None:
                        # print("test")
                        # for chromas in skin1["chromas"]:
                        # print(skin1["chromas"])
                    if skin1["chromas"][0]["displayIcon"] != None:
                        single_skins_images.append(skin1["chromas"][0]["displayIcon"])
                    else:
                        single_skins_images.append(skin1["chromas"][0]["fullRender"])
                    single_skins_tiers_uuids.append(skin1['contentTierUuid'])
                    # else:
                    #     single_skins_images.append(skin1['displayIcon'])
                    #     single_skins_tiers_uuids.append(skin1['contentTierUuid'])

    # print(single_skins_images)
    headers = {
        'X-Riot-Entitlements-JWT': entitlements_token,
        'Authorization': f'Bearer {access_token}',
        'X-Riot-ClientVersion': getVersion(),
        "X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
    }

    data = requests.get(f"https://pd.{REGION}.a.pvp.net/store/v1/offers/", headers=headers)

    offers_data = data.json()

    for row in bundle_fetch["data"]:
        if skins_data["FeaturedBundle"]["Bundle"]["DataAssetID"] == row['uuid']:
            r_bundle_data = requests.get(f"https://valorant-api.com/v1/bundles/{row['uuid']}")
            bundle_data = r_bundle_data.json()
            # print(f"Your featured bundle is {row_small['Name']} - {bundle_data['data']['displayIcon']} - {skins_data['FeaturedBundle']['BundleRemainingDurationInSeconds']}.")
            bundle_name = row['displayName']
            try:
                bundle_image = bundle_data['data']['displayIcon']
            except KeyError:
                bundle_image = "https://notyetinvalorant-api.com"


    daily_reset = skins_data["SkinsPanelLayout"]["SingleItemOffersRemainingDurationInSeconds"]

    skin_counter = 0
    # print("Your daily item shop is: ")

    for skin in single_skins:
        for row in weapon_fetch["data"]:
            if skin == row["uuid"]:
                if skin_counter == 0:
                    skin1_name = row['displayName']
                    skin1_image = row['displayIcon']
                    skin1_price = priceconvert(skin, offers_data)
                elif skin_counter == 1:
                    skin2_name = row['displayName']
                    skin2_image = row['displayIcon']
                    skin2_price = priceconvert(skin, offers_data)
                elif skin_counter == 2:
                    skin3_name = row['displayName']
                    skin3_image = row['displayIcon']
                    skin3_price = priceconvert(skin, offers_data)
                elif skin_counter == 3:
                    skin4_name = row['displayName']
                    skin4_image = row['displayIcon']
                    skin4_price = priceconvert(skin, offers_data)
                skin_counter += 1

    if daily_reset >= 3600:
        daily_reset_in_hr = round(daily_reset / 3600, 0)
        # print(f"Daily shop items resets in {int(daily_reset_in_hr)} hours.")
    else:
        daily_reset_in_minutes = round(daily_reset / 60, 2)
        # print(f"Daily shop items resets in {daily_reset_in_minutes} minutes.")
    skins_list = {
        "bundle_name": bundle_name,
        "bundle_image": bundle_image,
        "skin1_name": skin1_name,
        "skin1_image":skin1_image,
        "skin1_price":skin1_price,
        "skin2_name": skin2_name,
        "skin2_image": skin2_image,
        "skin2_price": skin2_price,
        "skin3_name": skin3_name,
        "skin3_image": skin3_image,
        "skin3_price": skin3_price,
        "skin4_name": skin4_name,
        "skin4_image": skin4_image,
        "skin4_price": skin4_price,
        "SingleItemOffersRemainingDurationInSeconds": daily_reset,
    }

    return skins_list




def check_item_shop(username, password):
    user_data = username_to_data(username, password)
    access_token = user_data[0]
    entitlements_token = user_data[1]
    user_id = user_data[2]
    skin_data = skins(entitlements_token, access_token, user_id)
    skin_list = [skin_data["skin1_name"], skin_data["skin2_name"], skin_data["skin3_name"], skin_data["skin4_name"], skin_data["SingleItemOffersRemainingDurationInSeconds"]]
    return skin_list



def check_favourite(skin_list):
    '''
    :param skin_list:
    check_favourite([skin_data['skin1_name'], skin_data['skin2_name'], skin_data['skin3_name'], skin_data['skin4_name']]
    you need to add list with skin names
    :return:
    True or False based on if skin in favourites.txt is in skin list.
    '''
    try:
        file = open("favourites.txt", "r")
    except FileNotFoundError:
        return False
    lines = file.readlines()
    for line in lines:
        if line.splitlines()[0] in skin_list:
            return True
    return False






@client.event
async def on_message(message):
    global username
    global password
    global author
    global msg
    global data_weapons
    global user_in_chat
    global skin_list
    global selected_weapon

    found = False

    if message.author != client.user:
        if message.content.lower().startswith(f'{Prefix}shop'):
            user_data = username_to_data(username, password)
            access_token = user_data[0]
            entitlements_token = user_data[1]
            user_id = user_data[2]
            skin_data = skins(entitlements_token, access_token, user_id)
            embed = discord.Embed(title=skin_data["bundle_name"])
            embed.set_image(url=skin_data["bundle_image"])
            await message.channel.send(embed=embed)
            try:
                embed = discord.Embed(title=f"{skin_data['skin1_name']} costs {skin_data['skin1_price']}")
                if skin_data["skin1_image"] != None:
                    embed.set_image(url=skin_data["skin1_image"])
                await message.channel.send(embed=embed)
                embed = discord.Embed(title=f"{skin_data['skin2_name']} costs {skin_data['skin2_price']}")
                if skin_data["skin2_image"] != None:
                    embed.set_image(url=skin_data["skin2_image"])
                await message.channel.send(embed=embed)
                embed = discord.Embed(title=f"{skin_data['skin3_name']} costs {skin_data['skin3_price']}")
                if skin_data["skin3_image"] != None:
                    embed.set_image(url=skin_data["skin3_image"])
                await message.channel.send(embed=embed)
                embed = discord.Embed(title=f"{skin_data['skin4_name']} costs {skin_data['skin4_price']}")
                if skin_data["skin4_image"] != None:
                    embed.set_image(url=skin_data["skin4_image"])
                await message.channel.send(embed=embed)
            except TypeError:
                embed = discord.Embed(title=f"{skin_data['skin1_name']} costs {skin_data['skin1_price']}",)
                embed.set_image(url=skin_data["skin1_image"])
                await message.channel.send(embed=embed)
                embed = discord.Embed(title=f"{skin_data['skin2_name']} costs {skin_data['skin2_price']}",)
                embed.set_image(url=skin_data["skin2_image"])
                await message.channel.send(embed=embed)
                embed = discord.Embed(title=f"{skin_data['skin3_name']} costs {skin_data['skin3_price']}",)
                embed.set_image(url=skin_data["skin3_image"])
                await message.channel.send(embed=embed)
                embed = discord.Embed(title=f"{skin_data['skin4_name']} costs {skin_data['skin4_price']}",)
                embed.set_image(url=skin_data["skin4_image"])
                await message.channel.send(embed=embed)

        elif message.content.lower().startswith(f'{Prefix}favourite'):
            author = message.author.id
            #ping user await message.channel.send(f"<@!{author}>")
            all_weapons = requests.get("https://valorant-api.com/v1/weapons")
            data_weapons = all_weapons.json()
            embed = discord.Embed(title="Choose weapon:")
            i = 0
            for weapon in data_weapons["data"]:
                embed.add_field(name=weapon["displayName"], value=reaction_list[i])
                i += 1
            msg = await message.channel.send(embed=embed)
            for emoji in reaction_list_windows:
                try:
                    await msg.add_reaction(emoji)
                except discord.errors.NotFound:
                    pass
        elif user_in_chat:
            user_in_chat = False
            for skin in skin_list:
                if skin.lower() == message.content.lower():
                    await message.channel.send(f"Succesfully added **{skin}** to favourites ❤!")
                    file_append = open("favourites.txt", "a")
                    file_append.write(skin + "\n")
                    file_append.close()
                    found = True
            if found == False:
                await message.channel.send("Couldn't find any matches :(")







        elif message.content.lower().startswith(f'{Prefix}help'):
            await message.channel.send(f"""{Prefix}help - show full list of commands
{Prefix}shop - show current shop
{Prefix}favourite - add skins to favourite so when it appears in shop you will get pinged""")

@client.event
async def on_reaction_add(reaction, user):
    global author
    global msg
    global reaction_emoji
    global data_weapons
    global user_in_chat
    global skin_list
    global selected_weapon

    user_in_chat = False
    skin_string = ""
    skin_list = []

    try:
        if msg.id == reaction.message.id:
            if user.id == author:
                if str(reaction) in reaction_list_windows:
                    reaction_emoji = reaction
                    await msg.delete()
                    selected_weapon = emoji_gun_convert(reaction_emoji)
                    await reaction.message.channel.send(f"Selected **{selected_weapon}** as a weapon!")
                    for weapon in data_weapons["data"]:
                        if weapon["displayName"] == selected_weapon:
                            for skin in weapon["skins"]:
                                skin_string += f"{skin['displayName']}\n"
                                skin_list.append(skin['displayName'])
                            skin_message = discord.Embed(title="Choose skin:", description="```" + skin_string + "```")
                            await reaction.message.channel.send(embed=skin_message)
                            await reaction.message.channel.send("Please type the skin you want to add to favourites: ")
                            user_in_chat = True
    except AttributeError:
        pass

async def my_background_task():
    global username
    global password
    global author
    global ChannelToSentNotifications
    global user_to_ping
    await client.wait_until_ready()
    channel = client.get_channel(ChannelToSentNotifications)
    while client.is_closed:
        user_data = username_to_data(username, password)
        access_token = user_data[0]
        entitlements_token = user_data[1]
        user_id = user_data[2]
        skin_data = skins(entitlements_token, access_token, user_id)
        shop_end = skin_data['SingleItemOffersRemainingDurationInSeconds']
        if check_favourite([skin_data['skin1_name'], skin_data['skin2_name'], skin_data['skin3_name'], skin_data['skin4_name']]) == True:
            await channel.send(f"<@{user_to_ping}> You have your favourite skin in shop!")
        await asyncio.sleep(int(shop_end))

client.loop.create_task(my_background_task())
client.run(bot_token)
