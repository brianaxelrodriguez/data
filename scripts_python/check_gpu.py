import torch
import torch_directml

def check_hardware():
    print("--- Verificación de Hardware para IA ---")
    print(f"Hilos lógicos del Ryzen 9: {torch.get_num_threads()}")

    try:
        # En las versiones nuevas se usa así:
        count = torch_directml.device_count()
        print(f"Cantidad de dispositivos DirectML: {count}")
        
        if count > 0:
            for i in range(count):
                print(f"✅ GPU {i} Detectada: {torch_directml.device_name(i)}")
            
            # Asignar el dispositivo
            dml = torch_directml.device()
            print(f"🚀 Usando dispositivo: {dml}")
            
            # Test de tensores
            x = torch.ones(3, 3).to(dml)
            print("🔥 Test de Tensores en GPU exitoso.")
        else:
            print("❌ No se encontraron GPUs compatibles con DirectML.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_hardware()