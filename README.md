# wordpress-api-jwt
Simple package for using a WordPress API using JWT authentication only


Prerequisites
--------
You need to install the **WP Plugin JWT Authentication** for WP REST API and its own prerequisites (which is WP REST API V2 as of now).
You can find the link here: https://wordpress.org/plugins/jwt-authentication-for-wp-rest-api/

Once installed, do not forget to do some configuration on the WP side! (such as CORs policy, token duration, etc.)

Code disclaimer
--------
- This is NOT a production ready package, just a very small package at its early stage. I created it for my own use, but I hope it can also help some other people who were struggling trying to integrate a Python web server against a WordPress authentication backend (such as Django <=> WP), which was impossible to make it work
- Feel free to send your PR to improve greatly this plugin, we can do great things I guess!
- The package only implements `GET` and `POST` methods for now, and you can retrieve either the response data directly or the response itself (I need to implement other methods later or perhaps create an abstract class)
- As of now, it does NOT handle the token refresh, as the token has a specific lifetime ; when using the API for a long session, make sure to call the API regularly to check if the token has expired or not (using endpoint `/WP-JSON/JWT-AUTH/V1/TOKEN/VALIDATE`), if so you'll need to connect again. Perhaps I will implement this automatically in the package itself in the future.
- **Not ALL scenarii have been tested with this API, so there can be some bugs!**

Install
--------

`pip install wordpress-api-jwt`

How-to-use (By example)
--------

The code is documented and you should also check the `main.py` file where you can find this complete example.

1) Make the import
```
from wpapijwt.wp_api import WordPressAPI
```

2) First, create the `WordPressAPI` instance. Please note that you pass only the domain, not the protocol (by default it's using HTTPS)
```
wp_api = WordPressAPI(domain="www.my-url-without-protocol.com", username="imthebest@gmail.com", password="PasswordImpossibleToHack")
```

3) *Optional*: If you still need to use a different protocol or use a different namespace than default `wp-json`, you can pass these extra parameters
```
wp_api = WordPressAPI(domain="www.my-url-without-protocol.com", 
                      username="imthebest@gmail.com", 
                      password="PasswordImpossibleToHack",
                      protocol="http",
                      namespace="wp-json-custom")
 ```

4) Call the `.connect()` method to actually connect the instance to WP. If it cannot connect, it should return `None` and print error message
```
wp_api.connect()
```

5) Once you are connected (always make sure it is thanks to property `.connected`), you can freely use the API! (example here by getting the connected user name with endpoint `/wp/v2/users/me`)
```
if wp_api.connected:
    print(f"{wp_api} Connected!")

    # Then you can start playing with the API :)
    get_myself = wp_api.get("/wp/v2/users/me")
    print(f"Hello {get_myself['name']}")
else:
    # Oops something went wrong!
    print("Not connected...")
```

**Note**: By default, the `.get()` and `.post()` methods return the JSON data from the endpoint's response directly **as a `dict`.** If you want to retrieve the response itself, you need to add parameter `get_response=True` to the method

**Note 2**: If you wish to add custom headers to the request, you should be able to pass a new dict containing your headers using `wp_api.headers.update({...})`

Result :
```
# /usr/bin/python3.6 -u /home/pycharmssh/wpapijwt/main.py
WordPressAPI Object : https://www.my-url-without-protocol.com/wp-json Connected!
Hello Baptiste!
```

Resources
--------
- https://developer.wordpress.org/rest-api/
- https://wordpress.org/plugins/jwt-authentication-for-wp-rest-api
- https://github.com/Tmeister/wp-api-jwt-auth/issues/59
