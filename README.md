# Gin-and-Tensor
We gon' make some drinks bruh.

Run development server with `python manage.py runserver`

When new drinks are added run `python manage.py get_images`
Only drinks where their static image folder is nonexistent will be searched for or downloaded.

For any drinks where the image feild in discovery is equal to "images/placeholder.jpg":
    The bot will search google for the name of the respective drink and download the first page of results into 
    the folder at '.../static/data/drink_images/00000000from_google'
    within a folder named the drink's discovery ID.
    Enter this folder and delete all but the desired image. Remove the __# from the end of that image's name.
    Move the folder into the drink_images folder when done.

All other drinks where an img src address is specified in the discovery result will be directly downloaded into a folder 
named their discovery ID and saved within the drink_images folder.

run `python manage.py db-populate` to insert discovery generated ids and drink names


