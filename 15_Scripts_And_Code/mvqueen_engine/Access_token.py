import requests

# Your credentials from Dev Dashboard
CLIENT_ID = "REMOVED_CLIENT_ID"
CLIENT_SECRET = "REMOVED_CLIENT_SECRET"
SHOP_DOMAIN = "mvqueen-2.myshopify.com"

# Step 1: Get Access Token
token_url = f"https://{SHOP_DOMAIN}/admin/oauth/access_token"

payload = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "client_credentials"
}

# Make the request to get access token
response = requests.post(token_url, json=payload)

if response.status_code == 200:
    access_token = response.json()["access_token"]
    print(f"Access Token: {access_token}")