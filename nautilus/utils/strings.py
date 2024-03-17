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
GENERAL_REQUIRE_PRIVMSG = (
    f"{COLOR}{C.RED}{BOLD}Error:{BOLD} El comando {BOLD}{{}}{BOLD} solo se"
    f" puede usar por {BOLD}mensaje privado{BOLD}"
)
GENERAL_REQUIRE_SPECIFIC_CHANNEL = (
    f"{COLOR}{C.RED}{BOLD}Error:{BOLD} El comando {BOLD}{{}}{BOLD} solo se"
    f" puede usar en {BOLD}{{}}{BOLD}"
)
GENERAL_REQUIRE_CONTROL_CHANNEL = (
    f"{COLOR}{C.RED}{BOLD}Error:{BOLD} El comando {BOLD}{{}}{BOLD} solo se"
    f" puede usar en {BOLD}{{}}{BOLD}"
)

STREAMERS_AVAILABLE_ACTIONS = [
    f"{COLOR}{C.BLUE}Acciones disponibles para el comando {BOLD}!djs{BOLD}:",
    f"{COLOR}{C.BLUE}!djs {BOLD}registrar",
    f"{COLOR}{C.BLUE}!djs {BOLD}borrar",
    f"{COLOR}{C.BLUE}!djs {BOLD}listar",
]
STREAMERS_UNKNOWN_COMMAND = (
    f"{COLOR}{C.RED}{BOLD}Error:{BOLD} no se reconoce el comando {BOLD}{{}}"
)
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
    f"{COLOR}{C.GREEN}Se ha eliminado al DJ {BOLD}{{}}{BOLD} con éxito"
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
    f'{COLOR}{C.RED}{BOLD}Error:{BOLD} el usuario {BOLD}"{{}}"{BOLD} no existe'
)
STREAMERS_ANON_NOT_EXISTS = f"{COLOR}{C.RED}{BOLD}Error:{BOLD} el usuario no existe"
STREAMERS_CONFIRM_CHANGE_PASSWORD = (
    f"{COLOR}{C.BLUE}Para confirmar la contraseña del DJ {BOLD}{{}}{BOLD} escribe:"
    f"{BOLD} !djs cambiar-password {{}} {{}} {{}}"
)
STREAMERS_CHANGE_PASSWORD_SUCCESS = (
    f"{COLOR}{C.GREEN}La contraseña del DJ {BOLD}{{}}{BOLD} se ha cambiado con éxito"
)
STREAMERS_CHANGE_PASSWORD_PASSWORDS_NOT_SAME = (
    f"{COLOR}{C.RED}{BOLD}Error:{BOLD} las contraseñas no coinciden"
)
