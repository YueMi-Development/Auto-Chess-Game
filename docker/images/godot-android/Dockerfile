# Extends barichello/godot-ci:4.7 with Android SDK and JDK
# for building Android exports in CI.
FROM barichello/godot-ci:4.7

ENV DEBIAN_FRONTEND=noninteractive

# Install JDK 17 (required by modern Android Gradle) and Android SDK tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jdk \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Set Java environment
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Download and install Android command-line tools
ARG ANDROID_SDK_ROOT=/opt/android-sdk
ENV ANDROID_SDK_ROOT=$ANDROID_SDK_ROOT

RUN mkdir -p $ANDROID_SDK_ROOT/cmdline-tools && \
    cd $ANDROID_SDK_ROOT/cmdline-tools && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O cmdline-tools.zip && \
    unzip -q cmdline-tools.zip && \
    mv cmdline-tools latest && \
    rm cmdline-tools.zip

ENV PATH=$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools:$PATH

# Accept licenses and install required SDK components
RUN yes | sdkmanager --licenses > /dev/null 2>&1 || true && \
    sdkmanager --install \
    "platforms;android-34" \
    "build-tools;34.0.0" \
    "platform-tools"

# Download and install Godot export templates (including Android)
ARG GODOT_VERSION=4.7-stable
ENV GODOT_VERSION=$GODOT_VERSION

RUN mkdir -p ~/.local/share/godot/export_templates/$GODOT_VERSION && \
    wget -q https://github.com/godotengine/godot/releases/download/$GODOT_VERSION/Godot_v$GODOT_VERSION-export_templates.tpz -O /tmp/templates.tpz && \
    cd ~/.local/share/godot/export_templates/$GODOT_VERSION && \
    unzip -q /tmp/templates.tpz && \
    mv templates/* . && \
    rm -rf templates /tmp/templates.tpz
