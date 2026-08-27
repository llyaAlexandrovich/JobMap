from hashlib import sha256



def generate_provider_codename_sha256(provider_name: str):
    return sha256(provider_name.encode()).hexdigest()[:24]
