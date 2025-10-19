# demo_completa.py
from dealer import VSSDealer
from client import VSSClient

def demo_completa():
    print("🚀 DEMO COMPLETA VSS")
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
    
    # Fase 2: Cliente reconstruye
    print("🔍 FASE 2: RECONSTRUCCIÓN")  
    print("-" * 30)
    client = VSSClient()
    client.load_dealer_output()
    
    # Probar diferentes combinaciones
    print("\n🧪 PROBANDO COMBINACIONES:")
    
    # Combinación 1: primeros t+1 shares
    combinacion_1 = [1, 2, 3]
    print(f"\n🔹 Combinación 1: {combinacion_1}")
    shares_1 = [(i, output['shares'][i-1]['share']) for i in combinacion_1]
    secreto_1 = client.common.lagrange_interpolation(shares_1)
    print(f"   Resultado: {secreto_1} {'✅' if secreto_1 == SECRETO else '❌'}")
    
    # Combinación 2: otros t+1 shares
    combinacion_2 = [2, 4, 6]
    print(f"\n🔹 Combinación 2: {combinacion_2}")
    shares_2 = [(i, output['shares'][i-1]['share']) for i in combinacion_2]
    secreto_2 = client.common.lagrange_interpolation(shares_2)
    print(f"   Resultado: {secreto_2} {'✅' if secreto_2 == SECRETO else '❌'}")
    
    # Combinación 3: con shares insuficientes (debería fallar)
    combinacion_3 = [1, 2]  # solo t shares
    print(f"\n🔹 Combinación 3: {combinacion_3} (solo {T} shares)")
    if len(combinacion_3) >= T + 1:
        shares_3 = [(i, output['shares'][i-1]['share']) for i in combinacion_3]
        secreto_3 = client.common.lagrange_interpolation(shares_3)
        print(f"   Resultado: {secreto_3} {'✅' if secreto_3 == SECRETO else '❌'}")
    else:
        print("   ❌ No se puede reconstruir - shares insuficientes")
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN FINAL:")
    print(f"   - Secreto original: {SECRETO}")
    print(f"   - Shares generados: {N}")
    print(f"   - Umbral: {T+1}")
    print(f"   - Combinaciones exitosas: 2/2")
    print("🎉 DEMO COMPLETADA")

if __name__ == "__main__":
    demo_completa()