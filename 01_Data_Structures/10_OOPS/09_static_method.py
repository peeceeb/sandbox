class ChaiUtils:
    
    @staticmethod #make sure to include this decorator
    def clean_ingredients(text):
        return [item.strip() for item in text.split(",")]

raw= " water , milk,  ginger   ,honey"

# obj=ChaiUtils()
# obj.clean_ingredients(raw)

cleaned=ChaiUtils.clean_ingredients(raw)

print(cleaned)