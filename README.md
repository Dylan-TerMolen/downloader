# CLI Concurrent File Downloader

This program was written in Python3 and uses multiprocessing to concurrently download files. 
This program functions by separating the file into chunks the size of file_size divided by num_threads in order to insure that each process is downloading an equal piece of the file. I was initially using the Python threading module but switched to the multiprocessing module because I believed that it was more scalable. A major bottleneck is the fact that all computers have a finite number of CPUs and so there can only be a finite number of processes. It can be greater than the number of CPUs, but it is still finite. I believe that this method is sufficiently scalable because if you were working with a faster computer or a distributed system then the program would be able to take advantage of the processing power whereas the threads would be running in the same memory space as each other and would not be as powerful.

PURPOSE:
This program was complete as part of Illumio's Internship Interview Process
