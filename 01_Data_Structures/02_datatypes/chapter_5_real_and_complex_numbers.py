import sys
from fractions import Fraction
from decimal import Decimal

ideal_temp=24.5
current_temp=37

print(f"ideal_temp",{ideal_temp})
print(f"current_temp",{current_temp})

Difference_temp=current_temp-ideal_temp
print(f"Difference_temp",{Difference_temp})
print(sys.float_info)
