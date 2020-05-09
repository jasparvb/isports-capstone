# iSports

The purpose of the site is to make it easier to view and save news articles from the whole web which relate specifically to the sports, leagues, teams, and players that you are interested in.

## Data
There are two APIs that are used on the site:


1. The [theSportsDB.com](https://www.thesportsdb.com/api.php). This will be used to find the sports, leagues, teams, and players available to be added as favorites. It is also used to find the upcoming events for your favorite leagues, teams and players.
2. The [newsapi.org](https://newsapi.org/). This will be used to find related news articles, using the category ‘sports’ combined with other search parameters.

## Features
- Ability to search for latest sports news.
- News articles are displayed with infinite scroll feature.
- A select menu on the homepage will let you choose the language your results should be displayed in.
- Users can create, edit, or delete their account
- On your user profile, you will be able to select the items you want to follow. Sports categories, leagues, teams, and players will appear in auto-complete as you type in the search bar.
- Users with an account are able to save news articles to their favorites list.
- When a user follows a league or team, the upcoming and past events will be displayed on their events page.

## User Flow
1. On the homepage, the user will see a carousel with top sports news headlines. A search bar below the carousel allows the user to search for top news headlines by sport, league, team, or player.
2. There will be links in the menu to create an account or login.
3. After creating an account, the user can choose to follow his favorite sports, leagues, teams, and players which are then saved to his profile. He will also be able to select the language(s) in which he wants his news to be displayed.
4. The user's custom news feed will display news items according to the items (teams, players, etc) he is following.
5. By clicking an icon on the news item, the user can save or remove it to his favorites list.

## Database Diagram
An overview of how the local database is set up.

![](https://raw.githubusercontent.com/jasparvb/isports-capstone/master/images/tables-diagram.JPG)