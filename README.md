TCP_Proxy-Server
================

A Multi-Threaded HTTP Proxy Server 

*** README ***

NAME : SAVITHRU M LOKANATH
SOURCE FILE : SavithruLokanath_proxy.py
MULTI-THREADING ENABLED
CACHING ENABLED WITH EXPIRY (5 MINUTES)
BLOCKS JPG FILES
CACHE PATH : /Users/savithru/Desktop/prog3/temp1

Steps to implement a proxy server on your local machine - 

1) OPEN the source file SavithruLokanath_proxy.py using any python interpreters or RUN this command - 
   python SavithruLokanath_proxy.py in terminal
4) The cache path is set to /Users/savithru/Desktop/prog3/temp1 for my local machine. Create a folder on desktop
   (preferable) & set the path to this folder. This is where you would want to store the cached files   
5) The port number is set to 9600 initially. CHANGE to a value greater than 8000 if needed
6) Once the source file is running, OPEN any browser (MOZILLA FIREFOX, GOOGLE CHROME, APPLE SAFARI) and navigate to 
   browser settings to get the proxy settings tab. Here choose the manual proxy configuration & enter 
   IP : localhost
   Port Number : 9600
7) Enter the desired URL & observe that the data will be fetched from the server by the proxy & returned to the 
   browser. A copy of the file is also stored in the path specified in the begining. This file will expire after 5 minutes &      will be deleted
8) A log file named proxyserver.log will be created in the working directory which stores all the information required 
   like IP address, port used, file fetched from cache, cache files deleted after timeout, etc. 
9) If the same file is requested again, then the proxy will send the file stored in the cache instead of fetching it 
   again from the server (Message seen : Sent from cache)
10) Multi-Threading can be tested by opening another session with the server on a differnt browser

IMPORTANT : The program won't create a folder for the cache files to be stored. It should be done manually. Make sure 				you mention the correct path name. 
