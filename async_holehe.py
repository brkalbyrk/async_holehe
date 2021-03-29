import trio
import httpx
import random
import importlib
import json
import pkgutil
from holehe.modules.shopping.amazon import amazon
from holehe.localuseragent import ua
from colorama import Fore, Style


def import_submodules(package, recursive=True):
    """Get all the holehe submodules"""
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + "." + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


def get_functions(modules, args=None):
    """Transform the modules objects to functions"""
    websites = []

    for module in modules:
        if len(module.split(".")) > 3:
            modu = modules[module]
            site = module.split(".")[-1]
            if (
                "adobe" not in str(modu.__dict__[site])
                and "mail_ru" not in str(modu.__dict__[site])
                and "odnoklassniki" not in str(modu.__dict__[site])
            ):
                websites.append(modu.__dict__[site])
            else:
                websites.append(modu.__dict__[site])
    return websites


async def launch_module(module, email, client, out):
    data = {
        "aboutme": "about.me",
        "adobe": "adobe.com",
        "amazon": "amazon.com",
        "anydo": "any.do",
        "archive": "archive.org",
        "armurerieauxerre": "armurerie-auxerre.com",
        "atlassian": "atlassian.com",
        "babeshows": "babeshows.co.uk",
        "badeggsonline": "badeggsonline.com",
        "biosmods": "bios-mods.com",
        "biotechnologyforums": "biotechnologyforums.com",
        "bitmoji": "bitmoji.com",
        "blablacar": "blablacar.com",
        "blackworldforum": "blackworldforum.com",
        "blip": "blip.fm",
        "blitzortung": "forum.blitzortung.org",
        "bluegrassrivals": "bluegrassrivals.com",
        "bodybuilding": "bodybuilding.com",
        "buymeacoffee": "buymeacoffee.com",
        "cambridgemt": "discussion.cambridge-mt.com",
        "caringbridge": "caringbridge.org",
        "chinaphonearena": "chinaphonearena.com",
        "clashfarmer": "clashfarmer.com",
        "codecademy": "codecademy.com",
        "codeigniter": "forum.codeigniter.com",
        "codepen": "codepen.io",
        "coroflot": "coroflot.com",
        "cpaelites": "cpaelites.com",
        "cpahero": "cpahero.com",
        "cracked_to": "cracked.to",
        "crevado": "crevado.com",
        "deliveroo": "deliveroo.com",
        "demonforums": "demonforums.net",
        "devrant": "devrant.com",
        "diigo": "diigo.com",
        "discord": "discord.com",
        "docker": "docker.com",
        "dominosfr": "dominos.fr",
        "ebay": "ebay.com",
        "ello": "ello.co",
        "envato": "envato.com",
        "eventbrite": "eventbrite.com",
        "evernote": "evernote.com",
        "fanpop": "fanpop.com",
        "firefox": "firefox.com",
        "flickr": "flickr.com",
        "freelancer": "freelancer.com",
        "freiberg": "drachenhort.user.stunet.tu-freiberg.de",
        "garmin": "garmin.com",
        "github": "github.com",
        "google": "google.com",
        "gravatar": "gravatar.com",
        "imgur": "imgur.com",
        "instagram": "instagram.com",
        "issuu": "issuu.com",
        "koditv": "forum.kodi.tv",
        "komoot": "komoot.com",
        "laposte": "laposte.fr",
        "lastfm": "last.fm",
        "lastpass": "lastpass.com",
        "mail_ru": "mail.ru",
        "mybb": "community.mybb.com",
        "myspace": "myspace.com",
        "nattyornot": "nattyornotforum.nattyornot.com",
        "naturabuy": "naturabuy.fr",
        "ndemiccreations": "forum.ndemiccreations.com",
        "nextpvr": "forums.nextpvr.com",
        "nike": "nike.com",
        "odampublishing": "forum.odampublishing.com",
        "odnoklassniki": "ok.ru",
        "office365": "office365.com",
        "onlinesequencer": "onlinesequencer.net",
        "parler": "parler.com",
        "patreon": "patreon.com",
        "pinterest": "pinterest.com",
        "plurk": "plurk.com",
        "pornhub": "pornhub.com",
        "protonmail": "protonmail.ch",
        "quora": "quora.com",
        "raidforums": "raidforums.com",
        "rambler": "rambler.ru",
        "redtube": "redtube.com",
        "replit": "repl.it",
        "rocketreach": "rocketreach.co",
        "samsung": "samsung.com",
        "seoclerks": "seoclerks.com",
        "sevencups": "7cups.com",
        "smule": "smule.com",
        "snapchat": "snapchat.com",
        "sporcle": "sporcle.com",
        "spotify": "spotify.com",
        "strava": "strava.com",
        "taringa": "taringa.net",
        "teamtreehouse": "teamtreehouse.com",
        "tellonym": "tellonym.me",
        "thecardboard": "thecardboard.org",
        "therianguide": "forums.therian-guide.com",
        "thevapingforum": "thevapingforum.com",
        "treasureclassifieds": "forum.treasureclassifieds.com",
        "tumblr": "tumblr.com",
        "tunefind": "tunefind.com",
        "twitter": "twitter.com",
        "venmo": "venmo.com",
        "vivino": "vivino.com",
        "voxmedia": "voxmedia.com",
        "vrbo": "vrbo.com",
        "vsco": "vsco.co",
        "wattpad": "wattpad.com",
        "wordpress": "wordpress",
        "xing": "xing.com",
        "xvideos": "xvideos.com",
        "yahoo": "yahoo.com",
    }
    try:
        await module(email, client, out)
    except:
        name = str(module).split("<function ")[1].split(" ")[0]
        out.append(
            {"name": name, "domain": data[name], "emailrecovery": None, "exists": False}
        )


def print_result(data, email, websites):

    print(email)
    for results in data:
        if results["exists"] == True:
            print(f"{Fore.GREEN}[+] {results['domain']} {Style.RESET_ALL}")


async def main():

    http_proxy = [http.strip() for http in open("http_proxy.txt").readlines()]
    email_list = [email.strip() for email in open("assets.txt").readlines()]
    modules = import_submodules("holehe.modules")

    for email in email_list:
        websites = get_functions(modules, email)
        proxy_index = random.randint(0, len(http_proxy) - 1)
        proxy_dict = {
            "http": "http://" + http_proxy[proxy_index]
        }
        # print(f"Requested IP: {http_proxy[proxy_index]}")
        out = []
        client = httpx.AsyncClient(proxies=proxy_dict)

        async with trio.open_nursery() as nursery:
            for website in websites:
                nursery.start_soon(launch_module, website, email, client, out)

        out = sorted(out, key=lambda i: i["name"])
        print_result(out, email, websites)
        await client.aclose()


if __name__ == "__main__":
    trio.run(main)
