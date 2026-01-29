from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

followers = Table(
    "follower_table",
    db.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("follower_id", ForeignKey("follower.id"), primary_key=True),
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=True)
    lastname: Mapped[str] = mapped_column(String(120), nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    post: Mapped[list["Post"]]=relationship()
    comment: Mapped[list["Comment"]]=relationship()
    followed: Mapped[list["Follower"]]= relationship("Follower", secondary= followers, back_populates= "followed_by")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
        }
       
class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    followed_by: Mapped[list[User]]= relationship("User", secondary= followers, back_populates= "followed")

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
