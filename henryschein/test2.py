base_url  = 'https://www.henryschein.fr/fr-fr/dental/c/anesthesie-pharmacie/aiguilles'

url_slice = base_url.split('?')

if len(url_slice) > 1 : 
    base_url = url_slice[0]
else:
    base_url = base_url


print(base_url)