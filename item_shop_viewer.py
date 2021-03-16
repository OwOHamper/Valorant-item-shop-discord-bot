import requests
import re
import discord

client = discord.Client()


username = "ENTER_RIOT_USERNAME_HERE"
password = "ENTER_RIOT_PASSWORD_HERE"
bot_token = "ENTER_BOT_TOKEN_HERE"


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

# def webhook(first, valorant_points, radianite_points, item_name, item_image, price, color):
#     global webhook_url
#
#
#     webhook_url = webhook_url
#     if first:
#         webhook_data = {
#             "username": "Valorant Item shop",
#             "avatar_url": "https://wi.wallpapertip.com/wsimgs/102-1024349_valorant-logo-wallpaper-hd.png",
#             "content": f"Valorant item shop for account = {user_id}"
#         }
#     else:
#         webhook_data = {
#             "username": "Valorant Item shop",
#             "avatar_url": "https://wi.wallpapertip.com/wsimgs/102-1024349_valorant-logo-wallpaper-hd.png",
#         }
#     if first:
#         webhook_data["embeds"] = [
#             {
#                 "title": f"You have {valorant_points} valorant points and {radianite_points} radianite points.",
#                 "description": f"Your featured bundle is {item_name}",
#                 "image": {
#                     "url": item_image
#                 }
#             }
#         ]
#     else:
#         webhook_data["embeds"] = [
#             {
#                 "color": hex_convert(color),
#                 "title": f"{item_name} costs {price} Valorant points",
#                 "image": {
#                     "url": item_image
#                 }
#             }
#         ]
#
#     result11 = requests.post(webhook_url, json=webhook_data)
#
#     try:
#         result11.raise_for_status()
#     except requests.exceptions.HTTPError as err:
#         print(err)
#     else:
#         print("Payload delivered successfully, code {}.".format(result11.status_code))


# webhook_url = input("Enter discord webhook url: ")
# webhook_url = "https://discord.com/api/webhooks"













def hex_convert(hex):
    if hex == "004c3d33":
        return "0x004c3d"
    elif hex == "e07a0633":
        return "0xE07A06"
    elif hex == "a2164333":
        return "0xa21643"
    elif hex == "1a58c133":
        return "0x1a58c1"
    elif hex == "dcd32133":
        return "0xdcd321"



