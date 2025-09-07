import os

# set the URLs of each website, we use the demo sites as an example
os.environ[
    "SHOPPING"
] = "https://agenttrickydps.vercel.app/shopping"
os.environ[
    "HEALTH"
] = "https://agenttrickydps.vercel.app/health"
os.environ[
    "NEWS"
] = "https://agenttrickydps.vercel.app/news"
os.environ[
    "LINKEDIN"
] = "https://agenttrickydps.vercel.app/linkedin"
os.environ[
    "SPOTIFY"
] = "https://agenttrickydps.vercel.app/spotify"
os.environ[
    "WIKIPEDIA"
] = "https://agenttrickydps.vercel.app/wiki"
print("Done setting up URLs")