import tweepy
import configparser
import reader

def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def main():
  # Fill in the values noted in previous step here
  config_parser = configparser.ConfigParser()
  config_parser.read('config.ini')
  cfg = config_parser['last-words']


  api = get_api(cfg)
  tweets = reader.get_tweets()
  for tweet in tweets:
    status = api.update_status(status=tweet)

if __name__ == "__main__":
  main()
