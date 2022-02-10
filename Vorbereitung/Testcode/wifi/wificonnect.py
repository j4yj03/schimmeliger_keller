from network import WLAN


def connect_wifi():
    wlan = WLAN(mode=WLAN.STA, antenna=WLAN.EXT_ANT)
    nets = wlan.scan()
    for net in nets:
        if net.ssid == WIFI_SSID:
            max_tries = 3
            for ntry in range(max_tries):
                #print(wlan.isconnected(), wlan.ifconfig()[0])
                if not wlan.isconnected():
                    try:
                        wlan.connect(net.ssid, auth=(net.sec, WIFI_PASS), timeout=10000)
                        print('Connecting to:', net.ssid,"\nAttempt:", str(ntry + 1) + "/" + str(max_tries))

                        while not wlan.isconnected():
                            machine.idle() # Save power while waiting.
                    except Exception as e:
                        print('ERROR:', e)
                        time.sleep(5)
                else:
                    break
            

            print("Connected to", WIFI_SSID, wlan.ifconfig(), "\n")

connect_wifi()