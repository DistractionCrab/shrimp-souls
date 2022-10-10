import sys
import ShrimpSouls as ss


try:
	if __name__ == '__main__':
		ss.GAME_MANAGER.main(sys.argv[1:])
			
except Exception as ex:
	raise ex
	print("ERROR: " + str(ex))