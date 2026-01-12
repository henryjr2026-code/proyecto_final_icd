import matplotlib.pyplot as plt
import numpy as np
import treecko as tk


def percent(precio_producto,trabajadores):
    axisas=list(trabajadores.keys())
    dicc=tk.porciento(precio_producto,trabajadores)
    ordenadas=[dicc[sector] for sector in axisas]

    plt.figure(figsize=(12, 6))  

    plt.bar(
         axisas, ordenadas,
    width=0.6,          
    edgecolor='black',  
    color="#FF1F1F",    
    alpha=1           
)


    plt.title("Porcentaje que Representa del Salario  la Canasta Básica")
    plt.ylabel("Porcentaje del Salario (%)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout() 

    return plt.show()
 



def pastel(datos_gasto, umbral=5):
    """
    Crea un gráfico de pastel agrupando productos minoritarios en 'Otros'.
    
    Args:
        datos_gasto (dict)
        umbral (float): Porcentaje mínimo para mostrar el producto individualmente.
    """
    total = sum(datos_gasto.values())
    datos_filtrados = {}
    otros_total = 0

    for producto, valor in datos_gasto.items():
        porcentaje = (valor / total) * 100
        
        if porcentaje < umbral:
            otros_total += valor
        else:
            datos_filtrados[producto] = valor

    # Añadir la categoría 'Otros' si hay productos acumulados
    if otros_total > 0:
        datos_filtrados["Otros"] = otros_total


    cantidades = list(datos_filtrados.values())
    labels = list(datos_filtrados.keys())

    plt.figure(figsize=(10, 7))
    plt.pie(
        cantidades,
        labels=labels,
        autopct='%1.1f%%', 
        startangle=20,
        colors=plt.cm.Paired.colors 
    )
    
    plt.title("Distribución del Gasto por Producto en la Canasta Básica")

    return plt.show()



def barras_agrupadas(datos_mundo):
    paises = list(datos_mundo.keys())
    
    salarios = []
    canastas = []
    
    for p in paises:
        info = datos_mundo[p]
        s = info.get("salario") or info.get("salario ") or info.get("salario minimo")
        c = info.get("canasta")
        salarios.append(s)
        canastas.append(c)

    
    x = np.arange(len(paises)) 
    width = 0.35               

    fig, ax = plt.subplots(figsize=(12, 7))
    
    rects1 = ax.bar(x - width/2, salarios, width, label='Salario Mensual', color='#2ecc71')
    rects2 = ax.bar(x + width/2, canastas, width, label='Costo Canasta', color='#e74c3c')

    # Añadir textos, títulos y etiquetas
    ax.set_ylabel('Valor en USD')
    ax.set_title('Comparativa Internacional: Salario Mínimo vs. Canasta Básica')
    ax.set_xticks(x)
    ax.set_xticklabels(paises)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    return plt.show()


def hung(datos_mundo):
    axisas=list(datos_mundo.keys())
    ordenadas=list(datos_mundo.values())
    plt.figure(figsize=(10,5))
    plt.bar(
        axisas,ordenadas,
        color="#FF3D3D",
        edgecolor="black",
        alpha=0.9
    )
    plt.title("Porcentaje del Salario Mínimo destinado a la Canasta Básica", fontsize=16, pad=20)
    plt.ylabel("Porcentaje del Salario (%)", fontsize=10)
    plt.xlabel("Países", fontsize=12)
    
 

    plt.tight_layout()
    for i, v in enumerate(ordenadas):
       plt.text(axisas[i], v + 3, str(v), ha='center', fontsize=9)
    
    return plt.show()


def unidades_salarios(salario):
    
    axisas=list(tk.promedios.keys())
    ordenadas=list(tk.calcular_unidades_por_salario(salario, tk.promedios).values())
    fig, ax = plt.subplots(figsize=(9, 5))
    
     
    colores = plt.cm.Blues(np.linspace(0.8, 0.4, len(axisas)))
    bars = ax.bar(axisas, ordenadas, color=colores, edgecolor='black', alpha=0.8)
    
    # Añadir los números arriba de las barras
    ax.bar_label(bars, padding=1, fontsize=9 )
    plt.bar(
        axisas, ordenadas, color="#6EFA98D1", edgecolor="black"

    )
    plt.xticks(rotation=45, ha="right")
    plt.title("Unidades/libras de productos que se pueden comprar con el salario mínimo")
    plt.tight_layout()
    return plt.show()


