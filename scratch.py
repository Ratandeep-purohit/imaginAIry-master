import os
from imaginairy.utils.model_manager import open_weights
from imaginairy.weight_management.conversion import cast_weights
from imaginairy.weight_management.utils import COMPONENT_NAMES, FORMAT_NAMES, MODEL_NAMES
from imaginairy.utils.downloads import download_huggingface_weights, normalize_diffusers_repo_url

base_url = "https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5/tree/main/"
unet_weights_path = download_huggingface_weights(base_url=base_url, sub="unet")
print("Downloaded unet weights to:", unet_weights_path)
unet_weights = open_weights(unet_weights_path, device="cpu")
print("Keys in unet_weights before cast:", len(unet_weights.keys()))
print("Sample keys:", list(unet_weights.keys())[:5])

unet_weights_cast = cast_weights(
    source_weights=unet_weights,
    source_model_name=MODEL_NAMES.SD15,
    source_component_name=COMPONENT_NAMES.UNET,
    source_format=FORMAT_NAMES.DIFFUSERS,
    dest_format=FORMAT_NAMES.REFINERS,
)
print("Keys in unet_weights after cast:", len(unet_weights_cast.keys()))
