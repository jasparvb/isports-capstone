from app import app
from models import db, User, Favorite, Follow

db.drop_all()
db.create_all()

u1 = User.signup(
    "messi10",
    "123456",
    "messi@fcb.es"
)

db.session.add(u1)
db.session.commit()

f1 = Favorite(
    title="Bundesliga droht TV-Blackout am ersten Spieltag des Re-Starts - Digitalfernsehen.de",
    url="https://www.digitalfernsehen.de/news/medien-news/maerkte/bundesliga-droht-tv-blackout-am-ersten-spieltag-des-re-starts-556301/",
    image_url="https://www.digitalfernsehen.de/wp-content/uploads/2019/11/Testbild.jpg",
    published_at="2020-05-15T17:17:28Z",
    user_id=u1.id
)
f2 = Favorite(
    title="BVB: Stadt Dortmund und Polizei planen Meisterfeier trotz Corona - SPORT1",
    url="https://www.sport1.de/fussball/bundesliga/2020/05/bvb-stadt-dortmund-und-polizei-planen-meisterfeier-trotz-corona",
    image_url="https://reshape.sport1.de/c/t/12FD2190-55F9-49DC-A6AA-4B4CBE75A436/1200x630",
    published_at="2020-05-15T17:20:00Z",
    user_id=u1.id
)


follow1 = Follow(
    name="Lionel Messi",
    user_id=u1.id,
    sportsdb_id="34146370",
    category="player",
    tb_image="https://www.thesportsdb.com/images/media/player/thumb/rgevg81516994688.jpg")

follow2 = Follow(
    name="Barcelona",
    user_id=u1.id,
    sportsdb_id="133739",
    category="team",
    tb_image="https://www.thesportsdb.com/images/media/team/badge/xqwpup1473502878.png")


db.session.add_all([f1, f2, follow1, follow2])
db.session.commit()
