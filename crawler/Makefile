NAME = crawler
PID = $(NAME).pid

prepare:
	mkdir text
	mkdir html

 clear:
	rm text html


 stop:
# 	if [ -e $(PID) ]; then \
# 		if [ -f /proc/'head -1 $(PIDFILE)'/status ];then \
# 		/sbin/start-stop-daemon --stop --signal 2 --pidfile $(PIDFILE) --retry 3 ;\
# 		rm -f $(PIDFILE); \
# 		fi; \
# 		fi
# 	rm -f nohup.out

start:
	/sbin/start-stop-daemon -m --chroot /home/nikitakrutoy/Projects/recommndersystem/crawler --pidfile $(PID) \
	    --start --startas '/home/nikitakrutoy/Projects/recommndersystem/crawler/crawler.sh'