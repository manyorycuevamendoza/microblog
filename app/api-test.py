import requests
import json

#parametro
names=["Pedro","jose","juan","miguel","jhon","Paul","Sabrina","Katherina"]

paises ={}



for name in names:
    url="htts://api.nationalize.io/?name/" + name
    result=requests.get(url).json()
    pais=result["country"][0]["country_id"]
    print(pais)

    if pais in paises:
        paises[pais]+=1
    else:
        paises[pais]=1

#muestra el resultado
print(json.dumps(paises),indent=4)

def get_Reviews():
    reviews=Review.query.all()
    print(reviews)
    reviewsStrings=""
    for review in reviews:
        reviewsStrings+=review.rating + " " + review.description + "<br>"
    return reviewsStrings
@app.route('/consodarPaises'):

