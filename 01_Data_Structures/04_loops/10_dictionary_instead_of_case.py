
Users=[
{"id":1,"total":100,"coupon":"p20"},
{"id":2,"total":150,"coupon":"p10"},

{"id":3,"total":80,"coupon":"p50"}
]

discounts = {
    "p20":(0.2,0),
    "p10":(0.5,0),
    "p50":(0,10),
}

for user in Users:
    percent, fixed= discounts.get(user["coupon"], (0,0))
    discount =user["total"] * percent + fixed
    print(f"{user["id"]} paid {user["total"]} and got discount for next visit of rupees {discount}")
