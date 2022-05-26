
from .models import * 

class PostService():
    @staticmethod
    def create_post(user, post):
        post = Post(user=user, post=post)
        post.save()

        return [post, True]

    @staticmethod
    def edit_post(user, post_id, content):
        try:
            post = Post.objects.get(id=post_id)
            if post.user != user:
                return {"success": False, "message": "Authorization denied"}
            else:
                post.post = content
                post.save()

                return {"success": True, "message": "Post successfully updated"}
        except Post.DoesNotExist:
            return {"success": False, "message": "The post does not exist"}
    
    @staticmethod
    def get_post(post_id):
        try:
            post = Post.objects.get(id=post_id)

            return post
        except Post.DoesNotExist:
            return None

    @staticmethod
    def update_post_like(user, post_id, liked):
        try:
            post = Post.objects.get(id=post_id)

            post_like, created = PostLike.objects.get_or_create(user=user, post=post, is_like=liked)
            post_like.save()

            return {"success": True, "message": "Post successfully updated"}

        except Post.DoesNotExist:
            return {"success": False, "message": "The post does not exist"}
    
    @staticmethod
    def update_post_dislike(user, post_id):
        try:
            post = Post.objects.get(id=post_id)

            try:
                post_like = PostLike.objects.get(user=user, post=post)
                post_like.delete()

            except PostLike.DoesNotExist:
                pass            

            return {"success": True, "message": "Post successfully updated"}

        except Post.DoesNotExist:
            return {"success": False, "message": "The post does not exist"}
    
    @staticmethod
    def is_post_liked(post_id, user):
        try:
            post = Post.objects.get(id=post_id)

            try:
                post_like = PostLike.objects.get(user=user, post=post)
                return post_like.is_like

            except PostLike.DoesNotExist:
                return False           

        except Post.DoesNotExist:
            return {"success": False, "message": "The post does not exist"}
            
    @staticmethod
    def get_all_posts():
        posts = Post.objects.all()
        return posts
    

