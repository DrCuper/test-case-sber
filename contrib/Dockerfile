FROM registry.access.redhat.com/ubi9/python-312@sha256:b918c875137771b4502d2fa481845e72a784f31650926f245c2196555c10c56b AS build

USER 0

RUN dnf install -y \
        gcc \
        gcc-c++ \
        make \
        binutils \
        findutils \
        which

WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TMPDIR=/tmp

COPY . .

RUN pip install --upgrade pip setuptools wheel && \
    pip install \
      pyinstaller \
      staticx \
      tzdata && \
    pip install . 

RUN mv contrib/run_flower.py . && \
    pyinstaller \
      --clean \
      --noconfirm \
      --onefile \
      --noupx \
      --paths . \
      --name flower \
      --collect-all flower \
      --collect-all tornado \
      --collect-all prometheus_client \
      --collect-all tzdata \
      --hidden-import flower.__main__ \
      /build/run_flower.py

RUN curl -fL -o patchelf.tar.gz \
    https://github.com/NixOS/patchelf/releases/download/0.18.0/patchelf-0.18.0-x86_64.tar.gz && \
    tar -xzf patchelf.tar.gz && \
    install -m 0755 bin/patchelf /usr/local/bin/patchelf && \
    python3 -m pip install --upgrade --force-reinstall "setuptools==75.8.0" && \
    staticx /build/dist/flower /build/flower_static

RUN mkdir -p /rootfs/tmp /rootfs/etc/ssl/certs /rootfs/app && \
    cp /build/flower_static /rootfs/app/flower

FROM scratch

ENV TMPDIR=/tmp \
    PYTHONUNBUFFERED=1

COPY --from=build /rootfs/ /

ENTRYPOINT ["/app/flower"]
