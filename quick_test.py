import sys
sys.path.insert(0, '.')

print("Testing basic imports...")

try:
    from core import constants
    print("[OK] constants imported")
except Exception as e:
    print(f"[FAIL] constants import failed: {e}")

try:
    from core import pieces
    print("[OK] pieces imported")
except Exception as e:
    print(f"[FAIL] pieces import failed: {e}")

try:
    from core import formation
    print("[OK] formation imported")
except Exception as e:
    print(f"[FAIL] formation import failed: {e}")

try:
    from core import heuristic
    print("[OK] heuristic imported")
except Exception as e:
    print(f"[FAIL] heuristic import failed: {e}")

try:
    from core.strategies import MinimaxDepth2Strategy
    print("[OK] MinimaxDepth2Strategy imported")
except Exception as e:
    print(f"[FAIL] MinimaxDepth2Strategy import failed: {e}")

print("\nTesting simple formation generation...")
try:
    from core import formation
    f = formation.generate_random_formation(top_side=True)
    print(f"[OK] Generated formation with {len(f)} units")
    for i, unit in enumerate(f):
        print(f"  Unit {i+1}: {unit.piece.name}")
except Exception as e:
    print(f"[FAIL] Formation generation failed: {e}")
    import traceback
    traceback.print_exc()

print("\nAll tests completed.")