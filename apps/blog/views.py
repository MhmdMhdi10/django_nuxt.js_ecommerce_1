from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import BlogPost, Comment
from .serializers import BlogPostSerializer, CommentSerializer
from .permissions import IsSuperuserOrStaffOrReadOnly, IsCommentOwner


class BlogPostListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, ):
        try:
            blog_posts = BlogPost.objects.all()
            serializer = BlogPostSerializer(blog_posts, many=True)
            return Response({"blogs": serializer.data, "message": "Blog posts retrieved successfully",
                             "type": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e), "type": "failure"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BlogPostDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        try:
            blog_post = BlogPost.objects.get(pk=pk)
            serializer = BlogPostSerializer(blog_post)
            return Response({"blog": serializer.data, "message": "Blog post retrieved successfully",
                             "type": "success"}, status=status.HTTP_200_OK)
        except BlogPost.DoesNotExist:
            return Response({"message": "Blog post not found", "type": "failure"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e), "type": "failure"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================< COMMENTS >============================================

class PostReviewListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, post_id):
        try:
            comments = Comment.objects.filter(post=post_id)
            serializer = CommentSerializer(comments, many=True)
            return Response({"Comments": serializer.data,
                             "message": "Comments fetched successfully", "type": "success"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Error fetching comments", "type": "failure"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostCommentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        request.data['user'] = request.user.id

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"comment": serializer.data, "message": "Comment created successfully", "type": "success"},
                            status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors, "message": "Failed to create comment", "type": "failure"},
                        status=status.HTTP_400_BAD_REQUEST)


class PostCommentUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCommentOwner]  # Apply permission classes

    def patch(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response({"message": "Comment not found", "type": "failure"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is the owner of the comment
        if not request.user == comment.user:
            return Response({"message": "You are not authorized to update this comment", "type": "failure"},
                            status=status.HTTP_403_FORBIDDEN)

        request.data['user'] = request.user.id
        request.data['post'] = comment.post.id

        if request.data['reply'] == comment.id:
            request.data['reply'] = comment.reply

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"comment": serializer.data, "message": "Comment updated successfully", "type": "success"},
                status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors, "message": "Failed to update comment", "type": "failure"},
                        status=status.HTTP_400_BAD_REQUEST)


class PostCommentDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCommentOwner]  # Apply permission classes

    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response({"message": "Comment not found", "type": "failure"}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response({"message": "Comment deleted successfully", "type": "success"},
                        status=status.HTTP_204_NO_CONTENT)


# ============================================< ADMIN >============================================

class BlogPostCreateView(APIView):
    permission_classes = [IsSuperuserOrStaffOrReadOnly]

    def post(self, request):
        self.check_permissions(request)

        request.data['created_by'] = request.user.id

        serializer = BlogPostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"blog": serializer.data, "message": "Blog post created successfully", "type": "success"},
                status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors, "message": "Failed to create blog post", "type": "failure"},
                        status=status.HTTP_400_BAD_REQUEST)


class BlogPostUpdateView(APIView):
    permission_classes = [IsSuperuserOrStaffOrReadOnly]  # Apply the permission class

    def put(self, request, pk):
        try:
            blog_post = BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            return Response({"message": "Blog post not found", "type": "failure"}, status=status.HTTP_404_NOT_FOUND)

        request.data['updated_by'] = request.user.id

        serializer = BlogPostSerializer(blog_post, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({"blog": serializer.data, "message": "Blog post updated successfully", "type": "success"},
                            status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors, "message": "Failed to update blog post", "type": "failure"},
                        status=status.HTTP_400_BAD_REQUEST)


class BlogPostDeleteView(APIView):
    permission_classes = [IsSuperuserOrStaffOrReadOnly]  # Apply the permission class

    def delete(self, request, pk):
        try:
            blog_post = BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            return Response({"message": "Blog post not found", "type": "failure"}, status=status.HTTP_404_NOT_FOUND)

        blog_post.delete()
        return Response({"message": "Blog post deleted successfully", "type": "success"},
                        status=status.HTTP_204_NO_CONTENT)




