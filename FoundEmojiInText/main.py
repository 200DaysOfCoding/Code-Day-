import demoji

text = "Enjoy your meal! 🍽🍕🍔🍟"
emojis = demoji.findall(text)
print("Emojis found:", list(emojis.keys()))
