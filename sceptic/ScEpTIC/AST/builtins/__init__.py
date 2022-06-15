from ScEpTIC.AST.builtins.builtin import Builtin

def load_libraries():
    """
    Loads the libraries of builtins
    """
    import ScEpTIC.AST.builtins.libs.math
    import ScEpTIC.AST.builtins.libs.mem
    import ScEpTIC.AST.builtins.libs.std
    import ScEpTIC.AST.builtins.libs.llvm


def link_builtins():
    """
    Links the builtins (both library-defined and user-defined)
    """
    Builtin.link()
