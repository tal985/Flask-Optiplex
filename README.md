# Flask Wake-on-Lan
This is a personal project meant to be put on my Raspberry Pi to help streamline my home network and automation, specifically with my Dell Optiplex.

This is a website made with the Flask framework and contains user authentication, waking my Optiplex, and polling of my Optiplex. \
This website has user authentication done by flask-login. User and Passwords should be put into "./FlaskOptiplex/static/json/users.json", which should be made based on the template in "examples.json", which is stored in the same folder. \
The wake-on-lan feature is tailored specifically to my Optiplex's MAC address. 

v2 Changelogs: \
Removed dependency on nmap by using simple socket checking instead. \
Added server-side data updates instead of using client-side to trigger the polling. \
Added Dinnerbone's MC world status checker for Nova Magia, running on port 25565, and LetItDie, running on port 25567.\