def getVersion():
    versionData = requests.get("https://valorant-api.com/v1/version")
    versionDataJson = versionData.json()['data']
    final = f"{versionDataJson['branch']}-{versionDataJson['buildVersion']}-{versionDataJson['version'][-6:]}"
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
    r = requests.get(f'https://pd.EU.a.pvp.net/store/v1/wallet/{user_id}', headers=headers)

    data = r.json()
    # print(f"""You have {data["Balances"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"]} valorant points and {data["Balances"]["e59aa87c-4cbf-517a-5983-6e81511be9b7"]} radiante points.""")
    valorant_points = data["Balances"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"]
    radianite_points = data["Balances"]["e59aa87c-4cbf-517a-5983-6e81511be9b7"]

def skins(entitlements_token, access_token, user_id):

    headers = {
        'X-Riot-Entitlements-JWT': entitlements_token,
        'Authorization': f'Bearer {access_token}',
    }

    r = requests.get(f'https://pd.EU.a.pvp.net/store/v2/storefront/{user_id}', headers=headers)

    skins_data = r.json()
    single_skins = skins_data["SkinsPanelLayout"]["SingleItemOffers"]

    headers = {
        'X-Riot-Entitlements-JWT': entitlements_token,
        'Authorization': f'Bearer {access_token}',
        'X-Riot-ClientVersion': getVersion(),
        "X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
    }

    r = requests.get(f'https://shared.EU.a.pvp.net/content-service/v2/content/', headers=headers)

    content_data = r.json()

    # with open("assets.txt", "w") as file:
    #     file.write(str(data))

    all_weapons = requests.get("https://valorant-api.com/v1/weapons")
    data_weapons = all_weapons.json()

    single_skins_images = []
    single_skins_tiers_uuids = []

    # ['12683d76-48d7-84a3-4e09-6985794f0445', 'e046854e-406c-37f4-6607-19a9ba8426fc', '60bca009-4182-7998-dee7-b8a2558dc369', 'e046854e-406c-37f4-6607-19a9ba8426fc']
    # print(contentuuidconvert("e046854e-406c-37f4-6607-19a9ba8426fc"))

    for skin in single_skins:
        for weapons_list in data_weapons['data']:
            for skin1 in weapons_list['skins']:
                if skin in str(skin1):
                    # print(skin1)
                    if skin1['displayIcon'] == None:
                        # print("test")
                        for chromas in skin1["chromas"]:
                            single_skins_images.append(chromas["displayIcon"])
                        single_skins_tiers_uuids.append(skin1['contentTierUuid'])
                    else:
                        single_skins_images.append(skin1['displayIcon'])
                        single_skins_tiers_uuids.append(skin1['contentTierUuid'])

    # print(single_skins_images)
    headers = {
        'X-Riot-Entitlements-JWT': entitlements_token,
        'Authorization': f'Bearer {access_token}',
        'X-Riot-ClientVersion': getVersion(),
        "X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
    }

    data = requests.get("https://pd.EU.a.pvp.net/store/v1/offers/", headers=headers)

    offers_data = data.json()

    for row in content_data:
        for row_small in content_data[row]:
            if skins_data["FeaturedBundle"]["Bundle"]["DataAssetID"].upper() in str(row_small):
                r_bundle_data = requests.get(f"https://valorant-api.com/v1/bundles/{row_small['ID']}")
                bundle_data = r_bundle_data.json()
                # print(f"Your featured bundle is {row_small['Name']} - {bundle_data['data']['displayIcon']} - {skins_data['FeaturedBundle']['BundleRemainingDurationInSeconds']}.")
                bundle_name = row_small['Name']
                bundle_image = bundle_data['data']['displayIcon']

    daily_reset = skins_data["SkinsPanelLayout"]["SingleItemOffersRemainingDurationInSeconds"]

    skin_counter = 0
    # print("Your daily item shop is: ")
    for skin in single_skins:
        for row in content_data:
            for row_small in content_data[row]:
                if skin.upper() in str(row_small):
                    # print(f"    {row_small['Name']} - {priceconvert(skin)}VP"
                    #       f" - {single_skins_images[skin_counter]}"
                    #       f" - {contentuuidconvert(single_skins_tiers_uuids[skin_counter])['displayIcon']}"
                    #       f" - {contentuuidconvert(single_skins_tiers_uuids[skin_counter])['highlightColor']}"
                    #       f" - {daily_reset}")
                    if skin_counter == 0:
                        skin1_name = row_small['Name']
                        skin1_image = single_skins_images[skin_counter]
                        skin1_price = priceconvert(skin, offers_data)
                        skin1_color = contentuuidconvert(single_skins_tiers_uuids[skin_counter])['highlightColor']
                    elif skin_counter == 1:
                        skin2_name = row_small['Name']
                        skin2_image = single_skins_images[skin_counter]
                        skin2_price = priceconvert(skin, offers_data)
                        skin2_color = contentuuidconvert(single_skins_tiers_uuids[skin_counter])['highlightColor']
                    elif skin_counter == 2:
                        skin3_name = row_small['Name']
                        skin3_image = single_skins_images[skin_counter]
                        skin3_price = priceconvert(skin, offers_data)
                        skin3_color = contentuuidconvert(single_skins_tiers_uuids[skin_counter])['highlightColor']
                    elif skin_counter == 3:
                        skin4_name = row_small['Name']
                        skin4_image = single_skins_images[skin_counter]
                        skin4_price = priceconvert(skin, offers_data)
                        skin4_color = contentuuidconvert(single_skins_tiers_uuids[skin_counter])['highlightColor']
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
        "skin1_color":skin1_color,
        "skin2_name": skin2_name,
        "skin2_image": skin2_image,
        "skin2_price": skin2_price,
        "skin2_color": skin2_color,
        "skin3_name": skin3_name,
        "skin3_image": skin3_image,
        "skin3_price": skin3_price,
        "skin3_color": skin3_color,
        "skin4_name": skin4_name,
        "skin4_image": skin4_image,
        "skin4_price": skin4_price,
        "skin4_color": skin4_color,
    }

    return skins_list

