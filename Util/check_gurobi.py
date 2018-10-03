
import sys

if __name__ == "__main__":
    try:
        import gurobipy
        gur = 0
    except:
        gur = 1

sys.exit(gur)