from config.logger import Logger

# ─────────────────────────────────────────────────────────────────────────────
# PATRÓN SINGLETON — SistemaConfig
# Centraliza la configuración global de la aplicación.
# ─────────────────────────────────────────────────────────────────────────────
class SistemaConfig:
    _inst = None

    def __new__(cls):
        if cls._inst is None:
            cls._inst = super().__new__(cls)
            cls._inst.nombre  = "Sistema de Gestión POO"
            cls._inst.version = "1.0"
            cls._inst.empresa = "IESTP Argentina"
            cls._inst.autor   = "Rodas Roque"
            Logger().info(
                f"Sistema Iniciado: {cls._inst.nombre} "
                f"Version: {cls._inst.version} "
                f"Empresa: {cls._inst.empresa} "
                f"Autor: {cls._inst.autor}"
            )
        return cls._inst
