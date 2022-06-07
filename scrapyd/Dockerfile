FROM vimagick/scrapyd:py3

# Copy crawler dir
COPY . .

# install requirements
RUN pip install -r requirements.txt

# Install project
RUN poetry config virtualenvs.create false --local
RUN poetry install && rm -rf ~/.cache/pypoetry/{cache,artifacts}

WORKDIR ${WORKDIR}/vsf_crawler

CMD ["scrapyd"]