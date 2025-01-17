import os 
import dotenv 

dotenv.load_dotenv()

# asana 
asana_token = os.getenv("ASANA_TOKEN")
workspace_gid = os.getenv("WORKSPACE_GID")  
team_gid = os.getenv('TEAM_GID')
portfolio_gid = os.getenv('PORTFOLIO_GID')  

# asana OAuth
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "http://localhost:5000/callback"
auth_url = "https://app.asana.com/-/oauth_authorize"

# telegram
bot_token = os.getenv("BOT_TOKEN")

# database 
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
database = os.getenv("DATABASE")

# redis
rd_host = 'localhost'
rd_port = 6379
token_ttl = 518400 # store cache for 6 days

# misc
gs_url = os.getenv("GS_URL")

 




