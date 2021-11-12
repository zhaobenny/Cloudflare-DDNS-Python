import http.client, json, sys

def main():
    with open('./config.json', 'r') as f:
        data = json.load(f)

    conn = http.client.HTTPSConnection("api.ipify.org")
    try:
        conn.request("GET", "/")
        res = conn.getresponse()
    except Exception as e:
        print(str(e))
        input()
        sys.exit(1)

    external_ip = (res.read()).decode("utf-8")

    conn = http.client.HTTPSConnection("api.cloudflare.com")
    payload = json.dumps({
        "type": "{}".format(data['type']),
        "name": "{}".format(data['name']),
        "content": "{}".format(external_ip)
    })

    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {}'.format(data['cfToken']),
    }

    try:
        conn.request("PUT", "/client/v4/zones/{}/dns_records/{}".format(data['zoneID'],data['recordID']), payload, headers)
        res = conn.getresponse()
    except Exception as e:
        print(str(e))
        input()
        sys.exit(1)

    res = json.loads(res.read().decode("utf-8"))

    if (res['success']):
        print("Cloudflare DDNS: Success in updating record!")
        sys.exit(0)
    else:
        print('Cloudflare DDNS: Error in updating record: {} - {}'
            .format(str(res['errors'][0]["code"]),(res['errors'][0]["message"])))
        input()
        sys.exit(1)

if __name__ == "__main__":
    main()
