import decimal

# --- 浮動小数点数（float）の計算 ---
print("--- float (浮動小数点数) の計算 ---")
float_result = 0.1 + 0.2
print(f"0.1 + 0.2 の結果: {float_result}")
print(f"結果が0.3と等しいか？: {float_result == 0.3}")

# --- decimal (高精度な十進数) の計算 ---
print("\n--- decimal (十進数) の計算 ---")
d_a = decimal.Decimal('0.1')
d_b = decimal.Decimal('0.2')
decimal_result = d_a + d_b
print(f"0.1 + 0.2 の結果: {decimal_result}")
print(f"結果が0.3と等しいか？: {decimal_result == decimal.Decimal('0.3')}")

# --- quantize()メソッドの実験 ---
print("\n--- quantize() メソッドの実験 ---")
price = decimal.Decimal('15.654321')
# 小数点以下2桁で四捨五入
rounded_price = price.quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_HALF_UP)
print(f"元の価格: {price}")
print(f"小数点第2位で四捨五入した結果: {rounded_price}")

# 小数点以下3桁で四捨五入
rounded_price_3 = price.quantize(decimal.Decimal('0.001'), rounding=decimal.ROUND_HALF_UP)
print(f"小数点第3位で四捨五入した結果: {rounded_price_3}")