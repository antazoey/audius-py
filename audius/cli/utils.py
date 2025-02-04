try:
    from rich import print
except ImportError:
    print = print


__all__ = ["print"]
