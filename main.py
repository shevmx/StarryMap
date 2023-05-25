def main():
	import logging

	# Log file name
	log_name_file = "data/logs/starry_map.log"

	# Create a custom logger
	logger = logging.getLogger(__name__)

	# Error logger handler
	logger.setLevel(logging.INFO)
	file_handler = logging.FileHandler(log_name_file)
	file_format = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', datefmt='%H:%M:%S')
	file_handler.setFormatter(file_format)
	logger.addHandler(file_handler)

	try:
	  import app
	except Exception as e:
	  logger.error("Exception occurred", exc_info=True)

	# Add a space in the end of the file
	with open(log_name_file, "a") as add_space_file:
		add_space_file.write("\n")


if __name__ == "__main__":
	main()

