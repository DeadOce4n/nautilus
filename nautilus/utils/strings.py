from sopel.formatting import (
    CONTROL_COLOR as COLOR,
    CONTROL_BOLD as BOLD,
    CONTROL_NORMAL as RESET,
    colors as C,
)

general = {"CONN_ERROR": f"{COLOR}{C.YELLOW}Error de conexión, intente más tarde"}

streamers = {
    "ALL_ARGS_MISSING": [
        f"{COLOR}{C.RED}{BOLD}Error:{BOLD} hacen falta argumentos.",
        f"{COLOR}{C.BLUE}Ejemplo: !djs {BOLD}registrar",
        f"{COLOR}{C.BLUE}Ejemplo: !djs {BOLD}borrar",
        f"{COLOR}{C.BLUE}Ejemplo: !djs {BOLD}lista",
    ],
    "ARGS_MISSING_DELETE": [
        f"{COLOR}{C.RED}{BOLD}Error:{BOLD} hacen falta argumentos.",
        f"{COLOR}{C.BLUE}Ejemplo: !djs borrar {BOLD}usuario",
    ],
    "LIST": f"{COLOR}{C.BLUE}Nuestros DJs son: {BOLD}{{streamers}}",
    "TO_DELETE_USER_X": f"{COLOR}{C.BLUE}Para borrar a {BOLD}{{}}{RESET}{COLOR}{C.BLUE}"
    "escribe:",
    "TO_DELETE_USER_X_CODE_COMMAND": f"{COLOR}{C.BLUE}!djs borrar {{}} {BOLD} {{}}",
    "USER_NOT_EXISTS": f"{COLOR}{C.RED}{BOLD}Error:{BOLD} el usuario {BOLD}{{}}{BOLD}"
    "no existe.",
    "DJ_REGISTRATION_SUCCESS": f"{COLOR}{C.GREEN}Se ha registrado al DJ {BOLD}{{}}{BOLD} con exito.",
    "DJ_REGISTRATION_FAILED": f"{COLOR}{C.RED}{BOLD}Error: no se pudo registrar al DJ (puede que el nick ya esté en uso).",
}

GENERAL_MISSING_ARGS = (
    f'{COLOR}{C.RED}{BOLD}Error:{BOLD} El argumento {BOLD}"{{}}"{BOLD} es obligatorio'
)

STREAMERS_AVAILABLE_ACTIONS = [
    f"{COLOR}{C.BLUE}Acciones disponibles para el comando {BOLD}!djs{BOLD}:",
    f"{COLOR}{C.BLUE}!djs {BOLD}registrar",
    f"{COLOR}{C.BLUE}!djs {BOLD}borrar",
    f"{COLOR}{C.BLUE}!djs {BOLD}lista",
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
