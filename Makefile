.PHONY: install 1 2 

install:
	uv pip install requests beautifulsoup4 urllib3

2:
	@python3 lost_bike.py

1: 
	@python3 sato.py