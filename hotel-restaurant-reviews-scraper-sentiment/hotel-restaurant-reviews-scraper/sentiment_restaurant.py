from pymongo import MongoClient
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from tqdm import tqdm
import time


nltk.download('vader_lexicon', quiet=True)
sia = SentimentIntensityAnalyzer()


client = MongoClient("mongodb://localhost:27017/")
db = client["Imad_Sassi"]
collection = db["Restaurants"]  


try:
   
    client.admin.command('ping')
    print("Connexion à MongoDB réussie!")
except Exception as e:
    print(f"Erreur de connexion à MongoDB: {e}")
    exit(1)


test_id = None
try:
   
    first_restaurant = collection.find_one() 
    if first_restaurant:
        test_id = first_restaurant["_id"]
        
        
        test_result = collection.update_one(
            {"_id": test_id},
            {"$set": {"_test_field": "test_value"}}
        )
        
       
        if test_result.modified_count > 0:
            print("Test de modification réussi!")
            collection.update_one(
                {"_id": test_id},
                {"$unset": {"_test_field": ""}}
            )
        else:
            print(" Le test de modification a échoué. Vérifiez vos permissions.")
            exit(1)
    else:
        print("Aucun document trouvé dans la collection!")
        exit(1)
except Exception as e:
    print(f"Erreur lors du test de modification: {e}")
    exit(1)


restaurants = list(collection.find())  
print(f"Nombre total de restaurants trouvés: {len(restaurants)}")  


total_reviews = 0
reviews_updated = 0
verification_errors = 0


verification_samples = []

for restaurant in tqdm(restaurants):  
    restaurant_id = restaurant["_id"]  
    reviews = restaurant.get("reviews", [])
    total_reviews += len(reviews)
    
    
    for i, review in enumerate(reviews):
        commentaire = review.get("commentaire", "")
        
       
        if commentaire:
            
            score = sia.polarity_scores(commentaire)
            compound = score["compound"]
            
            if compound >= 0.05:
                sentiment = "positif"
            elif compound <= -0.05:
                sentiment = "négatif"
            else:
                sentiment = "neutre"
            
          
            try:
                result = collection.update_one(
                    {"_id": restaurant_id},  
                    {"$set": {f"reviews.{i}.sentiment": sentiment}}  
                )
                
               
                if len(verification_samples) < 5:
                    verification_samples.append({
                        "restaurant_id": restaurant_id,  
                        "review_index": i,
                        "expected_sentiment": sentiment
                    })
                
                if result.modified_count > 0 or result.matched_count > 0:
                    reviews_updated += 1
                else:
                    print(f" Échec de mise à jour pour restaurant {restaurant_id}, review {i}")  
            except Exception as e:
                print(f"Erreur lors de la mise à jour: {e}")
                verification_errors += 1


print("Attente de 3 secondes pour la propagation des mises à jour...")
time.sleep(3)


print("\nVérification des échantillons mis à jour:")
for sample in verification_samples:
    restaurant = collection.find_one({"_id": sample["restaurant_id"]})  
    if restaurant and "reviews" in restaurant and len(restaurant["reviews"]) > sample["review_index"]:
        review = restaurant["reviews"][sample["review_index"]]
        actual_sentiment = review.get("sentiment", "NON TROUVÉ")  
        expected = sample["expected_sentiment"]
        
        if actual_sentiment == expected:
            print(f" Échantillon vérifié: sentiment = {actual_sentiment}")
        else:
            print(f" Échantillon NON vérifié: attendu '{expected}', trouvé '{actual_sentiment}'")
    else:
        print(f"Échantillon introuvable: restaurant {sample['restaurant_id']}, index {sample['review_index']}")  

print(f"\nRésumé de l'opération:")
print(f"- Total de restaurants traités: {len(restaurants)}")  
print(f"- Total de commentaires trouvés: {total_reviews}")
print(f"- Commentaires mis à jour avec sentiment: {reviews_updated}")  
print(f"- Erreurs lors de la mise à jour: {verification_errors}")
