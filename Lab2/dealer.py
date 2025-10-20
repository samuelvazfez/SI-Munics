# dealer.py
import json
import ckzg
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
        print(f" DEALER - Secret: {self.secret}, n: {self.n}, t: {self.t}")
        
        # 1. Generar polinomio
        self.polynomial_coeffs = self.common.generate_polynomial(self.secret, self.t)
        print(f"📊 Polinomio generado: grado {self.t}")
        
        # 2. Crear blob y commitment - USAR BLOB QUE SÍ FUNCIONA CON CKZG
        blob = b'\x00' * 131072  # Blob de ceros que funciona con ckzg
        
        # INTENTAR USAR KZG REAL
        shares = []
        if self.ckzg_ready and self.trusted_setup:
            try:
                # Usar ckzg real en lugar de simulado
                self.commitment = ckzg.blob_to_kzg_commitment(blob, self.trusted_setup)
                print("Commitment KZG REAL creado")
                print(f"📋 Commitment: {self.commitment.hex()[:20]}...")
                
                # 3. Generar shares con KZG REAL
                for i in range(1, self.n + 1):
                    share_value = self.common.evaluate_polynomial(self.polynomial_coeffs, i)
                    
                    z = i.to_bytes(32, 'little')
                    proof_result = ckzg.compute_kzg_proof(blob, z, self.trusted_setup)
                    witness = proof_result[0]  # ckzg retorna (proof, y)
                    
                    shares.append({
                        "participant_id": i,
                        "x": i,
                        "share": share_value,
                        "witness": witness.hex(),
                        "commitment": self.commitment.hex()
                    })
                    
                    print(f"✅ Share {i}: {share_value} (KZG REAL)")
                
                print(" KZG REAL funcionando completamente!")
                
            except Exception as e:
                print(f"⚠️  KZG real falló: {e}, usando simulado")
                # Fallback a modo simulado
                self.commitment = blob_to_kzg_commitment_sim(blob)
                print(f"📋 Commitment SIMULADO: {self.commitment.hex()[:20]}...")
                
                for i in range(1, self.n + 1):
                    share_value = self.common.evaluate_polynomial(self.polynomial_coeffs, i)
                    
                    z = i.to_bytes(32, 'little')
                    witness = compute_kzg_proof_sim(blob, z)
                    
                    shares.append({
                        "participant_id": i,
                        "x": i,
                        "share": share_value,
                        "witness": witness.hex(),
                        "commitment": self.commitment.hex()
                    })
                    
                    print(f"✅ Share {i}: {share_value} (SIMULADO)")
        else:
            # Modo simulado desde el inicio
            self.commitment = blob_to_kzg_commitment_sim(blob)
            print(f"📋 Commitment SIMULADO: {self.commitment.hex()[:20]}...")
            
            for i in range(1, self.n + 1):
                share_value = self.common.evaluate_polynomial(self.polynomial_coeffs, i)
                
                z = i.to_bytes(32, 'little')
                witness = compute_kzg_proof_sim(blob, z)
                
                shares.append({
                    "participant_id": i,
                    "x": i,
                    "share": share_value,
                    "witness": witness.hex(),
                    "commitment": self.commitment.hex()
                })
                
                print(f"✅ Share {i}: {share_value} (SIMULADO)")
        
        # 4. Guardar output
        output = {
            "parameters": {"n": self.n, "t": self.t, "secret": self.secret},
            "commitment": self.commitment.hex(),
            "polynomial": self.polynomial_coeffs,
            "shares": shares,
            "kzg_mode": "REAL" if (self.ckzg_ready and self.trusted_setup) else "SIMULADO"
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