# client.py
import json
from trusted_setup import verify_kzg_proof_sim
from vss_common import VSSCommon

class VSSClient:
    def __init__(self):
        self.common = VSSCommon()
        self.received_shares = {}
    
    def load_dealer_output(self, filename="dealer_output.json"):
        with open(filename, "r") as f:
            self.data = json.load(f)
        
        self.n = self.data["parameters"]["n"]
        self.t = self.data["parameters"]["t"]
        self.original_secret = self.data["parameters"]["secret"]
        self.commitment = bytes.fromhex(self.data["commitment"])
        
        print(f"👤 CLIENTE - Secret: {self.original_secret}, n: {self.n}, t: {self.t}")
        print(f"📁 Cargados {len(self.data['shares'])} shares")
    
    def verify_share(self, share_data):
        try:
            commitment = bytes.fromhex(share_data["commitment"])
            z = share_data["x"].to_bytes(32, 'little')
            y = share_data["share"].to_bytes(32, 'little')
            proof = bytes.fromhex(share_data["witness"])
            
            # En modo real usaríamos verify_kzg_proof con trusted_setup
            is_valid = verify_kzg_proof_sim(commitment, z, y, proof)
            return is_valid
        except:
            return False
    
    def collect_shares(self, share_indices=None):
        if not share_indices:
            share_indices = list(range(1, min(6, len(self.data["shares"]) + 1)))
        
        valid_shares = []
        for i in share_indices:
            share_data = self.data["shares"][i-1]  # -1 porque empiezan en 1
            if self.verify_share(share_data):
                valid_shares.append((share_data["x"], share_data["share"]))
                print(f"✅ Share {i}: {share_data['share']} (válido)")
            else:
                print(f"❌ Share {i}: {share_data['share']} (inválido)")
        
        return valid_shares
    
    def reconstruct_secret(self, shares):
        if len(shares) < self.t + 1:
            print(f"❌ Faltan shares. Necesarios: {self.t+1}, Tenemos: {len(shares)}")
            return None
        
        secret = self.common.lagrange_interpolation(shares[:self.t + 1])
        return secret
    
    def run_reconstruction(self):
        print("\n🔍 VERIFICANDO SHARES...")
        valid_shares = self.collect_shares()
        
        print(f"\n🎯 RECONSTRUYENDO...")
        print(f"   Shares válidos: {len(valid_shares)}")
        print(f"   Umbral necesario: {self.t + 1}")
        
        if len(valid_shares) >= self.t + 1:
            reconstructed = self.reconstruct_secret(valid_shares)
            print(f"   Secreto reconstruido: {reconstructed}")
            print(f"   Secreto original: {self.original_secret}")
            print(f"   {'✅ COINCIDEN' if reconstructed == self.original_secret else '❌ NO COINCIDEN'}")
            return reconstructed
        else:
            print("   ❌ No se puede reconstruir - shares insuficientes")
            return None

def main():
    client = VSSClient()
    client.load_dealer_output()
    client.run_reconstruction()

if __name__ == "__main__":
    main()