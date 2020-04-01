FROM python
COPY wanttoread/requirements.txt /app/wanttoread/requirements.txt
WORKDIR /app
RUN python -m pip install --upgrade pip; \
    pip3 install -r wanttoread/requirements.txt
CMD bash
