SUPPORTED_PLATFORMS = [
    "tiktok.com", "vm.tiktok.com", 
    "instagram.com", "www.instagram.com", "instagr.am",
    "youtu.be", "youtube.com", 
    "vk.com", "vk.ru"
]

def is_supported_url(url: str) -> bool:
    url_lower = url.lower()
    
    if any(domain in url_lower for domain in ["tiktok.com", "vm.tiktok.com"]):
        return True
    
    return any(domain in url_lower for domain in SUPPORTED_PLATFORMS)