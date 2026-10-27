import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base directory (project root is parent of backend)
BASE_DIR = Path(__file__).resolve().parent.parent

# Model and Storage Settings
MODEL_FILENAME = "best_van_udyan_top15.keras"
LOCAL_MODEL_PATH = Path(os.getenv("LOCAL_MODEL_PATH", str(BASE_DIR / MODEL_FILENAME)))
CLASS_MAPPING_PATH = Path(os.getenv("CLASS_MAPPING_PATH", str(BASE_DIR / "class_mapping.json")))
METRICS_PATH = Path(os.getenv("METRICS_PATH", str(BASE_DIR / "evaluation_summary.json")))

# Supabase Settings (Optional, safe server-side retrieval)
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")  # Anon or Service Role (Server-side ONLY)
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "models")
SUPABASE_MODEL_PATH = os.getenv("SUPABASE_MODEL_PATH", "best_van_udyan_top15.keras")

# Image Preprocessing Settings (EfficientNetB0)
IMG_HEIGHT = 224
IMG_WIDTH = 224
MAX_FILE_SIZE_BYTES = 8 * 1024 * 1024  # 8 MB
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}

# Confidence Warning Threshold
CONFIDENCE_THRESHOLD = 0.40  # Low confidence alert if top prediction is below 40%

