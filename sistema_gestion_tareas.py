import heapq
import json
from datetime import datetime

class SistemaTareas:
    def __init__(self, archivo_datos="tareas.json"):
        self.heap = []
        self.tareas_completadas = []
        self.archivo_datos = archivo_datos
        self._cargar_datos()

    def _cargar_datos(self):
        try:
            with open(self.archivo_datos, 'r') as archivo:
                datos = json.load(archivo)
                self.heap = [(t['prioridad'], t['fecha'], t['nombre'], t['dependencias']) for t in datos['pendientes']]
                self.tareas_completadas = datos['completadas']
                heapq.heapify(self.heap)
        except FileNotFoundError:
            pass

    def _guardar_datos(self):
        datos = {
            'pendientes': [{'prioridad': p, 'fecha': f, 'nombre': n, 'dependencias': d} for p, f, n, d in self.heap],
            'completadas': self.tareas_completadas
        }
        with open(self.archivo_datos, 'w') as archivo:
            json.dump(datos, archivo, indent=4)

    def _es_ejecutable(self, dependencias):
        return all(dep in [t[2] for t in self.tareas_completadas] for dep in dependencias)

    def añadir_tarea(self, nombre, prioridad, dependencias=None, fecha=None):
        if not nombre or not isinstance(prioridad, int):
            raise ValueError("El nombre no puede estar vacío y la prioridad debe ser un número entero.")
        if dependencias is None:
            dependencias = []
        if fecha is None:
            fecha = datetime.now().isoformat()
        tarea = (prioridad, fecha, nombre, dependencias)
        heapq.heappush(self.heap, tarea)
        self._guardar_datos()

    def mostrar_tareas(self):
        print("\nTareas Pendientes:")
        if not self.heap:
            print("No hay tareas pendientes.")
        else:
            for prioridad, fecha, nombre, dependencias in sorted(self.heap):
                estado = "Ejecutable" if self._es_ejecutable(dependencias) else "No Ejecutable"
                print(f"Prioridad: {prioridad}, Fecha: {fecha}, Nombre: {nombre}, Dependencias: {dependencias} ({estado})")

    def completar_tarea(self, nombre):
        for i, (prioridad, fecha, n, dependencias) in enumerate(self.heap):
            if n == nombre:
                if not self._es_ejecutable(dependencias):
                    print(f"Tarea '{nombre}' no puede completarse porque tiene dependencias pendientes: {dependencias}.")
                    return
                tarea_completada = heapq.heappop(self.heap)
                self.tareas_completadas.append(tarea_completada)
                self._guardar_datos()
                print(f"Tarea '{nombre}' completada.")
                return
        print(f"Tarea '{nombre}' no encontrada.")

    def obtener_siguiente_tarea(self):
        if self.heap:
            prioridad, fecha, nombre, dependencias = self.heap[0]
            if self._es_ejecutable(dependencias):
                print(f"Siguiente tarea de mayor prioridad: {nombre} (Prioridad: {prioridad}, Fecha: {fecha}, Dependencias: {dependencias})")
            else:
                print(f"Siguiente tarea '{nombre}' no es ejecutable. Dependencias pendientes: {dependencias}")
        else:
            print("No hay tareas pendientes.")

def menu_interactivo():
    sistema = SistemaTareas()
    while True:
        print("\n--- Sistema de Gestión de Tareas ---")
        print("1. Añadir tarea")
        print("2. Mostrar tareas pendientes")
        print("3. Completar tarea")
        print("4. Obtener tarea de mayor prioridad")
        print("5. Salir")
        opcion = input("Selecciona una opción (1-5): ").strip()

        if opcion == '1':
            nombre = input("Nombre de la tarea: ").strip()
            while True:
                try:
                    prioridad = int(input("Prioridad de la tarea (número entero): ").strip())
                    break
                except ValueError:
                    print("La prioridad debe ser un número entero.")
            dependencias = input("Dependencias de la tarea (separadas por comas, o presiona Enter si no hay): ").strip()
            dependencias = dependencias.split(",") if dependencias else []
            sistema.añadir_tarea(nombre, prioridad, dependencias)
            print("Tarea añadida exitosamente.")
        
        elif opcion == '2':
            sistema.mostrar_tareas()

        elif opcion == '3':
            nombre = input("Nombre de la tarea a completar: ").strip()
            sistema.completar_tarea(nombre)

        elif opcion == '4':
            sistema.obtener_siguiente_tarea()

        elif opcion == '5':
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida. Por favor, selecciona un número entre 1 y 5.")

# Ejecutar menú interactivo
if __name__ == "__main__":
    menu_interactivo()
