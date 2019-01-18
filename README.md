# Graph API

Python library to connect [instagram graph API](https://developers.facebook.com/docs/instagram-api) and get data.


## Usage
```
from graph_api import InstagramGraphHandler

# Get account data 
handler = InstagramGraphHandlers(access_token=<your-access_token>, 
                                 account_id=<your-instagram-account-id>)
account_data = handler.account_data.get()

# Get media data
handler = InstagramGraphHandlers(access_token=<your-access_token>, 
                                 media_id=<instagram-media-id>)
media_comments = handler.media_comments.get()
```

##notes:
* All `.get()` API call only return one page response and you should loop over next pages urls.
* All handlers are available stand alone from graph_api.handler path. 