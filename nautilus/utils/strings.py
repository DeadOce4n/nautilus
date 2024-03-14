from sopel.formatting import (
    CONTROL_COLOR as COLOR,
    CONTROL_BOLD as BOLD,
    colors as C,
)

GENERAL_CONN_ERROR = f"{COLOR}{C.YELLOW}Error de conexión, intente más tarde"

GENERAL_MISSING_ARG = (
    f"{COLOR}{C.RED}{BOLD}Error:{BOLD} El argumento {{}} es obligatorio"
)
GENERAL_MISSING_ARGS = (
    f"{COLOR}{C.RED}{BOLD}Error:{BOLD} Los argumentos {{}} son obligatorios"
)

STREAMERS_AVAILABLE_ACTIONS = [
    f"{COLOR}{C.BLUE}Acciones disponibles para el comando {BOLD}!djs{BOLD}:",
    f"{COLOR}{C.BLUE}!djs {BOLD}registrar",
    f"{COLOR}{C.BLUE}!djs {BOLD}borrar",
    f"{COLOR}{C.BLUE}!djs {BOLD}listar",
]
STREAMERS_UNKNOWN_COMMAND = f"{COLOR}{C.RED}Error: no se reconoce el comando {BOLD}{{}}"
STREAMERS_CONFIRM_DELETE = (
    f"{COLOR}{C.BLUE}Para confirmar la eliminación del DJ {BOLD}{{}}{BOLD} escribe:"
    f"{BOLD} !djs borrar {{}} {{}}"
)
STREAMERS_ERROR_MISSING_TOKEN = (
    f"{COLOR}{C.RED}Error: por favor introduce el código de confirmación"
)
STREAMERS_ERROR_WRONG_TOKEN = (
    f"{COLOR}{C.RED}Error: el código de confirmación es incorrecto"
)
STREAMERS_DELETE_SUCCESS = (
    f"{COLOR}{C.GREEN}Se ha eliminado al DJ {BOLD}{{}}{BOLD} con exito"
)
STREAMERS_UNKNOWN_ERROR = (
    f"{COLOR}{C.RED}Error desconocido, pídale al administrador que revise los logs"
)
STREAMERS_REGISTRATION_SUCCESS = (
    f"{COLOR}{C.GREEN}Se ha registrado al DJ {BOLD}{{}}{BOLD} con exito."
)
STREAMERS_REGISTRATION_FAILED = (
    f"{COLOR}{C.RED}{BOLD}Error: no se pudo registrar al DJ (puede que el nick ya"
    " esté en uso)"
)
STREAMERS_USER_NOT_EXISTS = (
    f"{COLOR}{C.RED}{BOLD}Error:{BOLD} el usuario {BOLD}{{}}{BOLD}"
)
