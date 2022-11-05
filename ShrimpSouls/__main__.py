import sys
import ShrimpSouls as ss


try:
	if __name__ == '__main__':
		if sys.argv[1] == "server":
			import ShrimpSouls.server as server
			server.run(sys.argv[2:])
		else:
			ss.main(sys.argv[1:])
			
except Exception as ex:
	raise ex
	print("ERROR: " + str(ex))
	#logger.log(ex.format_exc())