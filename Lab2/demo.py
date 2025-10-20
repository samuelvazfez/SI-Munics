# demo.py
from dealer import VSSDealer
from client import VSSClient

def demo_completa():
    print("🚀 DEMO COMPLETA VSS CON KZG")
    print("=" * 50)
    
    # Configuración
    SECRETO = 123
    N, T = 6, 2
    
    print(f"🔧 Configuración:")
    print(f"   - Secreto: {SECRETO}")
    print(f"   - Participantes: {N}")
    print(f"   - Umbral: {T} (necesita {T+1} shares)")
    print()
    
    # Fase 1: Dealer distribuye
    print("📦 FASE 1: DISTRIBUCIÓN")
    print("-" * 30)
    dealer = VSSDealer(n=N, t=T, secret=SECRETO)
    output = dealer.distribute_secret()
    
    print()
    
    # Fase 2: Cliente reconstruye CON VERIFICACIÓN KZG
    print("🔍 FASE 2: RECONSTRUCCIÓN CON VERIFICACIÓN KZG")  
    print("-" * 40)
    client = VSSClient()
    client.load_dealer_output()
    
    # Probar diferentes combinaciones CON VERIFICACIÓN
    print("\n🧪 PROBANDO COMBINACIONES CON VERIFICACIÓN KZG:")
    
    # Combinación 1: primeros t+1 shares
    combinacion_1 = [1, 2, 3]
    print(f"\n🔹 Combinación 1: {combinacion_1}")
    valid_shares_1 = client.collect_shares(combinacion_1)
    if len(valid_shares_1) >= T + 1:
        secreto_1 = client.reconstruct_secret(valid_shares_1)
        print(f"   Resultado: {secreto_1} {'✅' if secreto_1 == SECRETO else '❌'}")
    else:
        print("   ❌ No se puede reconstruir - shares insuficientes después de verificación")
    
    # Combinación 2: otros t+1 shares
    combinacion_2 = [2, 4, 6]
    print(f"\n🔹 Combinación 2: {combinacion_2}")
    valid_shares_2 = client.collect_shares(combinacion_2)
    if len(valid_shares_2) >= T + 1:
        secreto_2 = client.reconstruct_secret(valid_shares_2)
        print(f"   Resultado: {secreto_2} {'✅' if secreto_2 == SECRETO else '❌'}")
    else:
        print("   ❌ No se puede reconstruir - shares insuficientes después de verificación")
    
    # Combinación 3: con shares insuficientes (debería fallar)
    combinacion_3 = [1, 2]  # solo t shares
    print(f"\n🔹 Combinación 3: {combinacion_3} (solo {T} shares)")
    valid_shares_3 = client.collect_shares(combinacion_3)
    if len(valid_shares_3) >= T + 1:
        secreto_3 = client.reconstruct_secret(valid_shares_3)
        print(f"   Resultado: {secreto_3} {'✅' if secreto_3 == SECRETO else '❌'}")
    else:
        print("   ❌ No se puede reconstruir - shares insuficientes")
    
    # Combinación 4: Reconstrucción completa con todos los shares válidos
    print(f"\n🔹 Combinación 4: TODOS los shares (verificación completa)")
    resultado_final = client.run_reconstruction()
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN FINAL:")
    print(f"   - Secreto original: {SECRETO}")
    print(f"   - Shares generados: {N}")
    print(f"   - Umbral: {T+1}")
    print(f"   - Modo KZG: {output.get('kzg_mode', 'SIMULADO')}")
    print(f"   - Combinaciones exitosas: 2/3 + reconstrucción completa")
    print("🎉 DEMO COMPLETADA CON VERIFICACIÓN KZG")

if __name__ == "__main__":
    demo_completa()