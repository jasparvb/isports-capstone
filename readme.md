#<img src="https://raw.githubusercontent.com/jasparvb/isports-capstone/master/static/img/isports-logo.png" alt="alt text" width="150px" height="auto">  
The purpose of iSports is to make it easier to view and save news articles and events from the whole web which relate specifically to the sports, leagues, teams, and players that you are interested in.

The site is [deployed here](https://isports-news.herokuapp.com/).

## Data
There are two APIs that are used on the site:


1. The [theSportsDB.com](https://www.thesportsdb.com/api.php). This is used to find the sports, leagues, teams, and players available to be added as favorites. It is also used to find the upcoming events for your favorite leagues, teams and players.
2. The [newsapi.org](https://newsapi.org/). This is used to find related news articles, using the category ‘sports’ combined with other search parameters. News articles are returned in the language you select.

## Features
- Ability to search for latest sports news.
- News articles are displayed with a button to load more articles.
- A select menu in the navbar lets you choose the language your results should be displayed in. Your preference is stored in the session so it stays the same from page to page.
- Users can create, edit, or delete their account
- On your user profile, you are able to select the items you want to follow. Sports categories, leagues, teams, and players will appear in auto-complete as you type in the input field.
- Users with an account are able to save news articles to their favorites list.
- When a user follows a league or team, the upcoming and past events are displayed on their events page.

## User Flow
1. On the homepage, the user will see a carousel with top sports news headlines. A search bar below the carousel allows the user to search for top news headlines. He can change the language the articles are displayed in.
2. There will be links in the menu to create an account or login.
3. After creating an account, the user can choose to follow his favorite sports, leagues, teams, and players which are then saved to his profile.
4. The user can visit his news feed which will display news items according to the items (teams, players, etc) he is following.
5. By clicking an icon on the news item, the user can save or remove it to his favorites list.

## Tech Stack
- Backend: Python, Flask, Postgres
- Frontend: jQuery

## Database Diagram
An overview of how the local database is set up.

![](https://raw.githubusercontent.com/jasparvb/isports-capstone/master/static/img/tables-diagram.JPG)