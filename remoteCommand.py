import json,sys,traceback, time,datetime
import urllib2, subprocess 

server = 'http://localhost:8080';
user="admin";
pwd="admin";

seconds_wait=300

url_login = server + '/api/authenticate';
url_commands = server + '/api/remote-command';

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


def get_response_json_object(url, auth_token):
    '''
      returns json object with info
    '''
    req=urllib2.Request(url, None, getHeader(auth_token))
    response=urllib2.urlopen(req)
    html=response.read()
    json_obj=json.loads(html)
    return json_obj

def post_response_command (url, requestCommand, auth_token):
    '''
      upload to server the respond of the command
      returns string token
    '''    
    print "upload to server the respondcommand: {}".format(responseCommand);
    request = urllib2.Request(url=url, data=json.dumps(requestCommand), headers=getHeader(auth_token))
    response = urllib2.urlopen(request)

def perfom_requestcommand (requestCommand):
    '''
    returns a dict that represent the responseCommand
    '''    
    print "Perform requestRemoteCommand {} : {}".format(requestCommand['idRequestRemoteCommand'], requestCommand['command']);

    responseCommand = {};    
    responseCommand['description'] = requestCommand['description'];
    responseCommand['command'] = requestCommand['command'];
    responseCommand['idRequestRemoteCommand'] = requestCommand['idRequestRemoteCommand'];

    for command in requestCommand['command'].splitlines():
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log =  p.stdout.read();
        retval = p.wait();
        responseCommand['codReturn'] = retval;        
        if responseCommand.get('logResult') is not None:
            responseCommand['logResult'] = log;            
        else:             
            responseCommand['logResult'] = "\n".join([str(responseCommand.get('logResult')),log]);

    return responseCommand;



while True:
    print 'checking {}'.format(datetime.datetime.now() );

    try:
        # 1 Firt login and generate token
        auth_token = get_token(user, pwd);

        # 2 Get list of commands 
        result = get_response_json_object (url_commands,auth_token);

        # 3 Iterate over the list of commands and perfom th
        for requestCommand in result:
            responseCommand = perfom_requestcommand (requestCommand);
            upload_response_command(url_commands, responseCommand, auth_token);

    except: traceback.print_exc()

    time.sleep(seconds_wait)
