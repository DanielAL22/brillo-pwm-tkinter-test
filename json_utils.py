import json

def leer_json():
    try:
        with open("config_brillo.json", "r") as f:
            config = json.load(f)
            brillo = config.get("brillo", 100)  # valor por defecto
    except FileNotFoundError:
        brillo = 100  # Valor por defecto si no existe el archivo (100 brillo maximo)

    return brillo



def escribir_json(brillo):
    # Guardar distancia máxima en cm
    config = {"brillo": brillo}

    with open("config_brillo.json", "w") as f:
        json.dump(config, f)



if __name__ == "__main__":
    escribir_json(50)
    print(f"Brillo configurado: {leer_json()} cm")