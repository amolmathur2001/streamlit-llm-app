from outscraper import ApiClient



class ReviewData:
	def __init__(self, review_time, review_rating, review_text):
		self.time = review_time
		self.rating = review_rating
		self.text = review_text


class GoogleReviewsScrapper:
	def __init__(self, api_key):
		self.client = ApiClient(api_key=api_key)


	def get_latest_reviews(self, search_query):
		results = self.client.google_maps_reviews([search_query], reviews_limit=20, sort='newest', limit=500, language='en')
		review_data = []
		for place in results:
    			name = 'name:', place['name']
    			new_reviews = place.get('reviews_data', [])
	    		reviews = place.get('reviews_data', [])
    			for i, review in enumerate(reviews):
        			review_data.append(ReviewData(review['review_datetime_utc'], review["review_rating"], review["review_text"]))

		return review_data
