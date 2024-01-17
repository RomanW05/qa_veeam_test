# INSTALLATION
	Open a terminal window
	mkdir roman_walden_test
	cd roman_walden_test
	python -m venv venv
	venv\Scripts\Activate
	git clone https://github.com/RomanW05/qa_veeam_test.git
	cd qa_veeam_test
	pip install -r requirements.txt

# EXECUTION
	python sync_source_replica.py <source_path> <replica_path> <synchronization interval in seconds> <log_path>