# CORS Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Species taxonomy and metadata including Pune Van Udyan zones
SPECIES_INFO = {
    "Alstonia_scholaris": {
        "common_name": "Saptaparni / Devil's Tree",
        "marathi_name": "सप्तपर्णी (Saptaparni)",
        "family": "Apocynaceae",
        "zones": ["Zone 1", "Zone 3"],
        "primary_zone": "Zone 1 & 3",
        "ecological_role": "Evergreen native canopy tree, medicinal bark, pollinator host",
        "foliage": "Whorled glossy dark leaves",
        "blooming_season": "October to December"
    },
    "Azadirachta_indica": {
        "common_name": "Neem",
        "marathi_name": "कडुनिंब (Kadu Neem)",
        "family": "Meliaceae",
        "zones": ["Zone 1", "Zone 2", "Zone 3"],
        "primary_zone": "Zone 1, 2 & 3",
        "ecological_role": "Air purifier, natural antimicrobial, drought-hardy pioneer",
        "foliage": "Pinnate serrated leaflets",
        "blooming_season": "March to May"
    },
    "Bauhinia_variegata": {
        "common_name": "Kachnar / Orchid Tree",
        "marathi_name": "कांचन (Kanchan)",
        "family": "Fabaceae",
        "zones": ["Zone 2"],
        "primary_zone": "Zone 2",
        "ecological_role": "Nitrogen-fixing ornamental, fragrant blossom, nectar source",
        "foliage": "Distinct two-lobed butterfly leaves",
        "blooming_season": "February to April"
    },
    "Bombax_ceiba": {
        "common_name": "Semal / Silk Cotton Tree",
        "marathi_name": "सावर / काटेसावर (Kate Savar)",
        "family": "Malvaceae",
        "zones": ["Zone 1", "Zone 2", "Zone 3"],
        "primary_zone": "Zone 1, 2 & 3",
        "ecological_role": "Massive deciduous tree, spring nectar hub for birds and bats",
        "foliage": "Palmate compound leaves, spiny trunk",
        "blooming_season": "January to March"
    },
    "Cordia_dichotoma": {
        "common_name": "Lasora / Indian Cherry / Bhokar",
        "marathi_name": "भोकर (Bhokar)",
        "family": "Boraginaceae",
        "zones": ["Zone 3"],
        "primary_zone": "Zone 3",
        "ecological_role": "Edible mucilaginous fruit, key seasonal avian food resource",
        "foliage": "Broad ovate leaves, glabrous above",
        "blooming_season": "March to May"
    },
    "Dalbergia_latifolia": {
        "common_name": "Indian Rosewood / Shisham",
        "marathi_name": "शिसव (Shisav)",
        "family": "Fabaceae",
        "zones": ["Zone 3"],
        "primary_zone": "Zone 3",
        "ecological_role": "High-value timber legume, nitrogen fixation, canopy shelter",
        "foliage": "Odd-pinnate leaves with rounded leaflets",
        "blooming_season": "August to September"
    },
    "Erythrina_variegata": {
        "common_name": "Indian Coral Tree / Pangara",
        "marathi_name": "पंगारा (Pangara)",
        "family": "Fabaceae",
        "zones": ["Zone 1"],
        "primary_zone": "Zone 1",
        "ecological_role": "Vivid scarlet flowers, crucial food source for returning migratory birds",
        "foliage": "Trifoliate leaves with rhomboid leaflets",
        "blooming_season": "February to May"
    },
    "Ficus_benghalensis": {
        "common_name": "Banyan Tree / Vad",
        "marathi_name": "वड (Vad)",
        "family": "Moraceae",
        "zones": ["Zone 3"],
        "primary_zone": "Zone 3",
        "ecological_role": "Keystone biodiversity tree, extensive aerial roots, year-round fig crop",
        "foliage": "Thick leathery elliptic leaves",
        "blooming_season": "Year-round fruiting"
    },
    "Ficus_religiosa": {
        "common_name": "Peepal / Sacred Fig",
        "marathi_name": "पिंपळ (Pimpal)",
        "family": "Moraceae",
        "zones": ["Zone 1", "Zone 3"],
        "primary_zone": "Zone 1 & 3",
        "ecological_role": "Continuous oxygen emitter, keystone epiphyte host, frugivore sustenance",
        "foliage": "Heart-shaped cordate leaves with extended drip tip",
        "blooming_season": "Year-round fruiting"
    },
    "Mangifera_indica": {
        "common_name": "Mango / Aam",
        "marathi_name": "आंबा (Amba)",
        "family": "Anacardiaceae",
        "zones": ["Zone 1", "Zone 3"],
        "primary_zone": "Zone 1 & 3",
        "ecological_role": "Dense evergreen shade, major pollinator attraction, indigenous cultivars",
        "foliage": "Lanceolate dark green leaves",
        "blooming_season": "January to March"
    },
    "Pongamia_pinnata": {
        "common_name": "Karanj / Pongame Oiltree",
        "marathi_name": "करंज (Karanj)",
        "family": "Fabaceae",
        "zones": ["Zone 1", "Zone 2", "Zone 3"],
        "primary_zone": "Zone 1, 2 & 3",
        "ecological_role": "Hardy drought legume, biofuel seed oil, robust urban roadside barrier",
        "foliage": "Pinnate glossy leaves with pink-tinted new flush",
        "blooming_season": "April to June"
    },
    "Syzygium_cumini": {
        "common_name": "Jamun / Black Plum",
        "marathi_name": "जांभूळ (Jambhul)",
        "family": "Myrtaceae",
        "zones": ["Zone 2", "Zone 3"],
        "primary_zone": "Zone 2 & 3",
        "ecological_role": "Moisture-retaining riparian tree, antioxidant fruit, wildlife attractor",
        "foliage": "Opposite oblong leaves with turpentine scent when crushed",
        "blooming_season": "March to May"
    },
    "Tectona_grandis": {
        "common_name": "Teak / Sagwan",
        "marathi_name": "सागवान (Sagwan)",
        "family": "Lamiaceae",
        "zones": ["Zone 2", "Zone 3"],
        "primary_zone": "Zone 2 & 3",
        "ecological_role": "Deciduous dry-forest staple, extensive root network preventing erosion",
        "foliage": "Huge ovate leaves with stellate hairs",
        "blooming_season": "June to September"
    },
    "Terminalia_bellirica": {
        "common_name": "Baheda / Bibhitaki",
        "marathi_name": "बेहडा (Behada)",
        "family": "Combretaceae",
        "zones": ["Zone 3"],
        "primary_zone": "Zone 3",
        "ecological_role": "Triphala component, heavy nectar blossom, hollow-nesting habitat",
        "foliage": "Broadly elliptic leaves clustered at branch ends",
        "blooming_season": "March to May"
    },
    "Terminalia_catappa": {
        "common_name": "Indian Almond / Deshi Badam",
        "marathi_name": "बदाम (Deshi Badam)",
        "family": "Combretaceae",
        "zones": ["Zone 1", "Zone 3"],
        "primary_zone": "Zone 1 & 3",
        "ecological_role": "Pagoda-tier horizontal branches, salt-tolerant, bat and squirrel fodder",
        "foliage": "Large obovate leaves that turn scarlet red before falling",
        "blooming_season": "February to May"
    }
}
