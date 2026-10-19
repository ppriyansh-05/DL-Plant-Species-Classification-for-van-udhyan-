import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Model and Storage Settings
MODEL_FILENAME = "best_van_udyan_top15.keras"
LOCAL_MODEL_PATH = Path(os.getenv("LOCAL_MODEL_PATH", MODEL_FILENAME))
CLASS_MAPPING_PATH = Path(os.getenv("CLASS_MAPPING_PATH", "class_mapping.json"))

# Supabase Settings (Optional, safe server-side retrieval)
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")  # Anon or Service Role (Server-side ONLY)
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "models")
SUPABASE_MODEL_PATH = os.getenv("SUPABASE_MODEL_PATH", "best_van_udyan_top15.keras")

# Image Preprocessing Settings (EfficientNetB0)
IMG_HEIGHT = 224
IMG_WIDTH = 224

# Confidence Warning Threshold
CONFIDENCE_THRESHOLD = 0.40  # Low confidence alert if top prediction is below 40%

# Common names and zone details for Van Udyan Top-15
SPECIES_INFO = {
    "Alstonia_scholaris": {
        "common_name": "Saptaparni / Devil's Tree",
        "marathi_name": "सप्तपर्णी (Saptaparni)",
        "family": "Apocynaceae",
        "ecological_role": "Evergreen native canopy tree, medicinal bark, pollinator host"
    },
    "Azadirachta_indica": {
        "common_name": "Neem",
        "marathi_name": "कडुनिंब (Kadu Neem)",
        "family": "Meliaceae",
        "ecological_role": "Air purifier, natural antimicrobial, drought-hardy pioneer"
    },
    "Bauhinia_variegata": {
        "common_name": "Kachnar / Orchid Tree",
        "marathi_name": "कांचन (Kanchan)",
        "family": "Fabaceae",
        "ecological_role": "Nitrogen-fixing ornamental, fragrant blossom, nectar source"
    },
    "Bombax_ceiba": {
        "common_name": "Semal / Silk Cotton Tree",
        "marathi_name": "सावर / काटेसावर (Kate Savar)",
        "family": "Malvaceae",
        "ecological_role": "Massive deciduous tree, spring nectar hub for birds and bats"
    },
    "Cordia_dichotoma": {
        "common_name": "Lasora / Indian Cherry / Bhokar",
        "marathi_name": "भोकर (Bhokar)",
        "family": "Boraginaceae",
        "ecological_role": "Edible mucilaginous fruit, key seasonal avian food resource"
    },
    "Dalbergia_latifolia": {
        "common_name": "Indian Rosewood / Shisham",
        "marathi_name": "शिसव (Shisav)",
        "family": "Fabaceae",
        "ecological_role": "High-value timber legume, nitrogen fixation, canopy shelter"
    },
    "Erythrina_variegata": {
        "common_name": "Indian Coral Tree / Pangara",
        "marathi_name": "पंगारा (Pangara)",
        "family": "Fabaceae",
        "ecological_role": "Vivid scarlet flowers, crucial food source for returning migratory birds"
    },
    "Ficus_benghalensis": {
        "common_name": "Banyan Tree / Vad",
        "marathi_name": "वड (Vad)",
        "family": "Moraceae",
        "ecological_role": "Keystone biodiversity tree, extensive aerial roots, year-round fig crop"
    },
    "Ficus_religiosa": {
        "common_name": "Peepal / Sacred Fig",
        "marathi_name": "पिंपळ (Pimpal)",
        "family": "Moraceae",
        "ecological_role": "Oxygen emitter, keystone epiphyte host, frugivore sustenance"
    },
    "Mangifera_indica": {
        "common_name": "Mango / Aam",
        "marathi_name": "आंबा (Amba)",
        "family": "Anacardiaceae",
        "ecological_role": "Dense evergreen shade, major pollinator attraction, indigenous cultivars"
    },
    "Pongamia_pinnata": {
        "common_name": "Karanj / Pongame Oiltree",
        "marathi_name": "करंज (Karanj)",
        "family": "Fabaceae",
        "ecological_role": "Hardy drought legume, biofuel seed oil, robust urban roadside barrier"
    },
    "Syzygium_cumini": {
        "common_name": "Jamun / Black Plum",
        "marathi_name": "जांभूळ (Jambhul)",
        "family": "Myrtaceae",
        "ecological_role": "Moisture-retaining riparian tree, antioxidant fruit, wildlife attractor"
    },
    "Tectona_grandis": {
        "common_name": "Teak / Sagwan",
        "marathi_name": "सागवान (Sagwan)",
        "family": "Lamiaceae",
        "ecological_role": "Deciduous dry-forest staple, extensive root network preventing erosion"
    },
    "Terminalia_bellirica": {
        "common_name": "Baheda / Bibhitaki",
        "marathi_name": "बेहडा (Behada)",
        "family": "Combretaceae",
        "ecological_role": "Triphala component, heavy nectar blossom, hollow-nesting habitat"
    },
    "Terminalia_catappa": {
        "common_name": "Indian Almond / Deshi Badam",
        "marathi_name": "बदाम (Deshi Badam)",
        "family": "Combretaceae",
        "ecological_role": "Pagoda-tier horizontal branches, salt-tolerant, bat and squirrel fodder"
    }
}
