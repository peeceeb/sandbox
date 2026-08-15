import tiktoken

enc= tiktoken.encoding_for_model("gpt-4o")
text="Hello, how are you doing today? I hope everything is going well. This is a test to see how many tokens are in this text."
tokens=enc.encode(text)
print("Token", tokens)
print("Number of tokens:", len(tokens))

decoded=enc.decode([13225, 11, 1495, 553, 481, 5306, 4044, 30, 357, 5498, 5519, 382, 2966, 1775, 13, 1328, 382, 261, 1746, 316, 1921, 1495, 1991, 20290, 553, 306, 495, 2201, 13])

print("Decoded text:", decoded)                   


