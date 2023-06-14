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
}
