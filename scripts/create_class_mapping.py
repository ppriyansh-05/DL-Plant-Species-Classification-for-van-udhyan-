import json
from pathlib import Path

# The exact 15 classes in alphabetical order matching Keras flow_from_directory / image_dataset_from_directory
TOP15_CLASSES = [
    "Alstonia_scholaris",
    "Azadirachta_indica",
    "Bauhinia_variegata",
    "Bombax_ceiba",
    "Cordia_dichotoma",
    "Dalbergia_latifolia",
    "Erythrina_variegata",
    "Ficus_benghalensis",
    "Ficus_religiosa",
    "Mangifera_indica",
    "Pongamia_pinnata",
    "Syzygium_cumini",
    "Tectona_grandis",
    "Terminalia_bellirica",
    "Terminalia_catappa"
]

class_mapping = {str(i): name for i, name in enumerate(TOP15_CLASSES)}

with open("class_mapping.json", "w") as f:
    json.dump(class_mapping, f, indent=2)

print("Generated class_mapping.json with 15 classes successfully.")
