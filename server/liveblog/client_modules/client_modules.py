from liveblog.blogs.blogs import BlogsResource, BlogService
from eve.utils import ParsedRequest
from liveblog.posts.posts import PostsService, PostsResource, BlogPostsService, BlogPostsResource
from apps.users.users import UsersResource
from apps.users.services import UsersService
from apps.archive.common import item_url
from superdesk import get_resource_service


class ClientUsersResource(UsersResource):
    datasource = {
        'source': 'users',
        'default_sort': [('_created', -1)]
    }
    public_methods = ['GET']
    public_item_methods = ['GET']
    item_methods = ['GET']
    resource_methods = ['GET']

    schema = {}
    schema.update(UsersResource.schema)


class ClientUsersService(UsersService):
    def get(self, req, lookup):
        if req is None:
            req = ParsedRequest()
        docs = super().get(req, lookup)
        return docs


class ClientBlogsResource(BlogsResource):
    datasource = {
        'source': 'archive',
        'elastic_filter': {'term': {'particular_type': 'blog'}},
        'default_sort': [('_updated', -1)]
    }
    public_methods = ['GET']
    public_item_methods = ['GET']
    item_methods = ['GET']
    resource_methods = ['GET']

    schema = {}
    schema.update(BlogsResource.schema)


class ClientBlogsService(BlogService):
    def get(self, req, lookup):
        if req is None:
            req = ParsedRequest()
        docs = super().get(req, lookup)
        return docs


class ClientPostsResource(PostsResource):
    datasource = {
        'source': 'archive',
        'elastic_filter': {'term': {'particular_type': 'post'}},
        'default_sort': [('order', -1)]
    }
    public_methods = ['GET']
    public_item_methods = ['GET']
    item_methods = ['GET']
    resource_methods = ['GET']

    schema = {}
    schema.update(PostsResource.schema)


class ClientPostsService(PostsService):
    def get(self, req, lookup):
        if req is None:
            req = ParsedRequest()
        docs = super().get(req, lookup)
        return docs


class ClientBlogPostsResource(BlogPostsResource):
    url = 'client_blogs/<regex("[a-f0-9]{24}"):blog_id>/posts'
    schema = PostsResource.schema
    datasource = {
        'source': 'archive',
        'elastic_filter': {'term': {'particular_type': 'post'}},
        'default_sort': [('order', -1)]
    }
    public_methods = ['GET']
    public_item_methods = ['GET']
    item_methods = ['GET']
    resource_methods = ['GET']
    privileges = {'GET': 'blogs'}
    item_url = item_url


class ClientBlogPostsService(BlogPostsService):
    def get(self, req, lookup):
        if req is None:
            req = ParsedRequest()
        docs = super().get(req, lookup)
        # nest the user in the response
        for doc in docs:
            creator = get_resource_service('users').find_one(req=None, _id=doc.get('original_creator'))
            # select fields that are useful
            wanted_fields = ('first_name', 'last_name', 'display_name', 'username', 'picture_url')
            doc['original_creator'] = {key: creator.get(key, None) for key in wanted_fields}
        return docs
