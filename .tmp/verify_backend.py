
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from backend.main import parse_poliza_block

raw_string = "✅ ⏳ VENCE 30D | 🚗 AUTO | N° POL: 33333333 | 🏷️ PDL384 | 🅰️ A | ❤️ VIDA: SI | 🆘 AUX  ✅ VENCE 30D | ANULADA | 🚗 CAMIONETA | N° POL: 777742 | 🏷️ POL432"

print(f"TESTING STRING: {raw_string}\n")

parsed = parse_poliza_block(raw_string)

print(f"FOUND {len(parsed)} POLICIES:")
for i, p in enumerate(parsed):
    print(f"POLICY {i+1}: {p}")

# Verification
ok = True
if len(parsed) != 2:
    print("❌ ERROR: Expected 2 policies")
    ok = False

p1 = parsed[0]
if p1['patente'] != 'PDL384' or p1['numero'] != '33333333':
    print("❌ ERROR: Policy 1 data mismatch")
    ok = False

p2 = parsed[1]
if p2['patente'] != 'POL432' or p2['numero'] != '777742':
    print("❌ ERROR: Policy 2 data mismatch")
    ok = False
    
if p2['estado'] != 'ANULADA':
    print(f"❌ ERROR: Policy 2 status should be ANULADA, got {p2['estado']}")
    ok = False

if ok:
    print("\n✅ ALL TESTS PASSED")
else:
    print("\n❌ TESTS FAILED")
