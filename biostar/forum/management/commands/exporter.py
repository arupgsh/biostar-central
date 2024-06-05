
from sqlitedict import SqliteDict
from more_itertools import chunked

from django.core.management.base import BaseCommand
from django.conf import settings
from biostar.accounts.models import User, Profile
from biostar.forum.models import Post, SharedLink
from taggit.models import Tag

import logging, json

CHUNK_SIZE = 1000

def to_json(data):
    text = json.dumps(data, indent=4)
    return text

class Command(BaseCommand):
    help = 'Create search index for the forum app.'


    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=10,
                            help="limit to N entries")
        parser.add_argument('--dbname', type=str, default="export.db",
                            help="limit to N entries")

        # flag to dump posts
        parser.add_argument('--posts', action='store_true', help='Dump posts')
        # flag to dump users
        parser.add_argument('--users', action='store_true', help='Dump users')
        # flag to dump tags
        parser.add_argument('--tags', action='store_true', help='Dump tags')


    def post_dump(self, limit=None):
        date_fmt = "%Y-%m-%d %H:%M:%S"

        posts = Post.objects.filter().order_by("-pk")

        # Apply the limit.
        if limit:
            posts = posts[:limit]

        print("# post_dump ", posts.count())

        def post_format(post):
            data = dict(
                id=post.id,
                spam=post.spam,
                status=post.get_status_display(),
                type=post.get_type_display(),
                rank=int(post.rank),
                root_id=post.root_id,
                parent_id=post.parent_id,
                title=post.title,
                content=post.content,
                tag_val=post.tag_val,
                author_id=post.author_id,
                answer_count=post.answer_count,
                view_count=post.view_count,
                reply_count=post.reply_count,
                comment_count=post.comment_count,
                indexed=post.indexed,
                vote_count=post.vote_count,
                thread_votecount=post.thread_votecount,
                book_count=post.book_count,
                subs_count=post.subs_count,
                lastedit_user_id=post.lastedit_user_id,
                creation_date=post.creation_date.strftime(date_fmt),
                lastedit_date=post.lastedit_date.strftime(date_fmt),
                url=post.get_absolute_url(),
            )
            return data

        query = map(post_format, posts)
        return query

    def user_dump(self, limit=None):

        date_fmt = "%Y-%m-%d %H:%M:%S"

        users = User.objects.filter().select_related("profile").order_by("-pk")

        # Apply the limit.
        if limit:
            users = users[:limit]

        print("# user_dump ", users.count())

        def user_format(user):
            user.last_login = user.last_login or user.date_joined
            data = dict(

                id=user.id,
                uid=user.profile.uid,
                handle=user.profile.handle,
                role=user.profile.get_role_display(),
                message_prefs=user.profile.get_message_prefs_display(),
                digest_prefs=user.profile.get_digest_prefs_display(),
                name=user.profile.name,
                email=user.email,
                state=user.profile.get_state_display(),
                location=user.profile.location,
                website=user.profile.website,
                twitter=user.profile.twitter,
                scholar=user.profile.scholar,
                score=user.profile.score,
                text=user.profile.text,
                my_tags=user.profile.my_tags,
                watched_tags=user.profile.watched_tags,
                date_joined=user.date_joined.strftime(date_fmt),
                last_login=user.last_login.strftime(date_fmt),
            )
            return data

        query = map(user_format, users)
        return query

    def tag_dump(self, limit=None):
        tags = Tag.objects.filter().order_by("-pk")

        # Apply the limit.
        if limit:
            tags = tags[:limit]

        print("# tag_dump ", tags.count())

        def tag_format(tag):
            data = dict(
                id=tag.id,
                name=tag.name,
            )
            print(data)
            return data

        query = map(tag_format, tags)
        return query

    def save(self, query, db):
        for index, item in enumerate(query):
            key = item['id']
            db[key] = item
            if index % CHUNK_SIZE == 0:
                print(f"# committing at {index}")
                db.commit()
        print("# save complete")
        db.commit()

    def handle(self, *args, **options):

        limit = options['limit'] or None

        db_name = options['dbname']

        if options['posts']:
            post_db = SqliteDict(db_name, tablename="posts", encode=json.dumps, decode=json.loads)
            post_query = self.post_dump(limit=limit)
            self.save(post_query, db=post_db)
            post_db.close()

        if options['users']:
            user_db = SqliteDict(db_name, tablename="users", encode=json.dumps, decode=json.loads)
            user_query = self.user_dump(limit=limit)
            self.save(user_query, db=user_db)
            user_db.close()

        if options['tags']:
            tag_db = SqliteDict(db_name, tablename="tags", encode=json.dumps, decode=json.loads)
            tag_query = self.tag_dump(limit=limit)
            self.save(tag_query, db=tag_db)
            tag_db.close()







