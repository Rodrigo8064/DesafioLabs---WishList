from ninja import NinjaAPI

from authentication.auth import jwt_bearer_auth

api = NinjaAPI(auth=jwt_bearer_auth)

api.add_router('/authentication/', 'authentication.api.router')
api.add_router('/users', 'users.api.router')
api.add_router('/products/', 'products.api.router')
api.add_router('/reviews/', 'reviews.api.router')
api.add_router('/favorites/', 'favorites.api.router')
