import requests
import json
## Simple caching - to get iTunes data
def params_unique_combination(baseurl, params_d, private_keys=["api_key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)

def sample_get_cache_itunes_data(search_term,media_term="all"):
	CACHE_FNAME = 'cache_file_name.json'
	try:
	    cache_file = open(CACHE_FNAME, 'r')
	    cache_contents = cache_file.read()
	    CACHE_DICTION = json.loads(cache_contents)
	    cache_file.close()
	except:
	    CACHE_DICTION = {}
	baseurl = "https://itunes.apple.com/search"
	params = {}
	params["media"] = media_term
	params["term"] = search_term
	unique_ident = params_unique_combination(baseurl, params)
	if unique_ident in CACHE_DICTION:
		return CACHE_DICTION[unique_ident]
	else:
		CACHE_DICTION[unique_ident] = json.loads(requests.get(baseurl, params=params).text)
		full_text = json.dumps(CACHE_DICTION)
		cache_file_ref = open(CACHE_FNAME,"w")
		cache_file_ref.write(full_text)
		cache_file_ref.close()
		return CACHE_DICTION[unique_ident]
