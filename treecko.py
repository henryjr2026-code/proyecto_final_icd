#bibliotecas a usar
import json
import os

  #función para recorrer los productos y sus precios

def cargar_productos(carpeta):   
   
    productos = []

    #listar los archivos dentro de la carpeta
    for archivo in os.listdir(carpeta):
            
            #construcción de la ruta
            ruta = os.path.join(carpeta, archivo)          
            #abrir y leer cada archivo
            with open(ruta, "r", encoding="utf-8") as f:     
                datos = json.load(f)
            
            #extraemos la informacion de cada archivo
            mipyme_id = datos['id']
             
            for producto in datos["producto"]:
                productos.append({
                    "mipyme_id": mipyme_id,
                    "nombre": producto["nombre"],
                    "precio": producto["precio"]
                }) 
             
           
    return productos
productos=cargar_productos("mipymes")

#definir función promedio para calcular el promedio de los precios de los productos

def promedio(producto):
     
    acumulado={}   
    conteo={}   
    for i in producto:
         nombre= i["nombre"]
         precio=i["precio"]
         

         if nombre not in acumulado:
              acumulado[nombre]=0
              conteo[nombre]=0

         acumulado[nombre]+= precio
         conteo[nombre]+=1
  
    promedios={}
    for nombre in acumulado:
         promedios[nombre]= round(acumulado[nombre]/conteo[nombre],2)


    return promedios

promedios= promedio(productos)


def cargar_salarios(ruta_archivo):
     
     try:
         with open(ruta_archivo, "r", encoding="utf-8") as f:     
             datos = json.load(f)
             # Asumimos que los salarios están anidados en una clave "salarios"
             return datos.get("salarios", {}) 
     except FileNotFoundError:
         print(f"Advertencia: Archivo {ruta_archivo} no encontrado.")
         return {}
     except json.JSONDecodeError:
         print(f"Advertencia: Error de formato en {ruta_archivo}.")
         return {}
     
salarios_=cargar_salarios("otras_fuentes/salarios.json")
salarios=salarios_[0]


def cargar_tasa(ruta_archivo):
    """
    Carga las tasas de cambio desde el archivo JSON especificado.
   
    """
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
            # Retornamos el diccionario que contiene 'mlc' y 'usd'
            return datos
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar la tasa en {ruta_archivo}: {e}")
        return {}
    
           

def porciento(producto,salarios):
     """
     Calcula el porciento que representa el precio de un producto de los salarios

     Args: 
         pruducto(int): precio del producto
         salarios(dict): 
     Returns:
         dict:Diccionario:{ "sector": porciento}
     """
     resultado={}   
     for sector, salario in salarios.items():
          if salario > 0:
               porcentaje = (producto/salario)*100
               resultado[sector]=round(porcentaje,2)
      
     return resultado

def costo_promedio(nombre_producto,promedios):
     """
     Calcula el promedio de un producto específico
     
     Args:
         nombre_producto(string): "producto"
         promedios(dict): coste promedio de los productos
     Returns:
        dict: Diccionario: {"producto": costo promedio}    
     """
     return promedios.get(nombre_producto)
    
 
canasta_básica={
     "hígado_pollo": 10,      
     "cartón_huevo":1 ,
     "frijoles":6,      

     "arroz":8,         
     "coditos":2,      
     "espagueti":2,     
     "puré":2,          

     "perritos":1,
     "aceite":1,        
     "leche":1.        
}

def precio_total(canasta,lista_promedios):
     precio=0
     for i in canasta.keys():
          precio+= canasta[i]*lista_promedios[i]

     return round(precio,2)

precio_canasta=precio_total(canasta_básica,promedios)


