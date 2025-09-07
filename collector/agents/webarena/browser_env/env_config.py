# websites domain
import os

SHOPPING = os.environ.get("SHOPPING", "")
HEALTH = os.environ.get("HEALTH", "")
NEWS = os.environ.get("NEWS", "")
LINKEDIN = os.environ.get("LINKEDIN", "")
SPOTIFY = os.environ.get("SPOTIFY", "")
WIKIPEDIA = os.environ.get("WIKIPEDIA", "")

# assert (
#     SHOPPING
#     and HEALTH
#     and NEWS
#     and LINKEDIN
#     and SPOTIFY
#     and WIKIPEDIA
# ), (
#     f"Please setup the URLs to each site. Current: \n"
#     + f"Shopping: {SHOPPING}\n"
#     + f"Health: {HEALTH}\n"
#     + f"News: {NEWS}\n"
#     + f"Linkedin: {LINKEDIN}\n"
#     + f"Spotify: {SPOTIFY}\n"
#     + f"Wikipedia: {WIKIPEDIA}\n"
# )

# Not using this
# ACCOUNTS = {
#     "reddit": {"username": "MarvelsGrantMan136", "password": "test1234"},
#     "gitlab": {"username": "byteblaze", "password": "hello1234"},
#     "shopping": {
#         "username": "emma.lopez@gmail.com",
#         "password": "Password.123",
#     },
#     "shopping_admin": {"username": "admin", "password": "admin1234"},
#     "shopping_site_admin": {"username": "admin", "password": "admin1234"},
# }

URL_MAPPINGS = {
    SHOPPING: "https://agenttrickydps.vercel.app/shopping",
    HEALTH: "https://agenttrickydps.vercel.app/health",
    NEWS: "https://agenttrickydps.vercel.app/news",
    LINKEDIN: "https://agenttrickydps.vercel.app/linkedin",
    SPOTIFY: "https://agenttrickydps.vercel.app/spotify",
    WIKIPEDIA: "https://agenttrickydps.vercel.app/wiki",
}
