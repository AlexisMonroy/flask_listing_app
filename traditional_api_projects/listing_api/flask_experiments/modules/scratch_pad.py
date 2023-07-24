if session_id is not None:
        fetch_token_call = 'FetchToken' 
        use_fetch_token = True
        if use_fetch_token:
          call_name = fetch_token_call
          call_header['X-EBAY-API-CALL-NAME'] = call_name

        header = call_header    


def callback():
    if request.method == 'GET':
        fetch_token_headers = { 
    'X-EBAY-API-COMPATIBILITY-LEVEL': '719',
    'X-EBAY-API-DEV-NAME': 'dae89547-48b8-4c4b-9e57-e8e9a84527dd',
    'X-EBAY-API-APP-NAME': 'AlexisGo-pricepre-PRD-3ca7161d2-d3ef5057',
    'X-EBAY-API-CERT-NAME': 'PRD-ca7161d2a58b-663b-4c87-9cec-8cbd',
    'X-EBAY-API-CALL-NAME': 'FetchToken',
    'X-EBAY-API-SITEID': '0',
    'Content-Type' : 'text/xml'}     

        fetch_token_data = f'''<?xml version="1.0" encoding="utf-8"?>
        <FetchTokenRequest xmlns="urn:ebay:apis:eBLBaseComponents">
        <SessionID>{session_id}</SessionID>
        </FetchTokenRequest>'''

        fetch_token_response = requests.post(url, headers=fetch_token_headers, data=fetch_token_data)
        print(fetch_token_response.status_code)
        print(fetch_token_response.text)

        fetch_token_tree = ET.fromstring(fetch_token_response.text)
        fetch_token = fetch_token_tree[4].text
        token.append(fetch_token)
        print("Token: " + fetch_token)

        dict_data = {}
        for child in tree:
            dict_data[child.tag] = child.text


        with open('resp_output/response.txt', 'w') as f:
            f.write(session_response.text)
            f.write("\n\n\n")
            f.write(str(tree))
            f.write("\n\n\n")
            f.write(str(dict_data))
            f.write("\n\n\n")
            f.write(fetch_token_response.text)
            f.write("\n\n\n")
            f.write(str(fetch_token_tree))
            return render_template('callback.html')
    print("Done with Callback")
    return render_template('callback.html', dict_data=dict_data)

    
{% extends "base.html" %}
{% block body %}
    <h1>Access Granted</h1>
    <p>Login was successful</p>
    <p>
{% endblock %}
with open('resp_output/verify_data.txt', 'w') as f:
              f.write(str(verify_data))
          print("TYPE:\n", type(verify_data))
          with open('resp_output/start_end.txt', 'w') as f:
              f.write("START:\n:" + str(datetime.datetime.now()))

          verify_responses = []
for i in range(0, len(verify_data)):
            if verify_data[i] is not None:
              verify_response = requests.post(url, headers=api_call_headers, data=verify_data[i])
              print(verify_response.status_code)
              print(verify_response.text)
              print("Done with API Call")
              with open('resp_output/api_call_response.txt', 'a') as f:
                  f.write("Start:\n:" + str(datetime.datetime.now())) 
                  f.write(str(len(verify_data)))
                  print("\n\n\n")
                  f.write(str(verify_response))
                  f.write("\n\n\n")
                  f.write(str(verify_response.text))
                  print("\n\n\n")
                  print("End:\n:" + str(datetime.datetime.now()))
              verify_responses.append(verify_response.text)
          with open('resp_output/start_end.txt', 'a') as f:
              f.write("END:\n:" + str(datetime.datetime.now()))
              
def schedule_listings(num_items: int):
    scheduled_times = []
    now = datetime.utcnow() + timedelta(minutes=5)
    full_hours, remainder = divmod(num_items, 10)
    for hour in range(full_hours):
        for i in range(10):
            scheduled_time = now + timedelta(hours=hour) + timedelta(minutes=6 * i)
            scheduled_times.append(scheduled_time.isoformat())
            print(f"Item {hour * 10 + i + 1} scheduled for {scheduled_time.isoformat()}")
    for i in range(remainder):
        scheduled_time = now + timedelta(hours=full_hours) + timedelta(minutes=60 / remainder * i)
        scheduled_times.append(scheduled_time.isoformat())
        print(f"Item {full_hours * 10 + i + 1} scheduled for {scheduled_time.isoformat()}")
    print(scheduled_times)
    return scheduled_times
