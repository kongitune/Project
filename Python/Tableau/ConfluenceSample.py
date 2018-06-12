import requests
import json

BASE_URL = ""
SPACE_KEY = ""
PAGE_TITLE = "RestSample"
AUTH = ("USER", "PASSWORD")
HEADERS = {"content-type":"application/json"}
 
# access and search the page
# https://Confluence Server URL/rest/api/content?title=title&spaceKey=spaceKey
# HTTP get method
def get_page_info(space_key, page_title):
    response = requests.get(
        BASE_URL + "/rest/api/content",
        auth = AUTH,
        params = {"title":PAGE_TITLE, "spaseKey":SPACE_KEY, "expand":"version,history"})
    #HTTP status check 
    response.raise_for_status()
    return response
 
# create the page
# https://Confluence Server URL/rest/api/content
# HTTP post method
def create_page():
    json_data = create_json_data()
    response = requests.post(
         BASE_URL + "/rest/api/content",
         auth=AUTH,
         data = json.dumps(json_data),
         headers=HEADERS)
    response.raise_for_status()
    return response

# update the page
# http://Confluence Server URL/rest/api/content/pageID
# HTTP put method
def update_page(version_num, page_id):
    # add version information
    json_data = create_json_data()
    json_data["version"] = {'number':version_num}
    response = requests.put(
         BASE_URL + "/rest/api/content/" + page_id,
         auth=AUTH,
         data = json.dumps(json_data),
         headers=HEADERS)
    response.raise_for_status()
    return response
     
# create json data
def create_json_data():
   
    # input in the page_text the contents you want to set on the page
    file = open('page_text.html', 'r')
    page = file.read()
    print(page)
    page_text = page
   
    payload = {
                "type":"page",
                "title":PAGE_TITLE,
                "space":{"key":SPACE_KEY},
                "body":{
                  "storage":{
                    "value":page_text,
                    "representation":"storage"
                  }
                }
              }
    return payload
 
# main function
if __name__ == "__main__":
    print("-------------- start --------------------")
    response = get_page_info(SPACE_KEY, PAGE_TITLE)
     
    response_data = response.json()
    if response_data["size"] == 0:
        create_page()
        print("ページがないので作成しました")
    else:
        result = response_data["results"][0]
        new_version_number = result["version"]["number"] + 1
        page_id = result["id"]
        update_page(new_version_number, page_id)
        print("ページがあったので更新しました (version={0})".format(new_version_number))
print("-------------- end ----------------------")