# MoviePosterDB
MPDB_ROOT = 'http://minimalmovieposters.tumblr.com'
MPDB_JSON = '%s/tagged/%%s' % MPDB_ROOT

####################################################################################################
def Start():

	HTTP.CacheTime = None

####################################################################################################
class MMPAgent(Agent.Movies):

	name = 'Minimalist Movie Posters'
	languages = [Locale.Language.NoLanguage]
	primary_provider = False
	contributes_to = ['com.plexapp.agents.imdb']

	def search(self, results, media, lang):
	
		if media.primary_metadata is not None:
			results.Append(MetadataSearchResult(
				id = media.primary_metadata.id,
				score = 100
			))

	def update(self, metadata, media, lang):
	
		i = 0
		valid_names = list()
		title = media.title
		
		if title is not None:
			page = HTML.ElementFromURL(
				MPDB_JSON % (String.Quote(title, usePlus=False) ),
				errors='ignore'
			)
			zoomLinks = page.xpath('//div[@id="posts"]/div[@class="post"]/div[@class="photo"]/a[@class="zoom"]')
			for zoomLink in zoomLinks:
				href = zoomLink.get("href")
				valid_names.append(self.add_poster(metadata, href, i))
				i += 1
				
	def add_poster(self, metadata, href, index):

		Log('Adding new poster: %s' % href)
		metadata.posters[href] = Proxy.Preview(HTTP.Request(href), sort_order=index)
		return href