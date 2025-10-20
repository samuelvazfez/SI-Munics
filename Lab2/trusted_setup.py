# trusted_setup.py
import ckzg
import hashlib
import os

_trusted_setup = None
_loaded = False

def setup_ckzg():
    global _trusted_setup, _loaded
    if _loaded:
        return _trusted_setup is not None

    try:
        print("Configurando ckzg...")
        
        if not os.path.exists("trusted_setup.txt"):
            print("❌ trusted_setup.txt no encontrado")
            return False
        
        _trusted_setup = ckzg.load_trusted_setup("trusted_setup.txt", 4)
        _loaded = True
        
        print("ckzg configurado (grado 4)")
        return True
        
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return False

def get_trusted_setup():
    return _trusted_setup

def blob_to_kzg_commitment_sim(blob):
    return hashlib.sha256(blob).digest()[:48]

def compute_kzg_proof_sim(blob, z):
    return hashlib.sha256(blob + z).digest()[:48]

def verify_kzg_proof_sim(commitment, z, y, proof):
    return True