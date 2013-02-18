cd /pythonweb/36coder/
/usr/bin/uwsgi -s 127.0.0.1:9090 -w blog -M -p 4 -d uwsgi.log