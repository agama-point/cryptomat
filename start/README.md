> sudo chmod +x /home/pi/octopus-cryptomat/start3.py

header: #!/usr/bin/python3

> sudo nano /etc/systemd/system/octopus.service
:
-------------------------------------------
<pre>
[Unit]
Description=OctopusEngine Super CryptoMachine
After=network.target

[Service]
ExecStart=/home/pi/octopus-cryptomat/start3.py
WorkingDirectory=/home/pi/octopus-cryptomat

[Install]
WantedBy=multi-user.target
</pre>
-------------------------------------------

> systemctl daemon-reload
> systemctl start octopus

> systemctl list-units :
ok:
octopus.service  loaded active running   OctopusEngine Super CryptoMachine

> systemctl enable octopus

> sudo reboot

> journalctl -fu octopus :
root@octopus3:/home/pi# journalctl -fu octopus
-- Logs begin at Thu 2017-09-21 08:59:19 UTC. --
Sep 21 08:59:24 octopus3 systemd[1]: Starting OctopusEngine Super CryptoMachine...
Sep 21 08:59:24 octopus3 systemd[1]: Started OctopusEngine Super CryptoMachine.
Sep 21 08:59:26 octopus3 start3.py[520]: -----------------------------------one Loop
Sep 21 08:59:26 octopus3 start3.py[520]: >>> octopusengine.org/api --- getServerTime()
...
