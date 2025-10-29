if __package__:
    from .ponyxl import PonyXL
    from .flux import Flux
    from .wan import Wan
else:
    from ponyxl import PonyXL
    from flux import Flux
    from wan import Wan

NODE_CLASS_MAPPINGS = {
    "PonyXL": PonyXL,
    "Flux": Flux,
    "Wan": Wan
}
print("\033[34mGrok Prompts: \033[92mLoaded\033[0m")
