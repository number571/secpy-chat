.PHONY: default init install run clean
default: init clean install run
init: 
	# CHECK PROGRAMS
	pkill -15 --version
install: 
	# DOWNLOAD
	wget https://github.com/number571/hidden-lake/releases/download/v1.6.21/hle_amd64_linux
	wget https://github.com/number571/hidden-lake/releases/download/v1.6.21/hlt_amd64_linux
	# MOD EXEC & RENAME
	chmod +x hle_amd64_linux && mv hle_amd64_linux hle
	chmod +x hlt_amd64_linux && mv hlt_amd64_linux hlt
	# COPY HLE
	cp -r hle ./node1/prog_hle_1
	cp -r hle ./node2/prog_hle_2
	# COPY HLT
	cp -r hlt ./service_hlt/prog_hlt
	# COPY CLIENT
	cp -r ../main.py ./node1/main.py
	cp -r ../main.py ./node2/main.py
run: 
	# MAKEFILE RUN
	make run -C ./node1
	make run -C ./node2
	make run -C ./service_hlt
clean:
	# MAKEFILE CLEAN 
	make clean -C ./node1
	make clean -C ./node2
	make clean -C ./service_hlt
