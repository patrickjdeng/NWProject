Launch mininet with:
sudo mn --topo single,3
h1 python server.py & # server
h2 python renderer.py & # renderer
h3 python controller.py # host
port 5300 = controller to server
port 5400 = controller to renderer
port 5500 = renderer to server