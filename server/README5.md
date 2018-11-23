Using python2.7,with media in same directory as the $PWD when mininet is launched
Launch mininet with:
sudo mn --topo single,3

EACH TIME we exit controller, R and S close with it.
Assuming '10.0.0.x' is mininet's address domain:
mininet> h1 python server.py & # server
mininet> h2 python renderer.py & # renderer
mininet> h3 python controller.py # host

More reference: 
port 5300 = controller to server
port 5400 = controller to renderer
port 5500 = renderer to server