def cargar_servicios(carpeta):    
     """
     Carga la informacion acerca de los servicios que ofrece cada mipyme
    
     """
     servicios_info=[]      
     for archivo in os.listdir(carpeta):            
            ruta = os.path.join(carpeta, archivo)           

            with open(ruta, "r", encoding="utf-8") as f:     
                datos = json.load(f)           
            mipyme_id = datos['id']            
            servicios_info.append({
                "id": mipyme_id,
                "domicilio": datos.get('domicilio', False),
                "transferencia": datos.get('transferencia', False)
            })

     return servicios_info      

servicios=cargar_servicios("mipymes")


def contar_servicios(servicios):
     '''
     Cuenta la cantidad de mipymes que ofece cada servicio
         
     '''
     conteo = {
        "total_mipymes": len(servicios),
        "con_domicilio": 0,
        "sin_domicilio": 0,
        "con_transferencia": 0,
        "sin_transferencia": 0,
        "ambos_servicios": 0
    }
    
     for mipyme in servicios:
        # Contamos Domicilio
        if mipyme['domicilio'] is True:
            conteo["con_domicilio"] += 1
        else:
            conteo["sin_domicilio"] += 1
        # Contamos Transferencia
        if mipyme['transferencia'] is True:
            conteo["con_transferencia"] += 1
        else:
            conteo["sin_transferencia"] += 1           
        # Contamos la intersección (Ambos servicios)
        if mipyme['domicilio'] is True and mipyme['transferencia'] is True:
             conteo["ambos_servicios"] += 1
             
     return conteo

servicios_info=contar_servicios(servicios)




def gasto_por_producto(canasta, lista_promedios):
    """
    Calcula el dinero total gastado en cada producto de la canasta.
    
    Args:
        canasta (dict): informacion de la canasta basica 
        lista_promedios (dict): coste promedio de los productos
        
    Returns:
        dict: Diccionario {"producto": dinero_gastado}.
    """
    gasto_individual = {}   
    for producto, cantidad in canasta.items():

        precio_unitario = lista_promedios.get(producto, 0)
        
        total_producto = cantidad * precio_unitario
        gasto_individual[producto] = round(total_producto, 2)
        
    return gasto_individual

gasto=gasto_por_producto(canasta_básica,promedios)
tasa=cargar_tasa("otras_fuentes/tasa_de_cambio.json")


     
def convertir_a_divisa(dato, valor_tasa):
    """
    Convierte valores de CUP a la divisa seleccionada.
    Funciona con un número (como precio_canasta) o un diccionario (como salarios).
    """
    if valor_tasa <= 0:
        return dato
        
  
    if isinstance(dato, dict):
        resultado = {}
        for clave, valor in dato.items():
            resultado[clave] = round(valor / valor_tasa, 2)
        return resultado
    
 
    return round(dato / valor_tasa, 2)

usd=tasa.get("usd",1)
mlc=tasa.get("mlc",1)




def cargar_datos_mundo(ruta_archivo):
    """Carga los datos de salarios y canastas internacionales."""
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            return json.load(f) 
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def calcular_porcentaje_mundo(datos_mundo):
    """Calcula qué porcentaje del salario representa la canasta en cada país."""
    comparativa = {}
    for pais, info in datos_mundo.items():
        # Buscamos la clave del salario 
        salario = info.get("salario")
        canasta = info.get("canasta")
        
        if salario and canasta and salario > 0:
            porcentaje = (canasta / salario) * 100
            comparativa[pais] = round(porcentaje, 2)
            
    return comparativa

datos_mundo=cargar_datos_mundo("otras_fuentes/canasta_basica_salario_mundo.json")

mundo=calcular_porcentaje_mundo(datos_mundo)


def calcular_unidades_por_salario(salario, precios_promedio):
    """
    Calcula cuántas unidades de cada producto se pueden comprar 
    con un salario determinado.
    """
    unidades = {}
    for producto, precio in precios_promedio.items():
        # Evitamos división por cero si algún precio está mal
        if precio > 0:
            unidades[producto] = round(salario // precio)
    return unidades




print(salarios)