@client.event
async def on_message(message):
    global username
    global password
    if message.author != client.user:
        if message.content.lower().startswith('!shop'):
            user_data = username_to_data(username, password)
            access_token = user_data[0]
            entitlements_token = user_data[1]
            user_id = user_data[2]
            skin_data = skins(entitlements_token, access_token, user_id)
            embed = discord.Embed(title=skin_data["bundle_name"])
            embed.set_image(url=skin_data["bundle_image"])
            await message.channel.send(embed=embed)
            try:
                embed = discord.Embed(title=f"{skin_data['skin1_name']} costs {skin_data['skin1_price']}", colour=hex_convert(skin_data['skin1_color']))
                embed.set_image(url=skin_data["skin1_image"])
                await message.channel.send(embed=embed)
                embed = discord.Embed(title=f"{skin_data['skin2_name']} costs {skin_data['skin2_price']}", colour=hex_convert(skin_data['skin2_color']))
                embed.set_image(url=skin_data["skin2_image"])
                await message.channel.send(embed=embed)
                embed = discord.Embed(title=f"{skin_data['skin3_name']} costs {skin_data['skin3_price']}", colour=hex_convert(skin_data['skin3_color']))
                embed.set_image(url=skin_data["skin3_image"])
                await message.channel.send(embed=embed)
                embed = discord.Embed(title=f"{skin_data['skin4_name']} costs {skin_data['skin4_price']}", colour=hex_convert(skin_data['skin4_color']))
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
            # r = requests.get(f'https://pd.EU.a.pvp.net/store/v2/storefront/{user_id}', headers=headers)
            #
            # skins_data = r.json()
            # single_skins = skins_data["SkinsPanelLayout"]["SingleItemOffers"]
            #
            # headers = {
            #     'X-Riot-Entitlements-JWT': entitlements_token,
            #     'Authorization': f'Bearer {access_token}',
            #     'X-Riot-ClientVersion': getVersion(),
            #     "X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
            # }
            #
            # r = requests.get(f'https://shared.EU.a.pvp.net/content-service/v2/content/', headers=headers)

            # content_data = r.json()

            # with open("assets.txt", "w") as file:
            #     file.write(str(data))

            # all_weapons = requests.get("https://valorant-api.com/v1/weapons")
            # data_weapons = all_weapons.json()
            #
            # single_skins_images = []
            # single_skins_tiers_uuids = []

            # ['12683d76-48d7-84a3-4e09-6985794f0445', 'e046854e-406c-37f4-6607-19a9ba8426fc', '60bca009-4182-7998-dee7-b8a2558dc369', 'e046854e-406c-37f4-6607-19a9ba8426fc']
            # print(contentuuidconvert("e046854e-406c-37f4-6607-19a9ba8426fc"))

            # for skin in single_skins:
            #     for weapons_list in data_weapons['data']:
            #         for skin1 in weapons_list['skins']:
            #             if skin in str(skin1):
            #                 # print(skin1)
            #                 if skin1['displayIcon'] == None:
            #                     # print("test")
            #                     for chromas in skin1["chromas"]:
            #                         single_skins_images.append(chromas["displayIcon"])
            #                     single_skins_tiers_uuids.append(skin1['contentTierUuid'])
            #                 else:
            #                     single_skins_images.append(skin1['displayIcon'])
            #                     single_skins_tiers_uuids.append(skin1['contentTierUuid'])

            # print(single_skins_images)


