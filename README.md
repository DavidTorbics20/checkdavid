# checkdavid

After a succesfull rebrand I no longer compare prices of flights. This is now an application for tracking prices in a videogame called Escape From Tarkov.

The application should:
- Show all the prices for a specific category of items.
- Sort items throught a filter (by name, by category)
- A menu with item that the user saved.
  - With a star, bookmark or like button next to the item information.
  - The item should contain following data: 
    - image (optional)
    - name
    - current price avg
    - price per slot
    - how much more exepnsive it got
    - which trader sells this item.
    - how much the traders offers for an item
- Whenever the user checks on the saved items the application searches for it again and updates the price acordingly.
- Run application in the background to keep track of lowest and highest prices.

## Progress

### Webscraping 20.1.2023
For the retrival of data I am using the BeautifulSoup library and the information I am getting is from 
https://www.kiwi.com. I started the implementation of this but came across some difficulties like scraping just the content I need. 

I probably won't have a working code by midnight but that's what I have the weekend for anyways.

### Rebranding 25.1.2023

I gave up with the last project and started a new one. It is pretty simular to the old one with the exception that this time I save prices of items in a game.

For the retrival of data I am using the BeautifulSoup and Selenium library. The information I am getting is from 
https://tarkov-market.com/. 
