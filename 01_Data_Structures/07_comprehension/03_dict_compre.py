tea_prices ={
    "Masala Chai": 40,
    "Green Tea": 50,
    "Lemon Tea": 200,
}

tea_price_usd= {tea:price/90 for tea, price in tea_prices.items()}
print(tea_price_usd)