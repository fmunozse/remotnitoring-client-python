import json,sys,traceback, time,datetime
import urllib2, subprocess 

server = 'http://localhost:8080';
user="admin";
pwd="admin";

seconds_wait=300

url_login = server + '/api/authenticate';
url_ping = server + '/api/monitor/heartbeats/ping';

def getHeader (auth_token):
    '''
        return headers to use in the api call. In case auth_token, then include the Authorization token
    '''
    if auth_token is None:
        return {'Content-Type':'application/json', 'Accept':'application/json'};
    else:
        return {'Content-Type':'application/json', 'Accept':'application/json', "Authorization": "Bearer %s" %auth_token }

def get_token (user, pwd):
    '''
      returns string token
    '''        
    json_data_authenticate ={  "password": pwd,  "rememberMe": "true", "username": user};
    request = urllib2.Request(url=url_login, data=json.dumps(json_data_authenticate), headers=getHeader(None))
    response = urllib2.urlopen(request)
    result_json_authenticate =  json.loads(response.read());
    return result_json_authenticate['id_token'];


def post_ping(url, auth_token):
    '''
      post ping
    '''
    req=urllib2.Request(url, json.dumps({"temp":"temp"}), getHeader(auth_token))
    response=urllib2.urlopen(req)
    response_headers = response.info()
    html=response.read()
    print response_headers['X-remotnitoringApp-ping'];

while True:
    print 'checking {}'.format(datetime.datetime.now() );

    try:
        # 1 Firt login and generate token
        auth_token = get_token(user, pwd);

        # 2 do the ping
        post_ping (url_ping,auth_token);

    except: traceback.print_exc()

    time.sleep(seconds_wait)
