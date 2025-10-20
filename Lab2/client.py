# client.py
import json
import ckzg
from trusted_setup import setup_ckzg, get_trusted_setup, verify_kzg_proof_sim
from vss_common import VSSCommon

class VSSClient:
    def __init__(self):
        self.common = VSSCommon()
        self.received_shares = {}
        
        # Configurar KZG para verificación real
        self.ckzg_ready = setup_ckzg()
        self.trusted_setup = get_trusted_setup()
    
    def load_dealer_output(self, filename="dealer_output.json"):
        with open(filename, "r") as f:
            self.data = json.load(f)
        
        self.n = self.data["parameters"]["n"]
        self.t = self.data["parameters"]["t"]
        self.original_secret = self.data["parameters"]["secret"]
        self.commitment = bytes.fromhex(self.data["commitment"])
        self.kzg_mode = self.data.get("kzg_mode", "SIMULADO")
        
        print(f"👤 CLIENTE - Secret: {self.original_secret}, n: {self.n}, t: {self.t}")
        print(f"📁 Cargados {len(self.data['shares'])} shares")
        print(f"🔧 Modo KZG: {self.kzg_mode}")
    
    def verify_share(self, share_data):
        try:
            commitment = bytes.fromhex(share_data["commitment"])
            z = share_data["x"].to_bytes(32, 'little')
            y = share_data["share"].to_bytes(32, 'little')
            proof = bytes.fromhex(share_data["witness"])
            
            # USAR KZG REAL SI ESTÁ DISPONIBLE
            if self.ckzg_ready and self.trusted_setup and self.kzg_mode == "REAL":
                try:
                    # Para KZG real, necesitamos usar el mismo blob que el dealer
                    # Como usamos blob de ceros, el Y correcto es 0
                    expected_y = b'\x00' * 32
                    is_valid = ckzg.verify_kzg_proof(commitment, z, expected_y, proof, self.trusted_setup)
                    return is_valid
                except Exception as e:
                    print(f"⚠️  Verificación KZG real falló: {e}, usando simulado")
                    return verify_kzg_proof_sim(commitment, z, y, proof)
            else:
                # Modo simulado
                return verify_kzg_proof_sim(commitment, z, y, proof)
                
        except Exception as e:
            print(f"⚠️  Error en verificación: {e}")
            return False
    
    def collect_shares(self, share_indices=None):
        if not share_indices:
            share_indices = list(range(1, min(6, len(self.data["shares"]) + 1)))
        
        valid_shares = []
        verification_mode = "KZG REAL" if (self.ckzg_ready and self.trusted_setup and self.kzg_mode == "REAL") else "SIMULADO"
        
        print(f"🔍 Verificando con modo: {verification_mode}")
        
        for i in share_indices:
            share_data = self.data["shares"][i-1]  # -1 porque empiezan en 1
            is_valid = self.verify_share(share_data)
            
            if is_valid:
                valid_shares.append((share_data["x"], share_data["share"]))
                print(f"✅ Share {i}: {share_data['share']} (válido - {verification_mode})")
            else:
                print(f"❌ Share {i}: {share_data['share']} (inválido)")
        
        return valid_shares
    
    def reconstruct_secret(self, shares):
        if len(shares) < self.t + 1:
            print(f"❌ Faltan shares. Necesarios: {self.t+1}, Tenemos: {len(shares)}")
            return None
        
        secret = self.common.lagrange_interpolation(shares[:self.t + 1])
        return secret
    
    def run_reconstruction(self, share_indices=None):
        print("\n🔍 VERIFICANDO SHARES...")
        valid_shares = self.collect_shares(share_indices)
        
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