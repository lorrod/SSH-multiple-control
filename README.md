<h1> Multiple device control </h1>

This program could connect to multiple devices and execute commands.

<h2>Hellfire Control:</h2>

<h4>Main idea</h4>

It uses websocket connection between host and slave devices.

<h4>Start up</h4>

* You need program running on slave device
* Set up manually all dependencies 
* Fill the config file 
* python3 commander.py

<h2>SSH control</h2>

<h4>Start up:</h4>

 * To add or remove servers edit file config.txt and restart the programm. (check example file: config.txt.example)
 * python3 run.py

<h2>*GUI Functions Guide</h2>

 * Select servers by checkboxes on the right manually or by pressing "Select All";

 * Enter your command in the box under "Input command", then run press "Run";

 * To filter output press "Filter". If you need to see outputs for distinct servers tick them on the right side first;

 * To check the availability of all servers push the button "Check servers". Green text will mean that the server is up, otherwise text will be red;

 * To clean output press "Clean".
