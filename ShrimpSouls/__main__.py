import sys
import ShrimpSouls as ss

if len(sys.argv) > 0:
	if __name__ == '__main__':
		if sys.argv[1] == "server":
			import ShrimpSouls.server as server
			server.run(sys.argv[2:])
		else:
			ss.main(sys.argv[1:])
else:
	print("No command given for Shrimp Souls")