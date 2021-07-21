# This is an example code
# Feel free to replace this with your own WordPress integration so that you can quickly test the API.
from wpapijwt.wp_api import WordPressAPI

if __name__ == '__main__':
    # First, define the WP API object
    wp_api = WordPressAPI(domain="www.my-url-without-protocol.com", username="imthebest@gmail.com", password="PasswordImpossibleToHack")

    # Then you can call .connect() to actually connect to the API
    wp_api.connect()

    # Always check if the API is connected !
    if wp_api.connected:
        print(f"{wp_api} Connected!")

        # Then you can start playing with the API :)
        get_myself = wp_api.get("/wp/v2/users/me")
        print(f"Hello {get_myself['name']}")
    else:
        # Oops something went wrong!
        print("Not connected...")

