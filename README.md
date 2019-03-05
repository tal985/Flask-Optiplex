# Flask Wake-on-Lan + TCP Port Checker
Requires nmap in the PATH environment variable. \
This is a personal project meant to be put on my Raspberry Pi to help streamline my home network and automation, specifically with the Optiplex. \
This is a website made with the Flask framework and contains user authentication, waking my Optiplex, 15s polling of my Optiplex, and TCP port checking in general. \
This website has user authentication done by flask-login. User and Passwords should be put into "./FlaskOptiplex/static/json/users.json", which should be made based on the template in "examples.json", which is stored in the same folder \
The wake on lan feature is tailored specifically to my Optiplex's MAC address. \
The TCP portchecking is done by a wrapper to nmap.
