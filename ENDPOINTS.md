# API Endpoints
## register
**Pattern:** `accounts/register/`
**View:** `accounts.views.auth_views.view`

## verify_email
**Pattern:** `accounts/verify-email/<uidb64>/<token>/`
**View:** `accounts.views.auth_views.view`

## login
**Pattern:** `accounts/login/`
**View:** `rest_framework_simplejwt.views.view`

## token_refresh
**Pattern:** `accounts/token/refresh/`
**View:** `rest_framework_simplejwt.views.view`

## profile
**Pattern:** `accounts/profile/`
**View:** `accounts.views.auth_views.view`

## change_password
**Pattern:** `accounts/profile/password-change/`
**View:** `accounts.views.auth_views.view`

## password_reset
**Pattern:** `accounts/reset-password/`
**View:** `accounts.views.auth_views.view`

## password_reset_confirm
**Pattern:** `accounts/reset-password/<uidb64>/<token>/`
**View:** `accounts.views.auth_views.view`

## deposit
**Pattern:** `accounts/deposit/`
**View:** `accounts.views.payment_views.view`

## verify-deposit
**Pattern:** `accounts/deposit/verify/`
**View:** `accounts.views.payment_views.view`

## product-list
**Pattern:** `products/^products/$`
**View:** `products.views.ProductViewSet`

## product-list
**Pattern:** `products/^products\.(?P<format>[a-z0-9]+)/?$`
**View:** `products.views.ProductViewSet`

## product-detail
**Pattern:** `products/^products/(?P<pk>[^/.]+)/$`
**View:** `products.views.ProductViewSet`

## product-detail
**Pattern:** `products/^products/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`
**View:** `products.views.ProductViewSet`

## category-list
**Pattern:** `products/^categories/$`
**View:** `products.views.CategoryViewSet`

## category-list
**Pattern:** `products/^categories\.(?P<format>[a-z0-9]+)/?$`
**View:** `products.views.CategoryViewSet`

## category-detail
**Pattern:** `products/^categories/(?P<pk>[^/.]+)/$`
**View:** `products.views.CategoryViewSet`

## category-detail
**Pattern:** `products/^categories/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`
**View:** `products.views.CategoryViewSet`

## api-root
**Pattern:** `products/`
**View:** `rest_framework.routers.view`

## api-root
**Pattern:** `products/<drf_format_suffix:format>`
**View:** `rest_framework.routers.view`

## cartitem-list
**Pattern:** `carts/^cart-items/$`
**View:** `cart.views.CartItemViewSet`

## cartitem-list
**Pattern:** `carts/^cart-items\.(?P<format>[a-z0-9]+)/?$`
**View:** `cart.views.CartItemViewSet`

## cartitem-detail
**Pattern:** `carts/^cart-items/(?P<pk>[^/.]+)/$`
**View:** `cart.views.CartItemViewSet`

## cartitem-detail
**Pattern:** `carts/^cart-items/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`
**View:** `cart.views.CartItemViewSet`

## api-root
**Pattern:** `carts/`
**View:** `rest_framework.routers.view`

## api-root
**Pattern:** `carts/<drf_format_suffix:format>`
**View:** `rest_framework.routers.view`

## cart
**Pattern:** `carts/carts/`
**View:** `cart.views.view`

## cart-detail
**Pattern:** `carts/carts/<int:pk>/`
**View:** `cart.views.view`
