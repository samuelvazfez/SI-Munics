# dealer.py
import json
from trusted_setup import setup_ckzg, get_trusted_setup, blob_to_kzg_commitment_sim, compute_kzg_proof_sim
from vss_common import VSSCommon

class VSSDealer:
    def __init__(self, n: int, t: int, secret: int):
        if t > 4:
            raise ValueError("Grado máximo es 4")
        
        self.n = n
        self.t = t
        self.secret = secret
        self.common = VSSCommon()
        
        self.ckzg_ready = setup_ckzg()
        self.trusted_setup = get_trusted_setup()
        
        self.polynomial_coeffs = None
        self.commitment = None
    
    def distribute_secret(self):
        print(f"🎯 DEALER - Secret: {self.secret}, n: {self.n}, t: {self.t}")
        
        # 1. Generar polinomio
        self.polynomial_coeffs = self.common.generate_polynomial(self.secret, self.t)
        print(f"📊 Polinomio generado: grado {self.t}")
        
        # 2. Crear blob y commitment
        blob = self.common.polynomial_to_blob(self.polynomial_coeffs)
        
        if self.ckzg_ready and self.trusted_setup:
            self.commitment = blob_to_kzg_commitment_sim(blob)  # Cambiar por real si funciona
        else:
            self.commitment = blob_to_kzg_commitment_sim(blob)
        
        print(f"📋 Commitment: {self.commitment.hex()[:20]}...")
        
        # 3. Generar shares
        shares = []
        for i in range(1, self.n + 1):
            share_value = self.common.evaluate_polynomial(self.polynomial_coeffs, i)
            
            z = i.to_bytes(32, 'little')
            if self.ckzg_ready and self.trusted_setup:
                witness = compute_kzg_proof_sim(blob, z)  # Cambiar por real si funciona
            else:
                witness = compute_kzg_proof_sim(blob, z)
            
            shares.append({
                "participant_id": i,
                "x": i,
                "share": share_value,
                "witness": witness.hex(),
                "commitment": self.commitment.hex()
            })
            
            print(f"✅ Share {i}: {share_value}")
        
        # 4. Guardar output
        output = {
            "parameters": {"n": self.n, "t": self.t, "secret": self.secret},
            "commitment": self.commitment.hex(),
            "polynomial": self.polynomial_coeffs,
            "shares": shares
        }
        
        with open("dealer_output.json", "w") as f:
            json.dump(output, f, indent=2)
        
        print("💾 dealer_output.json guardado")
        return output

def main():
    dealer = VSSDealer(n=5, t=2, secret=42)
    dealer.distribute_secret()

if __name__ == "__main__":
    main()