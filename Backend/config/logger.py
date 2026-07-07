import datetime

# ─────────────────────────────────────────────────────────────────────────────
# PATRÓN SINGLETON — Logger
# Un Singleton garantiza que sólo exista UNA instancia de esta clase en toda la
# ejecución del programa. Así, cualquier módulo que haga Logger() siempre obtiene
# el mismo objeto y la misma lista de logs, sin importar cuántas veces se llame.
# ─────────────────────────────────────────────────────────────────────────────
class Logger:
    _instancia = None  # variable de clase que guarda la única instancia creada

    def __new__(cls):
        # __new__ se ejecuta ANTES de __init__ y es quien realmente crea el objeto.
        # Si ya existe una instancia previa, la devuelve sin crear una nueva.
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            # Inicializamos la lista de logs aquí (dentro de __new__) para que
            # sólo se cree una vez, aunque se llame Logger() muchas veces.
            cls._instancia._logs = []
        return cls._instancia

    def _registrar(self, nivel, mensaje):
        # Método privado que usan internamente info(), warning() y error().
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        entrada = {"hora": hora, "nivel": nivel, "msg": mensaje}
        self._logs.append(entrada)

    def info(self, msg):    self._registrar("INFO",    msg)
    def warning(self, msg): self._registrar("WARNING", msg)
    def error(self, msg):   self._registrar("ERROR",   msg)

    def mostrar_logs(self):
        print(f"\n=== HISTORIAL DEL SISTEMA ({len(self._logs)} eventos) ===")
        for log in self._logs:
            print(f"  [{log['hora']}] {log['nivel']:7} | {log['msg']}")

    def limpiar(self):
        self._logs.clear()
        print("  OK Historial de logs limpiado")
