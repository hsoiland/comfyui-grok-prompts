if __package__:
    from .ponyxl import PonyXL
    from .flux import Flux
    from .wan import Wan
    from .audio import Audio
else:
    from ponyxl import PonyXL
    from flux import Flux
    from wan import Wan
    from audio import Audio

NODE_CLASS_MAPPINGS = {
    "PonyXL": PonyXL,
    "Flux": Flux,
    "Wan": Wan,
    "Audio": Audio
}
print("\033[34mGrok Prompts: \033[92mLoaded\033[0m")
