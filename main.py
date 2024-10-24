import multiprocessing, sys, requests, time, json, hashlib, yaml

HLE_URL = "" # it is being overwritten
HLT_URL = "" # it is being overwritten
FRIENDS = {} # it is being overwritten

def main():
    init_load_config("config.yml")
    init_friends_list()
    parallel_run(input_task, output_task)

def init_friends_list():
    global FRIENDS
    
    # GET FRIENDS FROM HLE
    resp_hle = requests.get(
        HLE_URL+"/api/config/friends"
    )
    if resp_hle.status_code != 200:
        print("@ got response error from HLE (/api/config/friends)")
        exit(1)
    
    friends_list = json.loads(resp_hle.content)
    for v in friends_list:
        FRIENDS[v['alias_name']] = {}
    
def init_load_config(app_cfg):
    global HLE_URL, HLT_URL

    with open(app_cfg, "r") as stream:
        try:
            app_config_loaded = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print("@ failed load app config")
            exit(3)
    
    HLT_URL = "http://" + app_config_loaded["hlt_host"]
    HLE_URL = "http://" + app_config_loaded["hle_host"]

def parallel_run(*fns):
    proc = []
    for fn in fns:
        p = multiprocessing.Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()

def output_task():
    # GET SETTING = MESSAGES_CAPACITY
    resp_hlt = requests.get(
        HLT_URL+"/api/config/settings"
    )
    if resp_hlt.status_code != 200:
        print("@ got response error from HLT (/api/config/settings)")
        exit(1)
    
    try:
        messages_capacity = json.loads(resp_hlt.content)["messages_capacity"]
    except ValueError:
        print("@ got response invalid data from HLT (/api/config/settings)")
        exit(2)
    
    global_pointer = -1
    while True:
        # GET INITIAL POINTER OF MESSAGES
        try:
            resp_hlt = requests.get(
                HLT_URL+"/api/storage/pointer"
            )
            if resp_hlt.status_code != 200:
                print("@ got response error from HLT (/api/storage/pointer)")
                time.sleep(1)
                continue 
        except:
            print("@ failed do request HLT (/api/storage/pointer)")
            continue

        try:
            pointer = int(resp_hlt.content)
        except ValueError:
            print("@ got response invalid data from HLT (/api/storage/pointer)")
            time.sleep(1)
            continue

        if global_pointer == -1:
            global_pointer = pointer

        if global_pointer == pointer:
            time.sleep(1)
            continue
    
        # GET ALL MESSAGES FROM CURRENT POINTER TO GOT POINTER
        while global_pointer != pointer:
            global_pointer = (global_pointer + 1) % messages_capacity

            try:
                resp_hlt = requests.get(
                    HLT_URL+"/api/storage/hashes?id="+f"{(global_pointer - 1) % messages_capacity}"
                )
                if resp_hlt.status_code != 200:
                    break 
            except:
                print("@ failed do request HLT (/api/storage/hashes?id="+f"{(global_pointer - 1) % messages_capacity})")
                continue

            try:
                resp_hlt = requests.get(
                    HLT_URL+"/api/network/message?hash="+f"{resp_hlt.content.decode("utf8")}"
                )
                if resp_hlt.status_code != 200:
                    break 
            except:
                print("@ failed do request HLT (/api/network/message?hash="+f"{resp_hlt.content.decode("utf8")})")
                continue
            
            # TRY DECRYPT GOT MESSAGE
            try:
                resp_hle = requests.post(
                    HLE_URL+"/api/message/decrypt", 
                    data=resp_hlt.content
                )
                if resp_hle.status_code != 200:
                    continue 
            except:
                print("@ failed do request HLE (/api/message/decrypt)")
                continue

            try:
                json_resp = json.loads(resp_hle.content)
            except ValueError:
                print("@ got response invalid data from HLE (/api/message/decrypt)")
                continue
        
            # CHECK GOT PUBLIC KEY IN FRIENDS LIST
            friend_name = json_resp["alias_name"]
            if friend_name not in FRIENDS:
                continue 

            got_data = bytes.fromhex(json_resp["hex_data"]).decode('utf-8')
            print(f"[{friend_name}]: {got_data}\n> ", end="")

def input_task():
    friend = ""

    sys.stdin = open(0)
    while True:
        msg = input("> ")
        if len(msg) == 0:
            print("@ got null message")
            continue

        if msg.startswith("/friend "):
            try:
                _friend = msg[len("/friend "):].strip()
                _ok = FRIENDS[_friend]
            except KeyError:
                print("@ got invalid friend name")
                continue
            friend = _friend
            continue

        if friend == "":
            print("@ friend is null, use /friend to set")
            continue 

        try:
            resp_hle = requests.post(
                HLE_URL+"/api/message/encrypt", 
                json={"alias_name": friend, "hex_data": msg.encode("utf-8").hex()}
            )
            if resp_hle.status_code != 200:
                print("@ got response error from HLE (/api/message/encrypt)")
                continue 
        except:
            print("@ failed do request HLE (/api/message/encrypt)")
            continue
            
        try:
            resp_hlt = requests.post(
                HLT_URL+"/api/network/message", 
                data=resp_hle.content
            )
            if resp_hlt.status_code != 200:
                print("@ got response error from HLT (/api/network/message)")
                continue 
        except:
            print("@ failed do request HLT (/api/network/message)")
            continue

if __name__ == "__main__":
    main()
