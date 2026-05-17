import json
from prompts.mentoring_prompts import STEP04_RESOURCES, get_system_prompt


def build_prompt(topic: str, roadmap: list, learning_type: str = "hana") -> tuple:
    roadmap_text = json.dumps(roadmap, ensure_ascii=False, indent=2)
    user = STEP04_RESOURCES.format(topic=topic, roadmap=roadmap_text)
    return get_system_prompt(learning_type), user
