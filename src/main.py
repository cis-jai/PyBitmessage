"""This module is for thread start."""
import state

from bitmessagemain import main
try:
    import state
except ModuleNotFoundError:
    from . import  state
    
if __name__ == '__main__':
    state.kivy = True
    print("Kivy Loading......")
    from bitmessagemain import main
    main()