from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

follower_table = Table(
    "follower_table",
    db.metadata,
    Column("follower_id", ForeignKey("user.id"), primary_key=True),
    Column("followed_id", ForeignKey("user.id"), primary_key=True),
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=True)
    lastname: Mapped[str] = mapped_column(String(120), nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    post: Mapped[list["Post"]]=relationship()
    comment: Mapped[list["Comment"]]=relationship()
    following: Mapped[list["User"]]= relationship("User", secondary= follower_table, primaryjoin=(follower_table.c.follower_id == id), secondaryjoin=(follower_table.c.followed_id == id), back_populates= "followers")
    followers: Mapped[list["User"]]= relationship("User", secondary= follower_table, primaryjoin=(follower_table.c.followed_id == id), secondaryjoin=(follower_table.c.follower_id == id), back_populates= "following")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
        }
    
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int]= mapped_column(ForeignKey(User.id))
    post_by: Mapped[User]=relationship(back_populates="post")
    media: Mapped[list["Media"]]=relationship()

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int]= mapped_column(ForeignKey(Post.id))
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    Media_by: Mapped[Post]=relationship(back_populates="Post")

    def serialize(self):
        return{
            "url": self.url
        }
    
class Comment(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    Author_id: Mapped[int]= mapped_column(ForeignKey(User.id))
    commentary: Mapped[str]=mapped_column(String(180), unique=False ,nullable=True)
    post_id: Mapped[int]= mapped_column(ForeignKey(Post.id))
    commented_by: Mapped[User]=relationship(back_populates="comment")

    def serialize(self):
        return{
            "comment": self.commentary
        }