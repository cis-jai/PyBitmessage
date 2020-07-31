"""This module is for thread start."""
try:
    import state
    from bitmessagemain import main
except ModuleNotFoundError:
    from . import  state
    from .bitmessagemain import main
# import state

    
if __name__ == '__main__':
    state.kivy = True
    print("Kivy Loading......")
    try:
        from bitmessagemain import main
    except ModuleNotFoundError:
        from .bitmessagemain import main
    main()
