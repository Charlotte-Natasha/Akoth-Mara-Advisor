# wildlife personality traits and fun facts
import random

# --- Fun Facts ---
FUN_FACTS = [
    "🦁 Lions sleep up to 20 hours a day!",
    "🦒 A giraffe's tongue is about 20 inches long and purple!",
    "🐘 Elephants can recognize themselves in mirrors!",
    "🦓 Zebra stripes are unique to each individual!",
    "🦏 A rhino's horn is made of keratin!",
    "🦛 Hippos can hold their breath underwater for up to 5 minutes!",
    "🐆 Cheetahs can accelerate from 0 to 60 mph in 3 seconds!",
    "🦅 African fish eagles can spot prey from over 3 miles away!",
    "🦌 Wildebeest babies can stand and run within minutes of birth!",
    "🌳 Acacia trees communicate via chemical signals!",
]

# --- Quirky fallback intros ---
FALLBACK_INTROS = [
    "🦁 Hmm, tricky one! My database is taking a nap in the savanna...",
    "🦒 Great question! Let me stretch my neck and look around...",
    "🐘 I'm rummaging through my memory (elephants never forget!)...",
    "🦓 That's not in my herd of knowledge, but here's what I know...",
    "🌿 Ooh, that's outside my usual watering hole, but I can share this...",
]

# --- Animal Prefixes ---
ANIMAL_PREFIXES = {
    "lion": "🦁 Ah, the king of the jungle! ",
    "elephant": "🐘 Elephants are incredible! ",
    "giraffe": "🦒 Those long-necked beauties! ",
    "zebra": "🦓 The striped wonders of the savanna! ",
    "cheetah": "🐆 The fastest land animal on Earth! ",
    "rhino": "🦏 Magnificent armored giants! ",
    "hippo": "🦛 The river horse of Africa! ",
    "wildebeest": "🦌 The great migrators! ",
}

# --- Functions ---
def get_animal_prefix(query: str) -> str:
    query_lower = query.lower()
    for animal, prefix in ANIMAL_PREFIXES.items():
        if animal in query_lower:
            return prefix
    return ""

def add_fun_fact(response: str, chance: float = 0.3) -> str:
    if random.random() < chance:
        fun_fact = random.choice(FUN_FACTS)
        return f"{response}\n\n✨ Fun fact: {fun_fact}"
    return response

def get_quirky_intro() -> str:
    return random.choice(FALLBACK_INTROS)
