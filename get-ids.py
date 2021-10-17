import time, sys, json, http.client

def checkResponse(res) -> list:
    res = json.loads(res.read().decode("utf-8"))
    if (not res['success']):
        print('Error in requesting Cloudflare API: {} - {}'
            .format(str(res['errors'][0]["code"]),(res['errors'][0]["message"])))
        input()
        sys.exit(1)

    return res['result']

def requestCloudflare(headers, query) -> list:
    payload = ''
    conn = http.client.HTTPSConnection("api.cloudflare.com")
    try:
        conn.request("GET", query, payload, headers)
        res = conn.getresponse()
    except Exception as e:
        print(str(e))
        input()
        sys.exit(1)

    res = checkResponse(res)
    return res

def main():
    with open('./config.json', 'r') as f:
        data = json.load(f)

    headers = {
        'Authorization': 'Bearer {}'.format(data['cfToken'])
    }
    res = requestCloudflare(headers, "/client/v4/zones/")

    if (len(res) != 1):
        data['zoneID'] = res[0]['id']
    else:
        print("\n Zones:")
        print("# | Domain")
        for idx, zone in enumerate(res):
            print("{} | {}".format(str(idx + 1), zone['name'].ljust(1)))
        zoneNum = int(input("\n Enter the zone #: ")) - 1
        data['zoneID'] = res[zoneNum]['id']

    zone = "/client/v4/zones/{}/dns_records".format(data['zoneID'])
    res = requestCloudflare(headers, zone)

    print("\n Records:")
    print("{} | {}| {} | {}".format('#'.ljust(2), 'name'.ljust(35),'type'.ljust(5), 'content'))
    for idx, record in enumerate(res):
        print("{} | {}| {} | {}".format(str(idx + 1).ljust(2), record['name'].ljust(35),record['type'].ljust(5), record['content']))
    recordNum = int(input("\n Enter the record # to be changed: ")) - 1

    data['recordID'] = res[recordNum]['id']
    data['name'] = res[recordNum]['name']
    data['type'] = res[recordNum]['type']

    with open("config.json", "w") as f:
        json.dump(data, f)

    print("\n Config saved, use update-record.py to update DNS record")
    time.sleep(3)
    sys.exit(0)

if __name__ == "__main__":
    main()
