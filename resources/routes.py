from .api import StorePricesApi, ProductsApi, LogRemoteApi,LogRemoteDeleteApi, LoggingFileDeleteApi, OmviStoreToOmviProductsApi
#from .movie import MoviesApi, MovieApi
from .auth import SignupApi, LoginApi, ChangePassApi, UserDataUpdateApi, UsersApi
from .servapi import GetProductsLTApi, GetProductsLVApi, GetProductsETApi, GetProductsENApi, GetProductsRUApi, GetPricelistaApi, GetVWholesaleApi, CreateDescriptionsApi, CreateVPricelistApi, TestApi
def initialize_routes(api):

    api.add_resource(SignupApi, '/api/v1/auth/signup')
    api.add_resource(LoginApi, '/api/v1/auth/login')
    api.add_resource(ChangePassApi, '/api/v1/auth/changepass')
    api.add_resource(UserDataUpdateApi, '/api/v1/auth/user_data_update')
    
    api.add_resource(LogRemoteApi, '/api/v1/log_remote')
    api.add_resource(LogRemoteDeleteApi, '/api/v1/log_remote_delete')
    api.add_resource(LoggingFileDeleteApi, '/api/v1/logging_delete')
    api.add_resource(StorePricesApi, '/api/v1/store_prices')
    api.add_resource(UsersApi, '/api/v1/users')
    api.add_resource(ProductsApi, '/api/v1/products')
    api.add_resource(OmviStoreToOmviProductsApi, '/api/v1/omvistoretoomviproducts')

    api.add_resource(GetProductsLTApi, '/api/v1/get_products_lt')
    api.add_resource(GetProductsLVApi, '/api/v1/get_products_lv')
    api.add_resource(GetProductsETApi, '/api/v1/get_products_et')
    api.add_resource(GetProductsENApi, '/api/v1/get_products_en')
    api.add_resource(GetProductsRUApi, '/api/v1/get_products_ru')
    api.add_resource(GetPricelistaApi, '/api/v1/get_pricelista')
    api.add_resource(GetVWholesaleApi, '/api/v1/get_v_wholesale')
    api.add_resource(CreateDescriptionsApi, '/api/v1/descriptions')
    api.add_resource(CreateVPricelistApi, '/api/v1/v_pricelist')
    api.add_resource(TestApi, '/api/v1/test')
    
