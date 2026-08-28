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

# Download and install Android command-line tools at /usr/lib/android-sdk (matches base image path)
ENV ANDROID_HOME=/usr/lib/android-sdk
ENV PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$PATH

RUN mkdir -p $ANDROID_HOME/cmdline-tools && \
    cd $ANDROID_HOME/cmdline-tools && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O cmdline-tools.zip && \
    unzip -qo cmdline-tools.zip && \
    mv -T cmdline-tools latest 2>/dev/null || mv cmdline-tools latest && \
    rm cmdline-tools.zip

# Accept licenses and install required SDK components (base image already has 33.0.2 / android-33)
RUN yes | sdkmanager --licenses > /dev/null 2>&1 || true && \
    sdkmanager --install \
    "platforms;android-34" \
    "build-tools;34.0.0" \
    "platform-tools"

# Download and install Android export templates (base image already has Linux templates at 4.7.stable)
# Templates on godot-builds/releases use dot-free tag: 4.7-stable
RUN wget -q https://github.com/godotengine/godot-builds/releases/download/4.7-stable/Godot_v4.7-stable_export_templates.tpz -O /tmp/templates.tpz && \
    unzip -qo /tmp/templates.tpz -d /tmp/templates && \
    mkdir -p ~/.local/share/godot/export_templates/4.7.stable && \
    cp /tmp/templates/templates/* ~/.local/share/godot/export_templates/4.7.stable/ && \
    rm -rf /tmp/templates*

# Configure Android SDK paths in Godot editor settings
RUN mkdir -p ~/.config/godot && \
    echo '[gd_resource type="EditorSettings" format=3]' > ~/.config/godot/editor_settings-4.7.tres && \
    echo '[resource]' >> ~/.config/godot/editor_settings-4.7.tres && \
    echo 'export/android/java_sdk_path = "/usr/lib/jvm/java-17-openjdk-amd64"' >> ~/.config/godot/editor_settings-4.7.tres && \
    echo 'export/android/android_sdk_path = "/usr/lib/android-sdk"' >> ~/.config/godot/editor_settings-4.7.tres && \
    echo 'export/android/debug_keystore = ""' >> ~/.config/godot/editor_settings-4.7.tres && \
    echo 'export/android/debug_keystore_user = ""' >> ~/.config/godot/editor_settings-4.7.tres && \
    echo 'export/android/debug_keystore_pass = ""' >> ~/.config/godot/editor_settings-4.7.tres && \
    echo 'export/android/timestamping_authority_url = ""' >> ~/.config/godot/editor_settings-4.7.tres
