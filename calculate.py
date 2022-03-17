import mlrequest
import pandas as pd
import json

df_prices = pd.DataFrame(columns=['product', 'model', 'mean', 'std'])
products = []
with open('products.json') as f:
	products = json.load(f)

def remove_items(item):
    item.pop('seller', None)
    item.pop('prices', None)
    item.pop('installments', None)
    item.pop('address', None)
    item.pop('shipping', None)
    item.pop('seller_address', None)
    item.pop('attributes', None) # Should use
    item.pop('tags', None) # Should use
    return item

for product in products:
	for model in product['models']:
		print(f"Processing {product['product']}#{model}")
		response = mlrequest.busca(model, condition='used')
		results = response['results']
		results = list(map(remove_items, results))
		df = pd.DataFrame(results)
		df = df[df['domain_id'] == product['domain_id']]

		mean = df['price'].mean()
		std = df['price'].std()
		min_value = mean - std
		max_value = mean + std

		df = df[((df['price'] >= min_value) & (df['price'] <= max_value))]
		df_prices = df_prices.append({
			'product': product['product'],
			'model': model,
			'mean': df['price'].mean(),
			'std': df['price'].std()
		}, ignore_index=True)

df_prices.T.to_json('prices.json')

