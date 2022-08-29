FROM python
COPY sim2.py /sim2.py
COPY tagfile.txt /tagfile.txt
RUN pip3 install requests 
CMD python /sim2.py


