"""Import statements."""
from app.bucketlist.models import db, User, BucketList, Item

db.create_all()

# create sample user
user = User("Jack", "password")

db.session.add(user)
db.session.commit()

# create Bucketlist for user
bucket_list = BucketList("Travelling", 1)

db.session.add(bucket_list)
db.session.commit()

# create Bucketlist item for user
bucket_list_item = Item("Visit Dubai", 1)

db.session.add(bucket_list_item)
db.session.commit()
