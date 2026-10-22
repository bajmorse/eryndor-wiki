# Local, CPU-only transcription of Craig multitrack session recordings.
# Build context is this directory only; audio is bind-mounted at run time.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    HF_HOME=/cache

# Versions are pinned deliberately. faster-whisper declares `av>=11` with no
# upper bound, but PyAV 19.0.0 removed the `metadata_errors` kwarg that
# faster_whisper/audio.py passes to av.open(), so an unpinned build breaks on
# the first file it decodes. av 18.1.0 is the newest release that still works.
RUN pip install --no-cache-dir \
      "faster-whisper==1.2.1" \
      "av>=18,<19"

WORKDIR /app
COPY transcribe.py speakers.json vocab.txt ./

VOLUME ["/cache"]
ENTRYPOINT ["python", "/app/transcribe.py"]
CMD ["--input", "/in", "--output", "/out"]