# headers = {
#         'X-Riot-Entitlements-JWT': entitlements_token,
#         'Authorization': f'Bearer {access_token}',
#         'X-Riot-ClientVersion': getVersion(),
#         "X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
#     }
#
#
# data = requests.get("https://pd.EU.a.pvp.net/store/v1/offers/", headers=headers)
#
# offers_data = data.json()
#
#
#
# for row in content_data:
#     for row_small in content_data[row]:
#         if skins_data["FeaturedBundle"]["Bundle"]["DataAssetID"].upper() in str(row_small):
#             r_bundle_data = requests.get(f"https://valorant-api.com/v1/bundles/{row_small['ID']}")
#             bundle_data = r_bundle_data.json()
#             # print(f"Your featured bundle is {row_small['Name']} - {bundle_data['data']['displayIcon']} - {skins_data['FeaturedBundle']['BundleRemainingDurationInSeconds']}.")
#             bundle_name = row_small['Name']
#             bundle_image = bundle_data['data']['displayIcon']
#
# daily_reset = skins_data["SkinsPanelLayout"]["SingleItemOffersRemainingDurationInSeconds"]
#
#
# skin_counter = 0
# # print("Your daily item shop is: ")
# for skin in single_skins:
#     for row in content_data:
#         for row_small in content_data[row]:
#             if skin.upper() in str(row_small):
#                 # print(f"    {row_small['Name']} - {priceconvert(skin)}VP"
#                 #       f" - {single_skins_images[skin_counter]}"
#                 #       f" - {contentuuidconvert(single_skins_tiers_uuids[skin_counter])['displayIcon']}"
#                 #       f" - {contentuuidconvert(single_skins_tiers_uuids[skin_counter])['highlightColor']}"
#                 #       f" - {daily_reset}")
#                 if skin_counter == 0:
#                     skin1_name = row_small['Name']
#                     skin1_image = single_skins_images[skin_counter]
#                     skin1_price = priceconvert(skin)
#                     skin1_color = contentuuidconvert(single_skins_tiers_uuids[skin_counter])['highlightColor']
#                 elif skin_counter == 1:
#                     skin2_name = row_small['Name']
#                     skin2_image = single_skins_images[skin_counter]
#                     skin2_price = priceconvert(skin)
#                     skin2_color = contentuuidconvert(single_skins_tiers_uuids[skin_counter])['highlightColor']
#                 elif skin_counter == 2:
#                     skin3_name = row_small['Name']
#                     skin3_image = single_skins_images[skin_counter]
#                     skin3_price = priceconvert(skin)
#                     skin3_color = contentuuidconvert(single_skins_tiers_uuids[skin_counter])['highlightColor']
#                 elif skin_counter == 3:
#                     skin4_name = row_small['Name']
#                     skin4_image = single_skins_images[skin_counter]
#                     skin4_price = priceconvert(skin)
#                     skin4_color = contentuuidconvert(single_skins_tiers_uuids[skin_counter])['highlightColor']
#                 skin_counter += 1
#
#
#
#
#
#
#
# if daily_reset >= 3600:
#     daily_reset_in_hr = round(daily_reset / 3600, 0)
#     # print(f"Daily shop items resets in {int(daily_reset_in_hr)} hours.")
# else:
#     daily_reset_in_minutes = round(daily_reset / 60, 2)
#     # print(f"Daily shop items resets in {daily_reset_in_minutes} minutes.")
#
#
#
#
#
# webhook(True, valorant_points, radianite_points, bundle_name, bundle_image, 0, 0)
# webhook(False, valorant_points, radianite_points, skin1_name, skin1_image, skin1_price, skin1_color)
# webhook(False, valorant_points, radianite_points, skin2_name, skin2_image, skin2_price, skin2_color)
# webhook(False, valorant_points, radianite_points, skin3_name, skin3_image, skin3_price, skin3_color)
# webhook(False, valorant_points, radianite_points, skin4_name, skin4_image, skin4_price, skin4_color)



client.run(bot_token)
