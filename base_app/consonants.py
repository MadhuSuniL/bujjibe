from typing import Final, List, Dict, Tuple

class SpaceTopics:
    __SPACE_TOPICS : Final = [
        ('all', "Everything About Space"),
        ("galaxies", "Galaxies"),
        ("planets", "Planets"),
        ("stars", "Stars"),
        ("exoplanets", "Exoplanets"),
        ("black_holes", "Black Holes"),
        ("nebulae", "Nebulae"),
        ("cosmic_microwave_background", "Cosmic Microwave Background"),
        ("dark_matter", "Dark Matter"),
        ("dark_energy", "Dark Energy"),
        ("asteroids", "Asteroids"),
        ("comets", "Comets"),
        ("space_exploration", "Space Exploration"),
        ("alien_life", "Alien Life"),
        ("wormholes", "Wormholes"),
        ("supernovae", "Supernovae"),
        ("quasars", "Quasars"),
        ("pulsars", "Pulsars"),
        ("the_big_bang", "The Big Bang"),
        ("gravitational_waves", "Gravitational Waves"),
        ("solar_system", "Solar System"),
        ("space_weather", "Space Weather"),
        ("milky_way", "The Milky Way"),
        ("interstellar_medium", "Interstellar Medium"),
        ("space_time", "Space-Time"),
        ("cosmic_rays", "Cosmic Rays"),
        ("hubble_telescope", "The Hubble Space Telescope"),
        ("rogue_planets", "Rogue Planets"),
        ("gamma_ray_bursts", "Gamma-Ray Bursts"),
        ("fermi_paradox", "The Fermi Paradox"),
        ("drake_equation", "The Drake Equation"),
        ("voyager_missions", "Voyager Missions"),
        ("multiverse", "The Multiverse"),
        ("dark_galaxies", "Dark Galaxies"),
        ("cosmic_strings", "Cosmic Strings"),
        ("space_telescopes", "Space Telescopes"),
        ("international_space_station", "International Space Station (ISS)"),
        ("spacecraft_propulsion", "Spacecraft Propulsion"),
        ("meteorites", "Meteorites"),
        ("space_colonization", "Space Colonization"),
    ]
    
    @classmethod
    def get_space_topic_label_by_topic_slug(cls, topic_slug: str):
        for slug, label in cls.__SPACE_TOPICS:
            if slug == topic_slug:
                return label
        return None

    @classmethod
    def get_space_topics(cls):
        return cls.__SPACE_TOPICS

class SourceTypes:
    __SOURCES: Final = [
        {"id": "gemma-7b-it", "owner": "Google", "name": "Gemma 7B IT"},
        {"id": "llama3-8b-8192", "owner": "Meta", "name": "LLaMA 3 8B 8192"},
        {"id": "llama-3.1-8b-instant", "owner": "Meta", "name": "LLaMA 3.1 8B Instant"},
        {"id": "llama3-groq-70b-8192-tool-use-preview", "owner": "Groq", "name": "LLaMA 3 Groq 70B 8192 Tool Use Preview"},
        {"id": "llama3-70b-8192", "owner": "Meta", "name": "LLaMA 3 70B 8192"},
        {"id": "llama3-groq-8b-8192-tool-use-preview", "owner": "Groq", "name": "LLaMA 3 Groq 8B 8192 Tool Use Preview"},
        {"id": "llama-guard-3-8b", "owner": "Meta", "name": "LLaMA Guard 3 8B"},
        {"id": "llama-3.1-70b-versatile", "owner": "Meta", "name": "LLaMA 3.1 70B Versatile"},
        {"id": "mixtral-8x7b-32768", "owner": "Mistral AI", "name": "Mixtral 8x7B 32768"},
        {"id": "gemma2-9b-it", "owner": "Google", "name": "Gemma 2 9B IT"},
        {"id": "pretrained_pdf_files", "owner": "bujji", "name": "Pretrained PDF Files"}
    ]

    @classmethod
    def get_raw_sources(cls) -> Dict[str, List[Dict[str, str]]]:
        return cls.__SOURCES
            
    @classmethod
    def get_sources(cls) -> Dict[str, List[Dict[str, str]]]:
        grouped_sources = {}
        for source in cls.__SOURCES:
            owner = source["owner"]
            if owner not in grouped_sources:
                grouped_sources[owner] = []
            grouped_sources[owner].append({
                "id": source["id"],
                "name": source["name"]
            })
        return grouped_sources
    

def get_format(self):
    return {
        "user": "",       # The identifier or username of the user making the query
        "topic_id": "",      # The main subject of the user's query (e.g., Galaxies, Planets, Stars)
        "query": "",   # The specific query about the chosen topic
        "source_id": ""      # The source for generating the answer (e.g., Pretrained PDF Files, Mistral, LLaMA 3)
    }
    