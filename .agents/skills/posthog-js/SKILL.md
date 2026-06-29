---
name: posthog-js
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging posthog-js. Use this skill whenever modifying posthog-js configurations or adding related functionality.
---
# posthog-js

## File Tree

```text
posthog-js/
├── assets
├── modules
│   └── posthog-js
│       ├── examples
│       │   ├── example-ai-anthropic
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   ├── streaming.ts
│       │   │   └── tsconfig.json
│       │   ├── example-ai-aws-bedrock
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-azure-openai
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-cerebras
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-cloudflare-ai-gateway
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-cohere
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-convex
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── generate.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-dedalus
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-deepseek
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-fireworks-ai
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-gemini
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── image-generation.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   ├── streaming.ts
│       │   │   └── tsconfig.json
│       │   ├── example-ai-groq
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-helicone
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-hugging-face
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-instructor
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── extract.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-langchain
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── callback-handler.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-langgraph
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── agent.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-mastra
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   ├── tsconfig.json
│       │   │   └── workflow.ts
│       │   ├── example-ai-mistral
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-ollama
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-openai
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat-completions-streaming.ts
│       │   │   ├── chat-completions.ts
│       │   │   ├── embeddings.ts
│       │   │   ├── image-generation.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   ├── responses-streaming.ts
│       │   │   ├── responses.ts
│       │   │   ├── transcription.ts
│       │   │   └── tsconfig.json
│       │   ├── example-ai-openai-agents
│       │   │   ├── multi-agent.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-workspace.yaml
│       │   │   ├── single-agent.ts
│       │   │   └── tsconfig.json
│       │   ├── example-ai-openrouter
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-perplexity
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-portkey
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-together-ai
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-vercel-ai
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── anthropic-streaming.ts
│       │   │   ├── anthropic.ts
│       │   │   ├── generate-object.ts
│       │   │   ├── generate-text.ts
│       │   │   ├── google-streaming.ts
│       │   │   ├── google.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   ├── stream-object.ts
│       │   │   ├── stream-text.ts
│       │   │   └── tsconfig.json
│       │   ├── example-ai-vercel-ai-gateway
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-ai-xai
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── chat.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-cloudflare
│       │   │   ├── src
│       │   │   │   └── index.ts
│       │   │   ├── .editorconfig
│       │   │   ├── .gitignore
│       │   │   ├── .npmrc
│       │   │   ├── .prettierrc
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   ├── tsconfig.json
│       │   │   └── wrangler.toml
│       │   ├── example-cloudflare-hono-vite
│       │   │   ├── public
│       │   │   │   ├── .assetsignore
│       │   │   │   └── favicon.ico
│       │   │   ├── src
│       │   │   │   └── index.ts
│       │   │   ├── .gitignore
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   ├── tsconfig.json
│       │   │   ├── vite.config.ts
│       │   │   └── wrangler.jsonc
│       │   ├── example-cloudflare-kv-cache
│       │   │   ├── src
│       │   │   │   ├── cache.ts
│       │   │   │   └── worker.ts
│       │   │   ├── .gitignore
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   ├── tsconfig.json
│       │   │   └── wrangler.toml
│       │   ├── example-convex
│       │   │   ├── convex
│       │   │   │   ├── _generated
│       │   │   │   │   ├── api.d.ts
│       │   │   │   │   ├── api.js
│       │   │   │   │   ├── dataModel.d.ts
│       │   │   │   │   ├── server.d.ts
│       │   │   │   │   └── server.js
│       │   │   │   ├── aiSdk
│       │   │   │   │   ├── manualCapture.ts
│       │   │   │   │   └── openTelemetry.ts
│       │   │   │   ├── convexAgent
│       │   │   │   │   ├── manualCapture.ts
│       │   │   │   │   └── openTelemetry.ts
│       │   │   │   ├── README.md
│       │   │   │   ├── convex.config.ts
│       │   │   │   ├── crons.ts
│       │   │   │   ├── example.test.ts
│       │   │   │   ├── example.ts
│       │   │   │   ├── polyfills.ts
│       │   │   │   ├── posthog.ts
│       │   │   │   ├── schema.ts
│       │   │   │   ├── setup.test.ts
│       │   │   │   └── tsconfig.json
│       │   │   ├── src
│       │   │   │   ├── App.css
│       │   │   │   ├── App.tsx
│       │   │   │   ├── main.tsx
│       │   │   │   └── vite-env.d.ts
│       │   │   ├── .gitignore
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── index.html
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   ├── tsconfig.json
│       │   │   └── vite.config.ts
│       │   ├── example-expo-53
│       │   │   ├── android
│       │   │   │   ├── app
│       │   │   │   │   ├── src
│       │   │   │   │   │   ├── debug
│       │   │   │   │   │   │   └── AndroidManifest.xml
│       │   │   │   │   │   └── main
│       │   │   │   │   │       ├── java
│       │   │   │   │   │       │   └── com
│       │   │   │   │   │       │       └── marandaneto
│       │   │   │   │   │       │           └── exampleexpo53
│       │   │   │   │   │       │               ├── MainActivity.kt
│       │   │   │   │   │       │               └── MainApplication.kt
│       │   │   │   │   │       ├── res
│       │   │   │   │   │       │   ├── drawable
│       │   │   │   │   │       │   │   ├── ic_launcher_background.xml
│       │   │   │   │   │       │   │   └── rn_edit_text_material.xml
│       │   │   │   │   │       │   ├── drawable-hdpi
│       │   │   │   │   │       │   │   └── splashscreen_logo.png
│       │   │   │   │   │       │   ├── drawable-mdpi
│       │   │   │   │   │       │   │   └── splashscreen_logo.png
│       │   │   │   │   │       │   ├── drawable-xhdpi
│       │   │   │   │   │       │   │   └── splashscreen_logo.png
│       │   │   │   │   │       │   ├── drawable-xxhdpi
│       │   │   │   │   │       │   │   └── splashscreen_logo.png
│       │   │   │   │   │       │   ├── drawable-xxxhdpi
│       │   │   │   │   │       │   │   └── splashscreen_logo.png
│       │   │   │   │   │       │   ├── mipmap-anydpi-v26
│       │   │   │   │   │       │   │   ├── ic_launcher.xml
│       │   │   │   │   │       │   │   └── ic_launcher_round.xml
│       │   │   │   │   │       │   ├── mipmap-hdpi
│       │   │   │   │   │       │   │   ├── ic_launcher.webp
│       │   │   │   │   │       │   │   ├── ic_launcher_foreground.webp
│       │   │   │   │   │       │   │   └── ic_launcher_round.webp
│       │   │   │   │   │       │   ├── mipmap-mdpi
│       │   │   │   │   │       │   │   ├── ic_launcher.webp
│       │   │   │   │   │       │   │   ├── ic_launcher_foreground.webp
│       │   │   │   │   │       │   │   └── ic_launcher_round.webp
│       │   │   │   │   │       │   ├── mipmap-xhdpi
│       │   │   │   │   │       │   │   ├── ic_launcher.webp
│       │   │   │   │   │       │   │   ├── ic_launcher_foreground.webp
│       │   │   │   │   │       │   │   └── ic_launcher_round.webp
│       │   │   │   │   │       │   ├── mipmap-xxhdpi
│       │   │   │   │   │       │   │   ├── ic_launcher.webp
│       │   │   │   │   │       │   │   ├── ic_launcher_foreground.webp
│       │   │   │   │   │       │   │   └── ic_launcher_round.webp
│       │   │   │   │   │       │   ├── mipmap-xxxhdpi
│       │   │   │   │   │       │   │   ├── ic_launcher.webp
│       │   │   │   │   │       │   │   ├── ic_launcher_foreground.webp
│       │   │   │   │   │       │   │   └── ic_launcher_round.webp
│       │   │   │   │   │       │   ├── values
│       │   │   │   │   │       │   │   ├── colors.xml
│       │   │   │   │   │       │   │   ├── strings.xml
│       │   │   │   │   │       │   │   └── styles.xml
│       │   │   │   │   │       │   └── values-night
│       │   │   │   │   │       │       └── colors.xml
│       │   │   │   │   │       └── AndroidManifest.xml
│       │   │   │   │   ├── build.gradle
│       │   │   │   │   ├── debug.keystore
│       │   │   │   │   └── proguard-rules.pro
│       │   │   │   ├── gradle
│       │   │   │   │   └── wrapper
│       │   │   │   │       ├── gradle-wrapper.jar
│       │   │   │   │       └── gradle-wrapper.properties
│       │   │   │   ├── .gitignore
│       │   │   │   ├── build.gradle
│       │   │   │   ├── gradle.properties
│       │   │   │   ├── gradlew
│       │   │   │   ├── gradlew.bat
│       │   │   │   └── settings.gradle
│       │   │   ├── app
│       │   │   │   ├── (tabs)
│       │   │   │   │   ├── _layout.tsx
│       │   │   │   │   ├── error-tracking.tsx
│       │   │   │   │   ├── explore.tsx
│       │   │   │   │   ├── index.tsx
│       │   │   │   │   ├── logs.tsx
│       │   │   │   │   └── tracing-headers.tsx
│       │   │   │   ├── +not-found.tsx
│       │   │   │   ├── _layout.tsx
│       │   │   │   ├── posthog.tsx
│       │   │   │   └── surveys.tsx
│       │   │   ├── assets
│       │   │   │   ├── fonts
│       │   │   │   │   └── SpaceMono-Regular.ttf
│       │   │   │   └── images
│       │   │   │       ├── adaptive-icon.png
│       │   │   │       ├── favicon.png
│       │   │   │       ├── icon.png
│       │   │   │       ├── partial-react-logo.png
│       │   │   │       ├── react-logo.png
│       │   │   │       ├── react-logo@2x.png
│       │   │   │       ├── react-logo@3x.png
│       │   │   │       └── splash-icon.png
│       │   │   ├── components
│       │   │   │   ├── ui
│       │   │   │   │   ├── IconSymbol.ios.tsx
│       │   │   │   │   ├── IconSymbol.tsx
│       │   │   │   │   ├── TabBarBackground.ios.tsx
│       │   │   │   │   └── TabBarBackground.tsx
│       │   │   │   ├── Collapsible.tsx
│       │   │   │   ├── ExternalLink.tsx
│       │   │   │   ├── HapticTab.tsx
│       │   │   │   ├── HelloWave.tsx
│       │   │   │   ├── ParallaxScrollView.tsx
│       │   │   │   ├── ThemedText.tsx
│       │   │   │   └── ThemedView.tsx
│       │   │   ├── constants
│       │   │   │   └── Colors.ts
│       │   │   ├── hooks
│       │   │   │   ├── useColorScheme.ts
│       │   │   │   ├── useColorScheme.web.ts
│       │   │   │   └── useThemeColor.ts
│       │   │   ├── ios
│       │   │   │   ├── exampleexpo53
│       │   │   │   │   ├── Images.xcassets
│       │   │   │   │   │   ├── AppIcon.appiconset
│       │   │   │   │   │   │   ├── App-Icon-1024x1024@1x.png
│       │   │   │   │   │   │   └── Contents.json
│       │   │   │   │   │   ├── SplashScreenBackground.colorset
│       │   │   │   │   │   │   └── Contents.json
│       │   │   │   │   │   ├── SplashScreenLogo.imageset
│       │   │   │   │   │   │   ├── Contents.json
│       │   │   │   │   │   │   ├── image.png
│       │   │   │   │   │   │   ├── image@2x.png
│       │   │   │   │   │   │   └── image@3x.png
│       │   │   │   │   │   └── Contents.json
│       │   │   │   │   ├── Supporting
│       │   │   │   │   │   └── Expo.plist
│       │   │   │   │   ├── AppDelegate.swift
│       │   │   │   │   ├── Info.plist
│       │   │   │   │   ├── PrivacyInfo.xcprivacy
│       │   │   │   │   ├── SplashScreen.storyboard
│       │   │   │   │   ├── exampleexpo53-Bridging-Header.h
│       │   │   │   │   └── exampleexpo53.entitlements
│       │   │   │   ├── exampleexpo53.xcodeproj
│       │   │   │   │   ├── xcshareddata
│       │   │   │   │   │   └── xcschemes
│       │   │   │   │   │       └── exampleexpo53.xcscheme
│       │   │   │   │   └── project.pbxproj
│       │   │   │   ├── exampleexpo53.xcworkspace
│       │   │   │   │   └── contents.xcworkspacedata
│       │   │   │   ├── .gitignore
│       │   │   │   ├── .xcode.env
│       │   │   │   ├── Podfile
│       │   │   │   └── Podfile.properties.json
│       │   │   ├── scripts
│       │   │   │   └── reset-project.js
│       │   │   ├── .eslintrc.cjs
│       │   │   ├── .gitignore
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── app.json
│       │   │   ├── eas.json
│       │   │   ├── eslint.config.js
│       │   │   ├── export-posthog-cli.sh
│       │   │   ├── metro.config.js
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-gcp-functions
│       │   │   ├── .gitignore
│       │   │   ├── .npmrc
│       │   │   ├── index.js
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   └── pnpm-workspace.yaml
│       │   ├── example-hono
│       │   │   ├── src
│       │   │   │   └── index.ts
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-nestjs
│       │   │   ├── src
│       │   │   │   ├── app.controller.ts
│       │   │   │   ├── app.module.ts
│       │   │   │   └── main.ts
│       │   │   ├── .npmrc
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-next-app-router
│       │   │   ├── app
│       │   │   │   ├── auth
│       │   │   │   │   └── page.tsx
│       │   │   │   ├── capture
│       │   │   │   │   └── page.tsx
│       │   │   │   ├── client-hooks
│       │   │   │   │   ├── ClientHooksContent.tsx
│       │   │   │   │   └── page.tsx
│       │   │   │   ├── components
│       │   │   │   │   ├── ConsentBanner.tsx
│       │   │   │   │   └── Nav.tsx
│       │   │   │   ├── server-flags
│       │   │   │   │   └── page.tsx
│       │   │   │   ├── ssr-bootstrap
│       │   │   │   │   └── page.tsx
│       │   │   │   ├── globals.css
│       │   │   │   ├── layout.tsx
│       │   │   │   └── page.tsx
│       │   │   ├── .gitignore
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── middleware.ts
│       │   │   ├── next.config.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-workspace.yaml
│       │   │   ├── postcss.config.mjs
│       │   │   ├── tsconfig.json
│       │   │   └── vercel.json
│       │   ├── example-nextjs
│       │   │   ├── src
│       │   │   │   └── app
│       │   │   │       ├── actions.ts
│       │   │   │       ├── layout.tsx
│       │   │   │       ├── page.tsx
│       │   │   │       └── posthog.tsx
│       │   │   ├── .gitignore
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── eslint.config.mjs
│       │   │   ├── next.config.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-node
│       │   │   ├── diagnostics
│       │   │   │   ├── .eslintrc.js
│       │   │   │   ├── README.md
│       │   │   │   ├── heap-snapshot-helper.js
│       │   │   │   └── memory-leak-diagnostic.js
│       │   │   ├── .gitignore
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── example.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   ├── server.ts
│       │   │   └── tsconfig.json
│       │   ├── example-nuxt
│       │   │   ├── pages
│       │   │   │   ├── feature-flags.vue
│       │   │   │   ├── index.vue
│       │   │   │   └── page-error.vue
│       │   │   ├── server
│       │   │   │   ├── routes
│       │   │   │   │   └── error.ts
│       │   │   │   └── tsconfig.json
│       │   │   ├── utils
│       │   │   │   └── errorUtils.ts
│       │   │   ├── .gitignore
│       │   │   ├── .npmrc
│       │   │   ├── .prettierrc
│       │   │   ├── README.md
│       │   │   ├── app.vue
│       │   │   ├── nuxt.config.ts
│       │   │   ├── package.json
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example-sdk_dr
│       │   │   ├── README.md
│       │   │   ├── test-feature-flag-misconfiguration.html
│       │   │   └── test-time-based-detection.html
│       │   ├── example-web
│       │   │   ├── public
│       │   │   │   ├── favicon.ico
│       │   │   │   ├── index.html
│       │   │   │   ├── logo192.png
│       │   │   │   ├── logo512.png
│       │   │   │   ├── manifest.json
│       │   │   │   └── robots.txt
│       │   │   ├── src
│       │   │   │   ├── App.css
│       │   │   │   ├── App.test.tsx
│       │   │   │   ├── App.tsx
│       │   │   │   ├── index.css
│       │   │   │   ├── index.tsx
│       │   │   │   ├── logo.svg
│       │   │   │   ├── posthog.ts
│       │   │   │   ├── react-app-env.d.ts
│       │   │   │   ├── reportWebVitals.ts
│       │   │   │   └── setupTests.ts
│       │   │   ├── .gitignore
│       │   │   ├── .npmrc
│       │   │   ├── README.md
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   ├── example_rn_macos
│       │   │   ├── .bundle
│       │   │   │   └── config
│       │   │   ├── __tests__
│       │   │   │   └── App-test.tsx
│       │   │   ├── macos
│       │   │   │   ├── example_rn_macos-macOS
│       │   │   │   │   ├── Assets.xcassets
│       │   │   │   │   │   ├── AppIcon.appiconset
│       │   │   │   │   │   │   └── Contents.json
│       │   │   │   │   │   └── Contents.json
│       │   │   │   │   ├── Base.lproj
│       │   │   │   │   │   └── Main.storyboard
│       │   │   │   │   ├── AppDelegate.h
│       │   │   │   │   ├── AppDelegate.mm
│       │   │   │   │   ├── Info.plist
│       │   │   │   │   ├── example_rn_macos.entitlements
│       │   │   │   │   └── main.m
│       │   │   │   ├── example_rn_macos.xcodeproj
│       │   │   │   │   ├── xcshareddata
│       │   │   │   │   │   └── xcschemes
│       │   │   │   │   │       └── example_rn_macos-macOS.xcscheme
│       │   │   │   │   └── project.pbxproj
│       │   │   │   ├── example_rn_macos.xcworkspace
│       │   │   │   │   ├── xcshareddata
│       │   │   │   │   │   └── IDEWorkspaceChecks.plist
│       │   │   │   │   └── contents.xcworkspacedata
│       │   │   │   ├── .gitignore
│       │   │   │   ├── .xcode.env
│       │   │   │   └── Podfile
│       │   │   ├── .eslintrc.js
│       │   │   ├── .gitignore
│       │   │   ├── .node-version
│       │   │   ├── .npmrc
│       │   │   ├── .prettierrc.js
│       │   │   ├── .watchmanconfig
│       │   │   ├── App.tsx
│       │   │   ├── Gemfile
│       │   │   ├── Makefile
│       │   │   ├── README.md
│       │   │   ├── app.json
│       │   │   ├── babel.config.js
│       │   │   ├── index.js
│       │   │   ├── launch.json
│       │   │   ├── metro.config.js
│       │   │   ├── package.json
│       │   │   ├── pnpm-lock.yaml
│       │   │   ├── pnpm-workspace.yaml
│       │   │   └── tsconfig.json
│       │   └── README.md
│       ├── packages
│       │   ├── browser
│       │   │   ├── playground
│       │   │   │   ├── chakra-emotion
│       │   │   │   │   ├── src
│       │   │   │   │   │   ├── app.tsx
│       │   │   │   │   │   ├── main.tsx
│       │   │   │   │   │   └── vite-env.d.ts
│       │   │   │   │   ├── index.html
│       │   │   │   │   ├── package.json
│       │   │   │   │   ├── pnpm-lock.yaml
│       │   │   │   │   ├── pnpm-workspace.yaml
│       │   │   │   │   ├── tsconfig.app.json
│       │   │   │   │   ├── tsconfig.json
│       │   │   │   │   ├── tsconfig.node.json
│       │   │   │   │   └── vite.config.ts
│       │   │   │   ├── copy-autocapture
│       │   │   │   │   └── demo.html
│       │   │   │   ├── csp-violations
│       │   │   │   │   ├── src
│       │   │   │   │   │   ├── main.js
│       │   │   │   │   │   └── posthog.js
│       │   │   │   │   ├── static
│       │   │   │   │   │   └── styles.css
│       │   │   │   │   ├── .gitignore
│       │   │   │   │   ├── .npmrc
│       │   │   │   │   ├── README.md
│       │   │   │   │   ├── package.json
│       │   │   │   │   ├── pnpm-lock.yaml
│       │   │   │   │   ├── pnpm-workspace.yaml
│       │   │   │   │   ├── rollup.config.mjs
│       │   │   │   │   └── server.js
│       │   │   │   ├── css-layers
│       │   │   │   │   └── index.html
│       │   │   │   ├── cypress
│       │   │   │   │   ├── index.html
│       │   │   │   │   └── page2.html
│       │   │   │   ├── cypress-full
│       │   │   │   │   └── index.html
│       │   │   │   ├── error-tracking
│       │   │   │   │   ├── next-ts-app
│       │   │   │   │   │   ├── src
│       │   │   │   │   │   │   └── app
│       │   │   │   │   │   │       ├── error
│       │   │   │   │   │   │       │   ├── layout.tsx
│       │   │   │   │   │   │       │   └── page.tsx
│       │   │   │   │   │   │       ├── layout.tsx
│       │   │   │   │   │   │       ├── page.tsx
│       │   │   │   │   │   │       └── provider.tsx
│       │   │   │   │   │   ├── .gitignore
│       │   │   │   │   │   ├── .npmrc
│       │   │   │   │   │   ├── next.config.ts
│       │   │   │   │   │   ├── package.json
│       │   │   │   │   │   ├── pnpm-lock.yaml
│       │   │   │   │   │   ├── pnpm-workspace.yaml
│       │   │   │   │   │   └── tsconfig.json
│       │   │   │   │   ├── react-ts-esbuild
│       │   │   │   │   │   ├── src
│       │   │   │   │   │   │   ├── app.tsx
│       │   │   │   │   │   │   ├── error-button.tsx
│       │   │   │   │   │   │   ├── main.tsx
│       │   │   │   │   │   │   └── vite-env.d.ts
│       │   │   │   │   │   ├── .gitignore
│       │   │   │   │   │   ├── .npmrc
│       │   │   │   │   │   ├── eslint.config.js
│       │   │   │   │   │   ├── index.html
│       │   │   │   │   │   ├── package.json
│       │   │   │   │   │   ├── pnpm-lock.yaml
│       │   │   │   │   │   ├── pnpm-workspace.yaml
│       │   │   │   │   │   ├── tsconfig.app.json
│       │   │   │   │   │   ├── tsconfig.json
│       │   │   │   │   │   ├── tsconfig.node.json
│       │   │   │   │   │   └── vite.config.ts
│       │   │   │   │   ├── vue-ts-esbuild
│       │   │   │   │   │   ├── src
│       │   │   │   │   │   │   ├── components
│       │   │   │   │   │   │   │   ├── ErrorButton.vue
│       │   │   │   │   │   │   │   └── throw-error.ts
│       │   │   │   │   │   │   ├── App.vue
│       │   │   │   │   │   │   ├── main.ts
│       │   │   │   │   │   │   ├── shims-vue.d.ts
│       │   │   │   │   │   │   └── vite-env.d.ts
│       │   │   │   │   │   ├── .gitignore
│       │   │   │   │   │   ├── .npmrc
│       │   │   │   │   │   ├── index.html
│       │   │   │   │   │   ├── package.json
│       │   │   │   │   │   ├── pnpm-lock.yaml
│       │   │   │   │   │   ├── pnpm-workspace.yaml
│       │   │   │   │   │   ├── tsconfig.app.json
│       │   │   │   │   │   ├── tsconfig.json
│       │   │   │   │   │   ├── tsconfig.node.json
│       │   │   │   │   │   └── vite.config.ts
│       │   │   │   │   └── README.md
│       │   │   │   ├── flags
│       │   │   │   │   ├── .npmrc
│       │   │   │   │   ├── demo.html
│       │   │   │   │   ├── package.json
│       │   │   │   │   ├── pnpm-lock.yaml
│       │   │   │   │   ├── pnpm-workspace.yaml
│       │   │   │   │   └── server.js
│       │   │   │   ├── hydration
│       │   │   │   │   ├── vendor
│       │   │   │   │   │   ├── preact-compat.umd.js
│       │   │   │   │   │   ├── preact-hooks.umd.js
│       │   │   │   │   │   └── preact.umd.js
│       │   │   │   │   └── index.html
│       │   │   │   ├── ie11
│       │   │   │   │   └── index.html
│       │   │   │   ├── nuxtjs
│       │   │   │   │   ├── pages
│       │   │   │   │   │   ├── about.vue
│       │   │   │   │   │   └── index.vue
│       │   │   │   │   ├── plugins
│       │   │   │   │   │   └── posthog.client.js
│       │   │   │   │   ├── public
│       │   │   │   │   │   └── favicon.ico
│       │   │   │   │   ├── .gitignore
│       │   │   │   │   ├── .npmrc
│       │   │   │   │   ├── README.md
│       │   │   │   │   ├── nuxt.config.ts
│       │   │   │   │   ├── package.json
│       │   │   │   │   ├── pnpm-lock.yaml
│       │   │   │   │   ├── pnpm-workspace.yaml
│       │   │   │   │   └── tsconfig.json
│       │   │   │   ├── react-router
│       │   │   │   │   ├── app
│       │   │   │   │   │   ├── components
│       │   │   │   │   │   │   └── Navigation.tsx
│       │   │   │   │   │   ├── routes
│       │   │   │   │   │   │   ├── home.tsx
│       │   │   │   │   │   │   └── surveys.tsx
│       │   │   │   │   │   ├── welcome
│       │   │   │   │   │   │   ├── logo-dark.svg
│       │   │   │   │   │   │   ├── logo-light.svg
│       │   │   │   │   │   │   └── welcome.tsx
│       │   │   │   │   │   ├── app.css
│       │   │   │   │   │   ├── root.tsx
│       │   │   │   │   │   └── routes.ts
│       │   │   │   │   ├── public
│       │   │   │   │   │   └── favicon.ico
│       │   │   │   │   ├── .dockerignore
│       │   │   │   │   ├── .gitignore
│       │   │   │   │   ├── .npmrc
│       │   │   │   │   ├── Dockerfile
│       │   │   │   │   ├── README.md
│       │   │   │   │   ├── package.json
│       │   │   │   │   ├── pnpm-lock.yaml
│       │   │   │   │   ├── pnpm-workspace.yaml
│       │   │   │   │   ├── react-router.config.ts
│       │   │   │   │   ├── tsconfig.json
│       │   │   │   │   └── vite.config.ts
│       │   │   │   ├── redux-todo-list
│       │   │   │   │   ├── pages
│       │   │   │   │   │   ├── _app.tsx
│       │   │   │   │   │   ├── index.tsx
│       │   │   │   │   │   ├── kea.tsx
│       │   │   │   │   │   └── redux.tsx
│       │   │   │   │   ├── src
│       │   │   │   │   │   ├── components
│       │   │   │   │   │   │   ├── kea
│       │   │   │   │   │   │   │   ├── DemoControls.tsx
│       │   │   │   │   │   │   │   ├── TodoFilters.tsx
│       │   │   │   │   │   │   │   ├── TodoInput.tsx
│       │   │   │   │   │   │   │   ├── TodoList.tsx
│       │   │   │   │   │   │   │   └── TodoStats.tsx
│       │   │   │   │   │   │   ├── DemoControls.tsx
│       │   │   │   │   │   │   ├── TodoFilters.tsx
│       │   │   │   │   │   │   ├── TodoInput.tsx
│       │   │   │   │   │   │   ├── TodoList.tsx
│       │   │   │   │   │   │   └── TodoStats.tsx
│       │   │   │   │   │   ├── hooks.ts
│       │   │   │   │   │   ├── kea-store.ts
│       │   │   │   │   │   ├── store.ts
│       │   │   │   │   │   └── todoLogic.ts
│       │   │   │   │   ├── styles
│       │   │   │   │   │   └── globals.css
│       │   │   │   │   ├── .gitignore
│       │   │   │   │   ├── .npmrc
│       │   │   │   │   ├── .prettierrc
│       │   │   │   │   ├── README.md
│       │   │   │   │   ├── next.config.js
│       │   │   │   │   ├── package.json
│       │   │   │   │   ├── pnpm-lock.yaml
│       │   │   │   │   ├── pnpm-workspace.yaml
│       │   │   │   │   └── tsconfig.json
│       │   │   │   ├── segment
│       │   │   │   │   ├── segment.html
│       │   │   │   │   └── server.js
│       │   │   │   ├── session-recordings
│       │   │   │   │   ├── index.html
│       │   │   │   │   └── server.js
│       │   │   │   ├── slim-bundle
│       │   │   │   │   └── index.html
│       │   │   │   ├── snippet
│       │   │   │   │   └── index.html
│       │   │   │   ├── vite-surveys
│       │   │   │   │   ├── public
│       │   │   │   │   │   └── vite.svg
│       │   │   │   │   ├── src
│       │   │   │   │   │   ├── list.tsx
│       │   │   │   │   │   ├── main.tsx
│       │   │   │   │   │   └── vite-env.d.ts
│       │   │   │   │   ├── .gitignore
│       │   │   │   │   ├── .npmrc
│       │   │   │   │   ├── README.md
│       │   │   │   │   ├── index.html
│       │   │   │   │   ├── package.json
│       │   │   │   │   ├── pnpm-lock.yaml
│       │   │   │   │   ├── pnpm-workspace.yaml
│       │   │   │   │   ├── tsconfig.json
│       │   │   │   │   ├── tsconfig.node.json
│       │   │   │   │   └── vite.config.ts
│       │   │   │   ├── vscode-extension
│       │   │   │   │   ├── .vscode
│       │   │   │   │   │   └── launch.json
│       │   │   │   │   ├── src
│       │   │   │   │   │   └── extension.js
│       │   │   │   │   ├── .npmrc
│       │   │   │   │   ├── README.md
│       │   │   │   │   ├── package.json
│       │   │   │   │   └── pnpm-workspace.yaml
│       │   │   │   ├── .pnpmfile.cjs
│       │   │   │   ├── README.md
│       │   │   │   └── sentry.html
│       │   │   ├── react
│       │   │   │   ├── slim
│       │   │   │   │   └── package.json
│       │   │   │   ├── surveys
│       │   │   │   │   └── package.json
│       │   │   │   └── package.json
│       │   │   ├── references
│       │   │   │   ├── posthog-js-references-1.275.3.json
│       │   │   │   ├── posthog-js-references-1.276.0.json
│       │   │   │   ├── posthog-js-references-1.277.0.json
│       │   │   │   ├── posthog-js-references-1.278.0.json
│       │   │   │   ├── posthog-js-references-1.279.0.json
│       │   │   │   ├── posthog-js-references-1.279.1.json
│       │   │   │   ├── posthog-js-references-1.279.2.json
│       │   │   │   ├── posthog-js-references-1.279.3.json
│       │   │   │   ├── posthog-js-references-1.280.0.json
│       │   │   │   ├── posthog-js-references-1.280.1.json
│       │   │   │   ├── posthog-js-references-1.282.0.json
│       │   │   │   ├── posthog-js-references-1.283.0.json
│       │   │   │   ├── posthog-js-references-1.284.0.json
│       │   │   │   ├── posthog-js-references-1.285.0.json
│       │   │   │   ├── posthog-js-references-1.285.1.json
│       │   │   │   ├── posthog-js-references-1.285.2.json
│       │   │   │   ├── posthog-js-references-1.286.0.json
│       │   │   │   ├── posthog-js-references-1.287.0.json
│       │   │   │   ├── posthog-js-references-1.288.0.json
│       │   │   │   ├── posthog-js-references-1.288.1.json
│       │   │   │   ├── posthog-js-references-1.289.0.json
│       │   │   │   ├── posthog-js-references-1.290.0.json
│       │   │   │   ├── posthog-js-references-1.291.0.json
│       │   │   │   ├── posthog-js-references-1.292.0.json
│       │   │   │   ├── posthog-js-references-1.293.0.json
│       │   │   │   ├── posthog-js-references-1.294.0.json
│       │   │   │   ├── posthog-js-references-1.295.0.json
│       │   │   │   ├── posthog-js-references-1.296.0.json
│       │   │   │   ├── posthog-js-references-1.297.0.json
│       │   │   │   ├── posthog-js-references-1.297.2.json
│       │   │   │   ├── posthog-js-references-1.298.0.json
│       │   │   │   ├── posthog-js-references-1.299.0.json
│       │   │   │   ├── posthog-js-references-1.300.0.json
│       │   │   │   ├── posthog-js-references-1.301.0.json
│       │   │   │   ├── posthog-js-references-1.301.1.json
│       │   │   │   ├── posthog-js-references-1.301.2.json
│       │   │   │   ├── posthog-js-references-1.302.0.json
│       │   │   │   ├── posthog-js-references-1.302.1.json
│       │   │   │   ├── posthog-js-references-1.302.2.json
│       │   │   │   ├── posthog-js-references-1.303.0.json
│       │   │   │   ├── posthog-js-references-1.303.1.json
│       │   │   │   ├── posthog-js-references-1.304.0.json
│       │   │   │   ├── posthog-js-references-1.305.0.json
│       │   │   │   ├── posthog-js-references-1.306.0.json
│       │   │   │   ├── posthog-js-references-1.306.1.json
│       │   │   │   ├── posthog-js-references-1.306.2.json
│       │   │   │   ├── posthog-js-references-1.307.0.json
│       │   │   │   ├── posthog-js-references-1.307.1.json
│       │   │   │   ├── posthog-js-references-1.307.2.json
│       │   │   │   ├── posthog-js-references-1.308.0.json
│       │   │   │   ├── posthog-js-references-1.309.0.json
│       │   │   │   ├── posthog-js-references-1.309.1.json
│       │   │   │   ├── posthog-js-references-1.310.0.json
│       │   │   │   ├── posthog-js-references-1.310.1.json
│       │   │   │   ├── posthog-js-references-1.310.2.json
│       │   │   │   ├── posthog-js-references-1.311.0.json
│       │   │   │   ├── posthog-js-references-1.312.0.json
│       │   │   │   ├── posthog-js-references-1.313.0.json
│       │   │   │   ├── posthog-js-references-1.314.0.json
│       │   │   │   ├── posthog-js-references-1.315.0.json
│       │   │   │   ├── posthog-js-references-1.315.1.json
│       │   │   │   ├── posthog-js-references-1.316.0.json
│       │   │   │   ├── posthog-js-references-1.316.1.json
│       │   │   │   ├── posthog-js-references-1.317.0.json
│       │   │   │   ├── posthog-js-references-1.317.1.json
│       │   │   │   ├── posthog-js-references-1.318.0.json
│       │   │   │   ├── posthog-js-references-1.318.1.json
│       │   │   │   ├── posthog-js-references-1.318.2.json
│       │   │   │   ├── posthog-js-references-1.319.0.json
│       │   │   │   ├── posthog-js-references-1.319.1.json
│       │   │   │   ├── posthog-js-references-1.319.2.json
│       │   │   │   ├── posthog-js-references-1.320.0.json
│       │   │   │   ├── posthog-js-references-1.321.0.json
│       │   │   │   ├── posthog-js-references-1.321.1.json
│       │   │   │   ├── posthog-js-references-1.321.2.json
│       │   │   │   ├── posthog-js-references-1.321.3.json
│       │   │   │   ├── posthog-js-references-1.322.0.json
│       │   │   │   ├── posthog-js-references-1.323.0.json
│       │   │   │   ├── posthog-js-references-1.324.0.json
│       │   │   │   ├── posthog-js-references-1.324.1.json
│       │   │   │   ├── posthog-js-references-1.325.0.json
│       │   │   │   ├── posthog-js-references-1.326.0.json
│       │   │   │   ├── posthog-js-references-1.327.0.json
│       │   │   │   ├── posthog-js-references-1.328.0.json
│       │   │   │   ├── posthog-js-references-1.329.0.json
│       │   │   │   ├── posthog-js-references-1.330.0.json
│       │   │   │   ├── posthog-js-references-1.331.0.json
│       │   │   │   ├── posthog-js-references-1.331.1.json
│       │   │   │   ├── posthog-js-references-1.331.2.json
│       │   │   │   ├── posthog-js-references-1.331.3.json
│       │   │   │   ├── posthog-js-references-1.332.0.json
│       │   │   │   ├── posthog-js-references-1.333.0.json
│       │   │   │   ├── posthog-js-references-1.334.0.json
│       │   │   │   ├── posthog-js-references-1.334.1.json
│       │   │   │   ├── posthog-js-references-1.335.0.json
│       │   │   │   ├── posthog-js-references-1.335.1.json
│       │   │   │   ├── posthog-js-references-1.335.2.json
│       │   │   │   ├── posthog-js-references-1.335.3.json
│       │   │   │   ├── posthog-js-references-1.335.4.json
│       │   │   │   ├── posthog-js-references-1.335.5.json
│       │   │   │   ├── posthog-js-references-1.336.0.json
│       │   │   │   ├── posthog-js-references-1.336.1.json
│       │   │   │   ├── posthog-js-references-1.336.2.json
│       │   │   │   ├── posthog-js-references-1.336.3.json
│       │   │   │   ├── posthog-js-references-1.336.4.json
│       │   │   │   ├── posthog-js-references-1.337.0.json
│       │   │   │   ├── posthog-js-references-1.337.1.json
│       │   │   │   ├── posthog-js-references-1.338.0.json
│       │   │   │   ├── posthog-js-references-1.338.1.json
│       │   │   │   ├── posthog-js-references-1.339.0.json
│       │   │   │   ├── posthog-js-references-1.339.1.json
│       │   │   │   ├── posthog-js-references-1.340.0.json
│       │   │   │   ├── posthog-js-references-1.341.0.json
│       │   │   │   ├── posthog-js-references-1.341.1.json
│       │   │   │   ├── posthog-js-references-1.341.2.json
│       │   │   │   ├── posthog-js-references-1.342.0.json
│       │   │   │   ├── posthog-js-references-1.342.1.json
│       │   │   │   ├── posthog-js-references-1.343.0.json
│       │   │   │   ├── posthog-js-references-1.343.1.json
│       │   │   │   ├── posthog-js-references-1.343.2.json
│       │   │   │   ├── posthog-js-references-1.344.0.json
│       │   │   │   ├── posthog-js-references-1.345.0.json
│       │   │   │   ├── posthog-js-references-1.345.1.json
│       │   │   │   ├── posthog-js-references-1.345.2.json
│       │   │   │   ├── posthog-js-references-1.345.3.json
│       │   │   │   ├── posthog-js-references-1.345.4.json
│       │   │   │   ├── posthog-js-references-1.345.5.json
│       │   │   │   ├── posthog-js-references-1.346.0.json
│       │   │   │   ├── posthog-js-references-1.347.0.json
│       │   │   │   ├── posthog-js-references-1.347.1.json
│       │   │   │   ├── posthog-js-references-1.347.2.json
│       │   │   │   ├── posthog-js-references-1.348.0.json
│       │   │   │   ├── posthog-js-references-1.349.0.json
│       │   │   │   ├── posthog-js-references-1.350.0.json
│       │   │   │   ├── posthog-js-references-1.351.0.json
│       │   │   │   ├── posthog-js-references-1.351.1.json
│       │   │   │   ├── posthog-js-references-1.351.2.json
│       │   │   │   ├── posthog-js-references-1.351.3.json
│       │   │   │   ├── posthog-js-references-1.351.4.json
│       │   │   │   ├── posthog-js-references-1.352.0.json
│       │   │   │   ├── posthog-js-references-1.352.1.json
│       │   │   │   ├── posthog-js-references-1.353.0.json
│       │   │   │   ├── posthog-js-references-1.353.1.json
│       │   │   │   ├── posthog-js-references-1.354.0.json
│       │   │   │   ├── posthog-js-references-1.354.1.json
│       │   │   │   ├── posthog-js-references-1.354.2.json
│       │   │   │   ├── posthog-js-references-1.354.3.json
│       │   │   │   ├── posthog-js-references-1.354.4.json
│       │   │   │   ├── posthog-js-references-1.355.0.json
│       │   │   │   ├── posthog-js-references-1.356.0.json
│       │   │   │   ├── posthog-js-references-1.356.1.json
│       │   │   │   ├── posthog-js-references-1.356.2.json
│       │   │   │   ├── posthog-js-references-1.357.0.json
│       │   │   │   ├── posthog-js-references-1.357.1.json
│       │   │   │   ├── posthog-js-references-1.357.2.json
│       │   │   │   ├── posthog-js-references-1.358.0.json
│       │   │   │   ├── posthog-js-references-1.358.1.json
│       │   │   │   ├── posthog-js-references-1.359.0.json
│       │   │   │   ├── posthog-js-references-1.359.1.json
│       │   │   │   ├── posthog-js-references-1.360.0.json
│       │   │   │   ├── posthog-js-references-1.360.1.json
│       │   │   │   ├── posthog-js-references-1.360.2.json
│       │   │   │   ├── posthog-js-references-1.361.0.json
│       │   │   │   ├── posthog-js-references-1.361.1.json
│       │   │   │   ├── posthog-js-references-1.362.0.json
│       │   │   │   ├── posthog-js-references-1.363.0.json
│       │   │   │   ├── posthog-js-references-1.363.1.json
│       │   │   │   ├── posthog-js-references-1.363.2.json
│       │   │   │   ├── posthog-js-references-1.363.3.json
│       │   │   │   ├── posthog-js-references-1.363.4.json
│       │   │   │   ├── posthog-js-references-1.363.5.json
│       │   │   │   ├── posthog-js-references-1.363.6.json
│       │   │   │   ├── posthog-js-references-1.364.0.json
│       │   │   │   ├── posthog-js-references-1.364.1.json
│       │   │   │   ├── posthog-js-references-1.364.2.json
│       │   │   │   ├── posthog-js-references-1.364.3.json
│       │   │   │   ├── posthog-js-references-1.364.4.json
│       │   │   │   ├── posthog-js-references-1.364.5.json
│       │   │   │   ├── posthog-js-references-1.364.6.json
│       │   │   │   ├── posthog-js-references-1.364.7.json
│       │   │   │   ├── posthog-js-references-1.365.0.json
│       │   │   │   ├── posthog-js-references-1.365.1.json
│       │   │   │   ├── posthog-js-references-1.365.2.json
│       │   │   │   ├── posthog-js-references-1.365.3.json
│       │   │   │   ├── posthog-js-references-1.365.4.json
│       │   │   │   ├── posthog-js-references-1.365.5.json
│       │   │   │   ├── posthog-js-references-1.366.0.json
│       │   │   │   ├── posthog-js-references-1.366.1.json
│       │   │   │   ├── posthog-js-references-1.366.2.json
│       │   │   │   ├── posthog-js-references-1.367.0.json
│       │   │   │   ├── posthog-js-references-1.368.0.json
│       │   │   │   ├── posthog-js-references-1.368.1.json
│       │   │   │   ├── posthog-js-references-1.368.2.json
│       │   │   │   ├── posthog-js-references-1.369.0.json
│       │   │   │   ├── posthog-js-references-1.369.1.json
│       │   │   │   ├── posthog-js-references-1.369.2.json
│       │   │   │   ├── posthog-js-references-1.369.3.json
│       │   │   │   ├── posthog-js-references-1.369.4.json
│       │   │   │   ├── posthog-js-references-1.369.5.json
│       │   │   │   ├── posthog-js-references-1.370.0.json
│       │   │   │   ├── posthog-js-references-1.370.1.json
│       │   │   │   ├── posthog-js-references-1.371.0.json
│       │   │   │   ├── posthog-js-references-1.371.1.json
│       │   │   │   ├── posthog-js-references-1.371.2.json
│       │   │   │   ├── posthog-js-references-1.371.3.json
│       │   │   │   ├── posthog-js-references-1.371.4.json
│       │   │   │   ├── posthog-js-references-1.372.0.json
│       │   │   │   ├── posthog-js-references-1.372.1.json
│       │   │   │   ├── posthog-js-references-1.372.10.json
│       │   │   │   ├── posthog-js-references-1.372.2.json
│       │   │   │   ├── posthog-js-references-1.372.3.json
│       │   │   │   ├── posthog-js-references-1.372.4.json
│       │   │   │   ├── posthog-js-references-1.372.5.json
│       │   │   │   ├── posthog-js-references-1.372.6.json
│       │   │   │   ├── posthog-js-references-1.372.7.json
│       │   │   │   ├── posthog-js-references-1.372.8.json
│       │   │   │   ├── posthog-js-references-1.372.9.json
│       │   │   │   ├── posthog-js-references-1.373.0.json
│       │   │   │   ├── posthog-js-references-1.373.1.json
│       │   │   │   ├── posthog-js-references-1.373.2.json
│       │   │   │   ├── posthog-js-references-1.373.3.json
│       │   │   │   ├── posthog-js-references-1.373.4.json
│       │   │   │   ├── posthog-js-references-1.373.5.json
│       │   │   │   ├── posthog-js-references-1.374.0.json
│       │   │   │   ├── posthog-js-references-1.374.1.json
│       │   │   │   ├── posthog-js-references-1.374.2.json
│       │   │   │   ├── posthog-js-references-1.374.3.json
│       │   │   │   ├── posthog-js-references-1.374.4.json
│       │   │   │   ├── posthog-js-references-1.375.0.json
│       │   │   │   ├── posthog-js-references-1.376.0.json
│       │   │   │   └── posthog-js-references-latest.json
│       │   │   ├── rrweb
│       │   │   │   └── package.json
│       │   │   ├── rrweb-plugin-console-record
│       │   │   │   └── package.json
│       │   │   ├── rrweb-types
│       │   │   │   └── package.json
│       │   │   ├── scripts
│       │   │   │   ├── check-mangled-property-consistency.js
│       │   │   │   ├── copy-rrweb-worker-maps.js
│       │   │   │   ├── deprecate-old-versions.mjs
│       │   │   │   ├── generate-docs.js
│       │   │   │   ├── run-testcafe-localhost.mjs
│       │   │   │   └── strip-lib-package-json.js
│       │   │   ├── src
│       │   │   │   ├── __tests__
│       │   │   │   │   ├── customizations
│       │   │   │   │   │   ├── __snapshots__
│       │   │   │   │   │   │   └── getChangedState.test.ts.snap
│       │   │   │   │   │   ├── getChangedState.test.ts
│       │   │   │   │   │   └── setAllPersonProfilePropertiesAsPersonPropertiesForFlags.test.ts
│       │   │   │   │   ├── entrypoints
│       │   │   │   │   │   ├── lazy-loaded-dead-clicks-autocapture.test.ts
│       │   │   │   │   │   ├── logs.test.ts
│       │   │   │   │   │   └── module.test.ts
│       │   │   │   │   ├── extensions
│       │   │   │   │   │   ├── conversations
│       │   │   │   │   │   │   ├── conversations-api.test.ts
│       │   │   │   │   │   │   ├── conversations-identity-manager.test.tsx
│       │   │   │   │   │   │   ├── conversations-identity.test.ts
│       │   │   │   │   │   │   ├── conversations-manager.test.tsx
│       │   │   │   │   │   │   ├── conversations-persistence.test.ts
│       │   │   │   │   │   │   ├── conversations-widget.test.tsx
│       │   │   │   │   │   │   ├── conversations.test.ts
│       │   │   │   │   │   │   ├── rich-content.test.tsx
│       │   │   │   │   │   │   └── utils.test.ts
│       │   │   │   │   │   ├── exception-autocapture
│       │   │   │   │   │   │   ├── error-conversion.test.ts
│       │   │   │   │   │   │   └── exception-observer.test.ts
│       │   │   │   │   │   ├── replay
│       │   │   │   │   │   │   ├── external
│       │   │   │   │   │   │   │   ├── test_data
│       │   │   │   │   │   │   │   │   └── header-cases.ts
│       │   │   │   │   │   │   │   ├── denylist.test.ts
│       │   │   │   │   │   │   │   ├── fetch-wrapper-invariants.test.ts
│       │   │   │   │   │   │   │   ├── network-plugin.test.ts
│       │   │   │   │   │   │   │   └── xhr-wrapper-invariants.test.ts
│       │   │   │   │   │   │   ├── rrweb-plugins
│       │   │   │   │   │   │   │   └── patch.test.ts
│       │   │   │   │   │   │   ├── checkUrlTriggerConditions.test.ts
│       │   │   │   │   │   │   ├── config.test.ts
│       │   │   │   │   │   │   ├── flushed-size-tracker.test.ts
│       │   │   │   │   │   │   ├── lazy-sessionrecording-compression.test.ts
│       │   │   │   │   │   │   ├── lazy-sessionrecording.test.ts
│       │   │   │   │   │   │   ├── mutation-throttler.test.ts
│       │   │   │   │   │   │   ├── sessionRecording-onRemoteConfig.test.ts
│       │   │   │   │   │   │   ├── sessionRecordingStatus.test.ts
│       │   │   │   │   │   │   ├── sessionrecording-utils.test.ts
│       │   │   │   │   │   │   ├── triggerGroups-v1-compat.test.ts
│       │   │   │   │   │   │   └── triggerGroups.test.ts
│       │   │   │   │   │   ├── surveys
│       │   │   │   │   │   │   ├── action-matcher.test.ts
│       │   │   │   │   │   │   ├── feedback-widget.test.tsx
│       │   │   │   │   │   │   ├── question-types.test.tsx
│       │   │   │   │   │   │   └── survey-popup.test.tsx
│       │   │   │   │   │   ├── test_data
│       │   │   │   │   │   │   └── sessionrecording-utils-test-data.ts
│       │   │   │   │   │   ├── dead-clicks-autocapture.test.ts
│       │   │   │   │   │   ├── exception-autocapture.test.ts
│       │   │   │   │   │   ├── history-autocapture.test.ts
│       │   │   │   │   │   ├── logs.test.ts
│       │   │   │   │   │   ├── matcher-utils.test.ts
│       │   │   │   │   │   ├── product-tours-utils.test.ts
│       │   │   │   │   │   ├── rageclick.test.ts
│       │   │   │   │   │   ├── surveys-utils.test.ts
│       │   │   │   │   │   ├── surveys.test.ts
│       │   │   │   │   │   ├── toolbar.test.ts
│       │   │   │   │   │   └── web-vitals.test.ts
│       │   │   │   │   ├── helpers
│       │   │   │   │   │   ├── mock-logger.ts
│       │   │   │   │   │   ├── posthog-instance.ts
│       │   │   │   │   │   ├── script-utils.ts
│       │   │   │   │   │   └── truth.ts
│       │   │   │   │   ├── utils
│       │   │   │   │   │   ├── before-send-utils.test.ts
│       │   │   │   │   │   ├── device.test.json
│       │   │   │   │   │   ├── elements-chain-utils.test.ts
│       │   │   │   │   │   ├── event-utils.test.ts
│       │   │   │   │   │   ├── external-scripts-loader.test.ts
│       │   │   │   │   │   ├── os-test.json
│       │   │   │   │   │   ├── request-router.test.ts
│       │   │   │   │   │   ├── survey-event-receiver.test.ts
│       │   │   │   │   │   ├── survey-translations.test.ts
│       │   │   │   │   │   ├── survey-url-prefill.test.ts
│       │   │   │   │   │   └── user-agent-utils.test.ts
│       │   │   │   │   ├── ai.test.ts
│       │   │   │   │   ├── autocapture-utils.test.ts
│       │   │   │   │   ├── autocapture.test.ts
│       │   │   │   │   ├── bot-detection.test.ts
│       │   │   │   │   ├── config.test.ts
│       │   │   │   │   ├── consent.test.ts
│       │   │   │   │   ├── cookieless.test.ts
│       │   │   │   │   ├── deferred-init-extensions.test.ts
│       │   │   │   │   ├── evaluation-tags.test.ts
│       │   │   │   │   ├── extension-classes.test.ts
│       │   │   │   │   ├── featureflags.test.ts
│       │   │   │   │   ├── group-before-identify-bug.test.ts
│       │   │   │   │   ├── heatmaps.test.ts
│       │   │   │   │   ├── identify.test.ts
│       │   │   │   │   ├── loader.test.ts
│       │   │   │   │   ├── optimised-very-large-performance-data.json
│       │   │   │   │   ├── page-view.test.ts
│       │   │   │   │   ├── persistence-key-policy.test.ts
│       │   │   │   │   ├── personProcessing.test.ts
│       │   │   │   │   ├── posthog-core-also.test.ts
│       │   │   │   │   ├── posthog-core.beforeSend.test.ts
│       │   │   │   │   ├── posthog-core.identify.test.ts
│       │   │   │   │   ├── posthog-core.loaded.test.ts
│       │   │   │   │   ├── posthog-core.reset.test.ts
│       │   │   │   │   ├── posthog-core.set_config.test.ts
│       │   │   │   │   ├── posthog-core.test.ts
│       │   │   │   │   ├── posthog-exceptions.test.ts
│       │   │   │   │   ├── posthog-logs.test.ts
│       │   │   │   │   ├── posthog-persistence.test.ts
│       │   │   │   │   ├── posthog-product-tours.test.ts
│       │   │   │   │   ├── posthog-surveys.test.ts
│       │   │   │   │   ├── rate-limiter.test.ts
│       │   │   │   │   ├── remote-config.test.ts
│       │   │   │   │   ├── request-queue.test.ts
│       │   │   │   │   ├── request-utils.test.ts
│       │   │   │   │   ├── request.test.ts
│       │   │   │   │   ├── retry-queue.test.ts
│       │   │   │   │   ├── segment.test.ts
│       │   │   │   │   ├── session-props.test.ts
│       │   │   │   │   ├── sessionid.property.test.ts
│       │   │   │   │   ├── sessionid.test.ts
│       │   │   │   │   ├── setup.js
│       │   │   │   │   ├── site-apps.test.ts
│       │   │   │   │   ├── storage.test.ts
│       │   │   │   │   ├── surveys.test.ts
│       │   │   │   │   ├── test-uuid.test.ts
│       │   │   │   │   ├── tracing-headers.test.ts
│       │   │   │   │   ├── tsconfig.json
│       │   │   │   │   ├── utils.test.ts
│       │   │   │   │   ├── very-large-performance-data.json
│       │   │   │   │   └── web-experiments.test.ts
│       │   │   │   ├── customizations
│       │   │   │   │   ├── before-send.ts
│       │   │   │   │   ├── index.ts
│       │   │   │   │   ├── posthogReduxLogger.ts
│       │   │   │   │   └── setAllPersonProfilePropertiesAsPersonPropertiesForFlags.ts
│       │   │   │   ├── entrypoints
│       │   │   │   │   ├── all-external-dependencies.ts
│       │   │   │   │   ├── array.full.es5.ts
│       │   │   │   │   ├── array.full.no-external.ts
│       │   │   │   │   ├── array.full.ts
│       │   │   │   │   ├── array.no-external.ts
│       │   │   │   │   ├── array.ts
│       │   │   │   │   ├── conversations.ts
│       │   │   │   │   ├── crisp-chat-integration.ts
│       │   │   │   │   ├── customizations.full.ts
│       │   │   │   │   ├── dead-clicks-autocapture.ts
│       │   │   │   │   ├── default-extensions.ts
│       │   │   │   │   ├── element-inference.es.ts
│       │   │   │   │   ├── exception-autocapture.ts
│       │   │   │   │   ├── extension-bundles.es.ts
│       │   │   │   │   ├── external-scripts-loader.ts
│       │   │   │   │   ├── intercom-integration.ts
│       │   │   │   │   ├── lazy-recorder.ts
│       │   │   │   │   ├── logs.ts
│       │   │   │   │   ├── main.cjs.ts
│       │   │   │   │   ├── module.es.ts
│       │   │   │   │   ├── module.full.es.ts
│       │   │   │   │   ├── module.full.no-external.es.ts
│       │   │   │   │   ├── module.no-external.es.ts
│       │   │   │   │   ├── module.slim.es.ts
│       │   │   │   │   ├── module.slim.no-external.es.ts
│       │   │   │   │   ├── posthog-monolith.ts
│       │   │   │   │   ├── posthog-recorder.ts
│       │   │   │   │   ├── product-tours-preview.es.ts
│       │   │   │   │   ├── product-tours.ts
│       │   │   │   │   ├── recorder-v2.ts
│       │   │   │   │   ├── recorder.ts
│       │   │   │   │   ├── rrweb-plugin-console-record.es.ts
│       │   │   │   │   ├── rrweb-types.es.ts
│       │   │   │   │   ├── rrweb.es.ts
│       │   │   │   │   ├── surveys-preview.es.ts
│       │   │   │   │   ├── surveys.ts
│       │   │   │   │   ├── tracing-headers.ts
│       │   │   │   │   ├── web-vitals-with-attribution.ts
│       │   │   │   │   └── web-vitals.ts
│       │   │   │   ├── extensions
│       │   │   │   │   ├── conversations
│       │   │   │   │   │   ├── external
│       │   │   │   │   │   │   ├── components
│       │   │   │   │   │   │   │   ├── CloseChatButton.tsx
│       │   │   │   │   │   │   │   ├── ConversationsWidget.tsx
│       │   │   │   │   │   │   │   ├── IdentificationFormView.tsx
│       │   │   │   │   │   │   │   ├── MessagesView.tsx
│       │   │   │   │   │   │   │   ├── NewConversationButton.tsx
│       │   │   │   │   │   │   │   ├── OpenChatButton.tsx
│       │   │   │   │   │   │   │   ├── RestoreRequestView.tsx
│       │   │   │   │   │   │   │   ├── RichContent.tsx
│       │   │   │   │   │   │   │   ├── SendMessageButton.tsx
│       │   │   │   │   │   │   │   ├── TicketListItem.tsx
│       │   │   │   │   │   │   │   ├── TicketListView.tsx
│       │   │   │   │   │   │   │   ├── styles.ts
│       │   │   │   │   │   │   │   └── utils.ts
│       │   │   │   │   │   │   ├── README.md
│       │   │   │   │   │   │   ├── index.tsx
│       │   │   │   │   │   │   ├── persistence.ts
│       │   │   │   │   │   │   └── url-utils.ts
│       │   │   │   │   │   └── posthog-conversations.ts
│       │   │   │   │   ├── exception-autocapture
│       │   │   │   │   │   └── index.ts
│       │   │   │   │   ├── product-tours
│       │   │   │   │   │   ├── components
│       │   │   │   │   │   │   ├── ProductTourBanner.tsx
│       │   │   │   │   │   │   ├── ProductTourSurveyStepInner.tsx
│       │   │   │   │   │   │   ├── ProductTourTooltip.tsx
│       │   │   │   │   │   │   └── ProductTourTooltipInner.tsx
│       │   │   │   │   │   ├── constants.ts
│       │   │   │   │   │   ├── element-inference.ts
│       │   │   │   │   │   ├── index.ts
│       │   │   │   │   │   ├── preview.tsx
│       │   │   │   │   │   ├── product-tour.css
│       │   │   │   │   │   ├── product-tours-utils.ts
│       │   │   │   │   │   └── product-tours.tsx
│       │   │   │   │   ├── replay
│       │   │   │   │   │   ├── external
│       │   │   │   │   │   │   ├── README.md
│       │   │   │   │   │   │   ├── config.ts
│       │   │   │   │   │   │   ├── denylist.ts
│       │   │   │   │   │   │   ├── flushed-size-tracker.ts
│       │   │   │   │   │   │   ├── lazy-loaded-session-recorder.ts
│       │   │   │   │   │   │   ├── mutation-throttler.ts
│       │   │   │   │   │   │   ├── network-plugin.ts
│       │   │   │   │   │   │   ├── recording-strategies.ts
│       │   │   │   │   │   │   ├── sessionrecording-utils.ts
│       │   │   │   │   │   │   └── triggerMatching.ts
│       │   │   │   │   │   ├── rrweb-plugins
│       │   │   │   │   │   │   └── patch.ts
│       │   │   │   │   │   ├── types
│       │   │   │   │   │   │   ├── rrweb-types.ts
│       │   │   │   │   │   │   └── rrweb.ts
│       │   │   │   │   │   └── session-recording.ts
│       │   │   │   │   ├── surveys
│       │   │   │   │   │   ├── components
│       │   │   │   │   │   │   ├── BottomSection.tsx
│       │   │   │   │   │   │   ├── ConfirmationMessage.tsx
│       │   │   │   │   │   │   ├── PostHogLogo.tsx
│       │   │   │   │   │   │   ├── QuestionHeader.tsx
│       │   │   │   │   │   │   └── QuestionTypes.tsx
│       │   │   │   │   │   ├── action-matcher.ts
│       │   │   │   │   │   ├── icons.tsx
│       │   │   │   │   │   ├── survey.css
│       │   │   │   │   │   └── surveys-extension-utils.tsx
│       │   │   │   │   ├── utils
│       │   │   │   │   │   ├── matcher-utils.ts
│       │   │   │   │   │   └── stylesheet-loader.ts
│       │   │   │   │   ├── web-vitals
│       │   │   │   │   │   └── index.ts
│       │   │   │   │   ├── dead-clicks-autocapture.ts
│       │   │   │   │   ├── extension-bundles.ts
│       │   │   │   │   ├── external-integration.ts
│       │   │   │   │   ├── history-autocapture.ts
│       │   │   │   │   ├── rageclick.ts
│       │   │   │   │   ├── sampling.ts
│       │   │   │   │   ├── segment-integration.ts
│       │   │   │   │   ├── sentry-integration.ts
│       │   │   │   │   ├── surveys.tsx
│       │   │   │   │   ├── toolbar.ts
│       │   │   │   │   ├── tracing-headers.ts
│       │   │   │   │   └── types.ts
│       │   │   │   ├── utils
│       │   │   │   │   ├── blocked-uas.ts
│       │   │   │   │   ├── element-utils.ts
│       │   │   │   │   ├── elements-chain-utils.ts
│       │   │   │   │   ├── encode-utils.ts
│       │   │   │   │   ├── event-receiver.ts
│       │   │   │   │   ├── event-utils.ts
│       │   │   │   │   ├── globals.ts
│       │   │   │   │   ├── index.ts
│       │   │   │   │   ├── logger.ts
│       │   │   │   │   ├── product-tour-event-receiver.ts
│       │   │   │   │   ├── product-tour-utils.ts
│       │   │   │   │   ├── property-utils.ts
│       │   │   │   │   ├── prototype-utils.ts
│       │   │   │   │   ├── regex-utils.ts
│       │   │   │   │   ├── request-router.ts
│       │   │   │   │   ├── request-utils.ts
│       │   │   │   │   ├── simple-event-emitter.ts
│       │   │   │   │   ├── survey-branching.ts
│       │   │   │   │   ├── survey-event-receiver.ts
│       │   │   │   │   ├── survey-translations.ts
│       │   │   │   │   ├── survey-url-prefill.ts
│       │   │   │   │   ├── survey-utils.ts
│       │   │   │   │   └── type-utils.ts
│       │   │   │   ├── autocapture-utils.ts
│       │   │   │   ├── autocapture.ts
│       │   │   │   ├── config.ts
│       │   │   │   ├── consent.ts
│       │   │   │   ├── constants.ts
│       │   │   │   ├── declaration.d.ts
│       │   │   │   ├── heatmaps.ts
│       │   │   │   ├── page-view.ts
│       │   │   │   ├── persistence-key-policy.ts
│       │   │   │   ├── persistence-key-transforms.ts
│       │   │   │   ├── posthog-conversations-types.ts
│       │   │   │   ├── posthog-core.ts
│       │   │   │   ├── posthog-exceptions.ts
│       │   │   │   ├── posthog-featureflags.ts
│       │   │   │   ├── posthog-logs.ts
│       │   │   │   ├── posthog-persistence.ts
│       │   │   │   ├── posthog-product-tours-types.ts
│       │   │   │   ├── posthog-product-tours.ts
│       │   │   │   ├── posthog-surveys-types.ts
│       │   │   │   ├── posthog-surveys.ts
│       │   │   │   ├── rate-limiter.ts
│       │   │   │   ├── remote-config.ts
│       │   │   │   ├── request-queue.ts
│       │   │   │   ├── request.ts
│       │   │   │   ├── retry-queue.ts
│       │   │   │   ├── scroll-manager.ts
│       │   │   │   ├── session-props.ts
│       │   │   │   ├── sessionid.ts
│       │   │   │   ├── site-apps.ts
│       │   │   │   ├── storage.ts
│       │   │   │   ├── types.ts
│       │   │   │   ├── uuidv7.ts
│       │   │   │   ├── web-experiments-types.ts
│       │   │   │   ├── web-experiments.ts
│       │   │   │   └── web-types.d.ts
│       │   │   ├── testcafe
│       │   │   │   ├── check-testcafe-results.js
│       │   │   │   ├── e2e.spec.js
│       │   │   │   ├── helpers.js
│       │   │   │   └── tsconfig.json
│       │   │   ├── README.md
│       │   │   ├── rollup.config.mjs
│       │   │   ├── terser-mangled-names.json
│       │   │   ├── tsconfig.json
│       │   │   └── tsdoc.json
│       │   ├── core
│       │   │   ├── src
│       │   │   │   ├── __tests__
│       │   │   │   │   ├── cookie.spec.ts
│       │   │   │   │   ├── featureFlagUtils.spec.ts
│       │   │   │   │   ├── gzip.spec.ts
│       │   │   │   │   ├── posthog.ai.spec.ts
│       │   │   │   │   ├── posthog.capture.spec.ts
│       │   │   │   │   ├── posthog.core.spec.ts
│       │   │   │   │   ├── posthog.debug.spec.ts
│       │   │   │   │   ├── posthog.enqueue.spec.ts
│       │   │   │   │   ├── posthog.featureflags.spec.ts
│       │   │   │   │   ├── posthog.featureflags.v1.spec.ts
│       │   │   │   │   ├── posthog.flush.spec.ts
│       │   │   │   │   ├── posthog.gdpr.spec.ts
│       │   │   │   │   ├── posthog.groups.spec.ts
│       │   │   │   │   ├── posthog.identify.spec.ts
│       │   │   │   │   ├── posthog.init.spec.ts
│       │   │   │   │   ├── posthog.listeners.spec.ts
│       │   │   │   │   ├── posthog.person-profiles.spec.ts
│       │   │   │   │   ├── posthog.register.spec.ts
│       │   │   │   │   ├── posthog.remoteconfig.spec.ts
│       │   │   │   │   ├── posthog.reset.spec.ts
│       │   │   │   │   ├── posthog.sessions.spec.ts
│       │   │   │   │   ├── posthog.setProperties.spec.ts
│       │   │   │   │   ├── posthog.shutdown.spec.ts
│       │   │   │   │   ├── tracing-headers.spec.ts
│       │   │   │   │   └── utils.spec.ts
│       │   │   │   ├── error-tracking
│       │   │   │   │   ├── coercers
│       │   │   │   │   │   ├── dom-exception-coercer.ts
│       │   │   │   │   │   ├── error-coercer.ts
│       │   │   │   │   │   ├── error-event-coercer.ts
│       │   │   │   │   │   ├── event-coercer.ts
│       │   │   │   │   │   ├── index.ts
│       │   │   │   │   │   ├── object-coercer.ts
│       │   │   │   │   │   ├── primitive-coercer.ts
│       │   │   │   │   │   ├── promise-rejection-event.spec.ts
│       │   │   │   │   │   ├── promise-rejection-event.ts
│       │   │   │   │   │   ├── string-coercer.spec.ts
│       │   │   │   │   │   ├── string-coercer.ts
│       │   │   │   │   │   └── utils.ts
│       │   │   │   │   ├── parsers
│       │   │   │   │   │   ├── base.ts
│       │   │   │   │   │   ├── chrome.ts
│       │   │   │   │   │   ├── gecko.ts
│       │   │   │   │   │   ├── index.ts
│       │   │   │   │   │   ├── node.ts
│       │   │   │   │   │   ├── opera.ts
│       │   │   │   │   │   ├── safari.ts
│       │   │   │   │   │   └── winjs.ts
│       │   │   │   │   ├── chunk-ids.ts
│       │   │   │   │   ├── error-properties-builder.coerce.spec.ts
│       │   │   │   │   ├── error-properties-builder.parse.spec.ts
│       │   │   │   │   ├── error-properties-builder.ts
│       │   │   │   │   ├── exception-steps.spec.ts
│       │   │   │   │   ├── exception-steps.ts
│       │   │   │   │   ├── index.ts
│       │   │   │   │   ├── types.ts
│       │   │   │   │   └── utils.ts
│       │   │   │   ├── surveys
│       │   │   │   │   ├── events.spec.ts
│       │   │   │   │   ├── events.ts
│       │   │   │   │   ├── index.ts
│       │   │   │   │   ├── translations.spec.ts
│       │   │   │   │   ├── translations.ts
│       │   │   │   │   ├── validation.spec.ts
│       │   │   │   │   └── validation.ts
│       │   │   │   ├── testing
│       │   │   │   │   ├── PostHogCoreTestClient.ts
│       │   │   │   │   ├── index.ts
│       │   │   │   │   └── test-utils.ts
│       │   │   │   ├── utils
│       │   │   │   │   ├── bot-detection.ts
│       │   │   │   │   ├── bucketed-rate-limiter.spec.ts
│       │   │   │   │   ├── bucketed-rate-limiter.ts
│       │   │   │   │   ├── index.ts
│       │   │   │   │   ├── logger.ts
│       │   │   │   │   ├── number-utils.spec.ts
│       │   │   │   │   ├── number-utils.ts
│       │   │   │   │   ├── promise-queue.spec.ts
│       │   │   │   │   ├── promise-queue.ts
│       │   │   │   │   ├── string-utils.spec.ts
│       │   │   │   │   ├── string-utils.ts
│       │   │   │   │   ├── type-utils.spec.ts
│       │   │   │   │   ├── type-utils.ts
│       │   │   │   │   └── user-agent-utils.ts
│       │   │   │   ├── vendor
│       │   │   │   │   └── uuidv7.ts
│       │   │   │   ├── cookie.ts
│       │   │   │   ├── eventemitter.ts
│       │   │   │   ├── featureFlagUtils.ts
│       │   │   │   ├── gzip.ts
│       │   │   │   ├── index.ts
│       │   │   │   ├── posthog-core-stateless.ts
│       │   │   │   ├── posthog-core.ts
│       │   │   │   ├── tracing-headers.ts
│       │   │   │   └── types.ts
│       │   │   ├── .eslintrc.cjs
│       │   │   ├── .gitignore
│       │   │   ├── .prettierrc
│       │   │   ├── CHANGELOG.md
│       │   │   ├── babel.config.mjs
│       │   │   ├── jest.config.mjs
│       │   │   ├── package.json
│       │   │   ├── rslib.config.ts
│       │   │   ├── tsconfig.build.json
│       │   │   └── tsconfig.json
│       │   ├── node
│       │   │   ├── examples
│       │   │   │   └── etag-polling-test.mjs
│       │   │   ├── references
│       │   │   │   ├── posthog-node-references-5.10.0.json
│       │   │   │   ├── posthog-node-references-5.10.1.json
│       │   │   │   ├── posthog-node-references-5.10.2.json
│       │   │   │   ├── posthog-node-references-5.12.0.json
│       │   │   │   ├── posthog-node-references-5.15.0.json
│       │   │   │   ├── posthog-node-references-5.16.0.json
│       │   │   │   ├── posthog-node-references-5.17.0.json
│       │   │   │   ├── posthog-node-references-5.17.1.json
│       │   │   │   ├── posthog-node-references-5.17.2.json
│       │   │   │   ├── posthog-node-references-5.17.3.json
│       │   │   │   ├── posthog-node-references-5.17.4.json
│       │   │   │   ├── posthog-node-references-5.18.0.json
│       │   │   │   ├── posthog-node-references-5.18.1.json
│       │   │   │   ├── posthog-node-references-5.19.0.json
│       │   │   │   ├── posthog-node-references-5.20.0.json
│       │   │   │   ├── posthog-node-references-5.21.0.json
│       │   │   │   ├── posthog-node-references-5.21.1.json
│       │   │   │   ├── posthog-node-references-5.21.2.json
│       │   │   │   ├── posthog-node-references-5.22.0.json
│       │   │   │   ├── posthog-node-references-5.23.0.json
│       │   │   │   ├── posthog-node-references-5.24.0.json
│       │   │   │   ├── posthog-node-references-5.24.1.json
│       │   │   │   ├── posthog-node-references-5.24.10.json
│       │   │   │   ├── posthog-node-references-5.24.11.json
│       │   │   │   ├── posthog-node-references-5.24.12.json
│       │   │   │   ├── posthog-node-references-5.24.13.json
│       │   │   │   ├── posthog-node-references-5.24.14.json
│       │   │   │   ├── posthog-node-references-5.24.15.json
│       │   │   │   ├── posthog-node-references-5.24.16.json
│       │   │   │   ├── posthog-node-references-5.24.17.json
│       │   │   │   ├── posthog-node-references-5.24.2.json
│       │   │   │   ├── posthog-node-references-5.24.3.json
│       │   │   │   ├── posthog-node-references-5.24.4.json
│       │   │   │   ├── posthog-node-references-5.24.5.json
│       │   │   │   ├── posthog-node-references-5.24.6.json
│       │   │   │   ├── posthog-node-references-5.24.7.json
│       │   │   │   ├── posthog-node-references-5.24.8.json
│       │   │   │   ├── posthog-node-references-5.24.9.json
│       │   │   │   ├── posthog-node-references-5.25.0.json
│       │   │   │   ├── posthog-node-references-5.26.0.json
│       │   │   │   ├── posthog-node-references-5.26.1.json
│       │   │   │   ├── posthog-node-references-5.26.2.json
│       │   │   │   ├── posthog-node-references-5.27.0.json
│       │   │   │   ├── posthog-node-references-5.27.1.json
│       │   │   │   ├── posthog-node-references-5.28.0.json
│       │   │   │   ├── posthog-node-references-5.28.1.json
│       │   │   │   ├── posthog-node-references-5.28.10.json
│       │   │   │   ├── posthog-node-references-5.28.11.json
│       │   │   │   ├── posthog-node-references-5.28.2.json
│       │   │   │   ├── posthog-node-references-5.28.3.json
│       │   │   │   ├── posthog-node-references-5.28.4.json
│       │   │   │   ├── posthog-node-references-5.28.5.json
│       │   │   │   ├── posthog-node-references-5.28.6.json
│       │   │   │   ├── posthog-node-references-5.28.7.json
│       │   │   │   ├── posthog-node-references-5.28.8.json
│       │   │   │   ├── posthog-node-references-5.28.9.json
│       │   │   │   ├── posthog-node-references-5.29.0.json
│       │   │   │   ├── posthog-node-references-5.29.1.json
│       │   │   │   ├── posthog-node-references-5.29.2.json
│       │   │   │   ├── posthog-node-references-5.29.3.json
│       │   │   │   ├── posthog-node-references-5.29.4.json
│       │   │   │   ├── posthog-node-references-5.29.5.json
│       │   │   │   ├── posthog-node-references-5.29.6.json
│       │   │   │   ├── posthog-node-references-5.29.7.json
│       │   │   │   ├── posthog-node-references-5.30.0.json
│       │   │   │   ├── posthog-node-references-5.30.1.json
│       │   │   │   ├── posthog-node-references-5.30.2.json
│       │   │   │   ├── posthog-node-references-5.30.3.json
│       │   │   │   ├── posthog-node-references-5.30.4.json
│       │   │   │   ├── posthog-node-references-5.30.5.json
│       │   │   │   ├── posthog-node-references-5.30.6.json
│       │   │   │   ├── posthog-node-references-5.30.7.json
│       │   │   │   ├── posthog-node-references-5.30.8.json
│       │   │   │   ├── posthog-node-references-5.31.0.json
│       │   │   │   ├── posthog-node-references-5.32.0.json
│       │   │   │   ├── posthog-node-references-5.32.1.json
│       │   │   │   ├── posthog-node-references-5.33.0.json
│       │   │   │   ├── posthog-node-references-5.33.1.json
│       │   │   │   ├── posthog-node-references-5.33.2.json
│       │   │   │   ├── posthog-node-references-5.33.3.json
│       │   │   │   ├── posthog-node-references-5.33.4.json
│       │   │   │   ├── posthog-node-references-5.33.5.json
│       │   │   │   ├── posthog-node-references-5.33.6.json
│       │   │   │   ├── posthog-node-references-5.33.7.json
│       │   │   │   ├── posthog-node-references-5.34.0.json
│       │   │   │   ├── posthog-node-references-5.34.1.json
│       │   │   │   ├── posthog-node-references-5.34.10.json
│       │   │   │   ├── posthog-node-references-5.34.2.json
│       │   │   │   ├── posthog-node-references-5.34.3.json
│       │   │   │   ├── posthog-node-references-5.34.4.json
│       │   │   │   ├── posthog-node-references-5.34.5.json
│       │   │   │   ├── posthog-node-references-5.34.6.json
│       │   │   │   ├── posthog-node-references-5.34.7.json
│       │   │   │   ├── posthog-node-references-5.34.8.json
│       │   │   │   ├── posthog-node-references-5.34.9.json
│       │   │   │   ├── posthog-node-references-5.35.0.json
│       │   │   │   ├── posthog-node-references-5.35.1.json
│       │   │   │   ├── posthog-node-references-5.9.1.json
│       │   │   │   └── posthog-node-references-latest.json
│       │   │   ├── scripts
│       │   │   │   └── generate-docs.mjs
│       │   │   ├── src
│       │   │   │   ├── __tests__
│       │   │   │   │   ├── extensions
│       │   │   │   │   │   ├── error-conversion.spec.ts
│       │   │   │   │   │   ├── exception-autocapture.spec.ts
│       │   │   │   │   │   ├── exception-autocapture.worker.mjs
│       │   │   │   │   │   ├── express.spec.ts
│       │   │   │   │   │   ├── nestjs.spec.ts
│       │   │   │   │   │   ├── relative-path.spec.ts
│       │   │   │   │   │   ├── sentry-integration.spec.ts
│       │   │   │   │   │   └── tracing-headers.spec.ts
│       │   │   │   │   ├── utils
│       │   │   │   │   │   └── index.ts
│       │   │   │   │   ├── bot-detection.spec.ts
│       │   │   │   │   ├── cache.spec.ts
│       │   │   │   │   ├── context.spec.ts
│       │   │   │   │   ├── crypto.spec.ts
│       │   │   │   │   ├── evaluate-flags.spec.ts
│       │   │   │   │   ├── experimental.spec.ts
│       │   │   │   │   ├── feature-flags.dependencies.spec.ts
│       │   │   │   │   ├── feature-flags.flags.spec.ts
│       │   │   │   │   ├── feature-flags.overrides.spec.ts
│       │   │   │   │   ├── feature-flags.spec.ts
│       │   │   │   │   ├── posthog-node.spec.ts
│       │   │   │   │   └── waituntil-flush.spec.ts
│       │   │   │   ├── entrypoints
│       │   │   │   │   ├── index.edge.ts
│       │   │   │   │   ├── index.node.ts
│       │   │   │   │   └── nestjs.ts
│       │   │   │   ├── extensions
│       │   │   │   │   ├── context
│       │   │   │   │   │   ├── context.ts
│       │   │   │   │   │   └── types.ts
│       │   │   │   │   ├── error-tracking
│       │   │   │   │   │   ├── modifiers
│       │   │   │   │   │   │   ├── context-lines.node.ts
│       │   │   │   │   │   │   ├── module.node.ts
│       │   │   │   │   │   │   └── relative-path.node.ts
│       │   │   │   │   │   ├── autocapture.ts
│       │   │   │   │   │   └── index.ts
│       │   │   │   │   ├── feature-flags
│       │   │   │   │   │   ├── cache.ts
│       │   │   │   │   │   ├── crypto.ts
│       │   │   │   │   │   └── feature-flags.ts
│       │   │   │   │   ├── express.ts
│       │   │   │   │   ├── nestjs.ts
│       │   │   │   │   ├── sentry-integration.ts
│       │   │   │   │   └── tracing-headers.ts
│       │   │   │   ├── client.ts
│       │   │   │   ├── experimental.ts
│       │   │   │   ├── exports.ts
│       │   │   │   ├── feature-flag-evaluations.ts
│       │   │   │   ├── storage-memory.ts
│       │   │   │   └── types.ts
│       │   │   ├── .gitignore
│       │   │   ├── .prettierrc
│       │   │   ├── CHANGELOG.md
│       │   │   ├── README.md
│       │   │   ├── api-extractor.jsonc
│       │   │   ├── babel.config.mjs
│       │   │   ├── example.mjs
│       │   │   ├── jest.config.mjs
│       │   │   ├── package.json
│       │   │   ├── rslib.config.ts
│       │   │   ├── tsconfig.build.json
│       │   │   ├── tsconfig.json
│       │   │   └── tsdoc.json
│       │   ├── rrweb
│       │   │   ├── record
│       │   │   │   ├── src
│       │   │   │   │   └── index.ts
│       │   │   │   ├── test
│       │   │   │   │   └── record.test.ts
│       │   │   │   ├── .gitignore
│       │   │   │   ├── CHANGELOG.md
│       │   │   │   ├── README.md
│       │   │   │   ├── package.json
│       │   │   │   ├── tsconfig.json
│       │   │   │   ├── vite.config.ts
│       │   │   │   └── vitest.config.ts
│       │   │   ├── replay
│       │   │   │   ├── src
│       │   │   │   │   └── index.ts
│       │   │   │   ├── test
│       │   │   │   │   └── replay.test.ts
│       │   │   │   ├── .gitignore
│       │   │   │   ├── CHANGELOG.md
│       │   │   │   ├── README.md
│       │   │   │   ├── package.json
│       │   │   │   ├── tsconfig.json
│       │   │   │   ├── vite.config.ts
│       │   │   │   └── vitest.config.ts
│       │   │   ├── rrdom
│       │   │   │   ├── src
│       │   │   │   │   ├── diff.ts
│       │   │   │   │   ├── document.ts
│       │   │   │   │   ├── index.ts
│       │   │   │   │   └── style.ts
│       │   │   │   ├── test
│       │   │   │   │   ├── __snapshots__
│       │   │   │   │   │   └── virtual-dom.test.ts.snap
│       │   │   │   │   ├── diff
│       │   │   │   │   │   └── dialog.test.ts
│       │   │   │   │   ├── html
│       │   │   │   │   │   ├── iframe.html
│       │   │   │   │   │   ├── main.html
│       │   │   │   │   │   └── shadow-dom.html
│       │   │   │   │   ├── diff.test.ts
│       │   │   │   │   ├── document.test.ts
│       │   │   │   │   └── virtual-dom.test.ts
│       │   │   │   ├── .gitignore
│       │   │   │   ├── CHANGELOG.md
│       │   │   │   ├── README.md
│       │   │   │   ├── jest.config.js
│       │   │   │   ├── package.json
│       │   │   │   ├── tsconfig.json
│       │   │   │   ├── vite.config.js
│       │   │   │   └── vitest.config.ts
│       │   │   ├── rrdom-nodejs
│       │   │   │   ├── src
│       │   │   │   │   ├── document-nodejs.ts
│       │   │   │   │   ├── index.ts
│       │   │   │   │   └── polyfill.ts
│       │   │   │   ├── test
│       │   │   │   │   ├── document-nodejs.test.ts
│       │   │   │   │   └── polyfill.test.ts
│       │   │   │   ├── .gitignore
│       │   │   │   ├── CHANGELOG.md
│       │   │   │   ├── README.md
│       │   │   │   ├── package.json
│       │   │   │   ├── tsconfig.json
│       │   │   │   ├── vite.config.js
│       │   │   │   └── vitest.config.ts
│       │   │   ├── rrweb
│       │   │   │   ├── rrweb-record
│       │   │   │   │   └── package.json
│       │   │   │   ├── rrweb-replay
│       │   │   │   │   └── package.json
│       │   │   │   ├── scripts
│       │   │   │   │   ├── repl.js
│       │   │   │   │   ├── stream.js
│       │   │   │   │   └── utils.js
│       │   │   │   ├── src
│       │   │   │   │   ├── entries
│       │   │   │   │   │   ├── record.ts
│       │   │   │   │   │   └── replay.ts
│       │   │   │   │   ├── record
│       │   │   │   │   │   ├── observers
│       │   │   │   │   │   │   └── canvas
│       │   │   │   │   │   │       ├── 2d.ts
│       │   │   │   │   │   │       ├── canvas-manager.ts
│       │   │   │   │   │   │       ├── canvas.ts
│       │   │   │   │   │   │       ├── serialize-args.ts
│       │   │   │   │   │   │       └── webgl.ts
│       │   │   │   │   │   ├── workers
│       │   │   │   │   │   │   ├── image-bitmap-data-url-worker.ts
│       │   │   │   │   │   │   └── tsconfig.json
│       │   │   │   │   │   ├── cross-origin-iframe-mirror.ts
│       │   │   │   │   │   ├── error-handler.ts
│       │   │   │   │   │   ├── iframe-manager.ts
│       │   │   │   │   │   ├── index.ts
│       │   │   │   │   │   ├── mutation.ts
│       │   │   │   │   │   ├── observer.ts
│       │   │   │   │   │   ├── processed-node-manager.ts
│       │   │   │   │   │   ├── shadow-dom-manager.ts
│       │   │   │   │   │   └── stylesheet-manager.ts
│       │   │   │   │   ├── replay
│       │   │   │   │   │   ├── canvas
│       │   │   │   │   │   │   ├── 2d.ts
│       │   │   │   │   │   │   ├── deserialize-args.ts
│       │   │   │   │   │   │   ├── index.ts
│       │   │   │   │   │   │   └── webgl.ts
│       │   │   │   │   │   ├── dialog
│       │   │   │   │   │   │   └── index.ts
│       │   │   │   │   │   ├── media
│       │   │   │   │   │   │   └── index.ts
│       │   │   │   │   │   ├── styles
│       │   │   │   │   │   │   ├── inject-style.ts
│       │   │   │   │   │   │   └── style.css
│       │   │   │   │   │   ├── index.ts
│       │   │   │   │   │   ├── machine.ts
│       │   │   │   │   │   ├── smoothscroll.ts
│       │   │   │   │   │   └── timer.ts
│       │   │   │   │   ├── index.ts
│       │   │   │   │   ├── types.ts
│       │   │   │   │   └── utils.ts
│       │   │   │   ├── test
│       │   │   │   │   ├── __snapshots__
│       │   │   │   │   │   ├── integration.test.ts.snap
│       │   │   │   │   │   ├── record.test.ts.snap
│       │   │   │   │   │   └── replayer.test.ts.snap
│       │   │   │   │   ├── benchmark
│       │   │   │   │   │   ├── dom-mutation.test.ts
│       │   │   │   │   │   └── replay-fast-forward.test.ts
│       │   │   │   │   ├── e2e
│       │   │   │   │   │   ├── __image_snapshots__
│       │   │   │   │   │   │   ├── webgl-test-ts-test-e-2-e-webgl-test-ts-e-2-e-webgl-will-record-and-replay-a-webgl-image-1-snap.png
│       │   │   │   │   │   │   └── webgl-test-ts-test-e-2-e-webgl-test-ts-e-2-e-webgl-will-record-and-replay-a-webgl-square-1-snap.png
│       │   │   │   │   │   └── webgl.test.ts
│       │   │   │   │   ├── events
│       │   │   │   │   │   ├── adopted-style-sheet-modification.ts
│       │   │   │   │   │   ├── adopted-style-sheet.ts
│       │   │   │   │   │   ├── bad-style.ts
│       │   │   │   │   │   ├── bad-textarea.ts
│       │   │   │   │   │   ├── canvas-in-iframe.ts
│       │   │   │   │   │   ├── custom-element-define-class.ts
│       │   │   │   │   │   ├── dialog-playback.ts
│       │   │   │   │   │   ├── document-replacement.ts
│       │   │   │   │   │   ├── hover.ts
│       │   │   │   │   │   ├── iframe-shadowdom-hover.ts
│       │   │   │   │   │   ├── iframe.ts
│       │   │   │   │   │   ├── input.ts
│       │   │   │   │   │   ├── ordering.ts
│       │   │   │   │   │   ├── scroll-with-parent-styles.ts
│       │   │   │   │   │   ├── scroll.ts
│       │   │   │   │   │   ├── selection.ts
│       │   │   │   │   │   ├── shadow-dom.ts
│       │   │   │   │   │   ├── style-sheet-rule-events.ts
│       │   │   │   │   │   ├── style-sheet-text-mutation.ts
│       │   │   │   │   │   ├── video-playback-on-full-snapshot.ts
│       │   │   │   │   │   ├── video-playback.ts
│       │   │   │   │   │   └── webgl.ts
│       │   │   │   │   ├── html
│       │   │   │   │   │   ├── assets
│       │   │   │   │   │   │   ├── 1-minute-of-silence.mp3
│       │   │   │   │   │   │   ├── bunny-video.webm
│       │   │   │   │   │   │   ├── robot.png
│       │   │   │   │   │   │   ├── style.css
│       │   │   │   │   │   │   └── webgl-utils.js
│       │   │   │   │   │   ├── audio.html
│       │   │   │   │   │   ├── base64-image-compression.html
│       │   │   │   │   │   ├── benchmark-dom-mutation-add-and-move.html
│       │   │   │   │   │   ├── benchmark-dom-mutation-add-and-remove.html
│       │   │   │   │   │   ├── benchmark-dom-mutation-attributes.html
│       │   │   │   │   │   ├── benchmark-dom-mutation-deep-nested.html
│       │   │   │   │   │   ├── benchmark-dom-mutation-multiple-descendant-add.html
│       │   │   │   │   │   ├── benchmark-dom-mutation.html
│       │   │   │   │   │   ├── blank.html
│       │   │   │   │   │   ├── block.html
│       │   │   │   │   │   ├── blocked-unblocked.html
│       │   │   │   │   │   ├── canvas-webgl-image.html
│       │   │   │   │   │   ├── canvas-webgl-shader.html
│       │   │   │   │   │   ├── canvas-webgl-square.html
│       │   │   │   │   │   ├── canvas-webgl.html
│       │   │   │   │   │   ├── canvas.html
│       │   │   │   │   │   ├── dialog.html
│       │   │   │   │   │   ├── empty.html
│       │   │   │   │   │   ├── form.html
│       │   │   │   │   │   ├── frame-image-blob-url.html
│       │   │   │   │   │   ├── frame1.html
│       │   │   │   │   │   ├── frame2.html
│       │   │   │   │   │   ├── hello-world.html
│       │   │   │   │   │   ├── ignore.html
│       │   │   │   │   │   ├── image-blob-url.html
│       │   │   │   │   │   ├── link.html
│       │   │   │   │   │   ├── main.html
│       │   │   │   │   │   ├── mask-text.html
│       │   │   │   │   │   ├── move-node.html
│       │   │   │   │   │   ├── mutation-observer.html
│       │   │   │   │   │   ├── password.html
│       │   │   │   │   │   ├── polyfilled-shadowdom-mutation.html
│       │   │   │   │   │   ├── react-styled-components.html
│       │   │   │   │   │   ├── select2.html
│       │   │   │   │   │   ├── shadow-dom.html
│       │   │   │   │   │   ├── shuffle.html
│       │   │   │   │   │   └── video.html
│       │   │   │   │   ├── record
│       │   │   │   │   │   ├── __snapshots__
│       │   │   │   │   │   │   ├── cross-origin-iframes.test.ts.snap
│       │   │   │   │   │   │   ├── dialog.test.ts.snap
│       │   │   │   │   │   │   └── webgl.test.ts.snap
│       │   │   │   │   │   ├── canvas-context.test.ts
│       │   │   │   │   │   ├── canvas-manager.test.ts
│       │   │   │   │   │   ├── cross-origin-iframes.test.ts
│       │   │   │   │   │   ├── dialog.test.ts
│       │   │   │   │   │   ├── error-handler.test.ts
│       │   │   │   │   │   ├── memory-leaks.test.ts
│       │   │   │   │   │   ├── serialize-args.test.ts
│       │   │   │   │   │   ├── shadow-dom-manager.test.ts
│       │   │   │   │   │   ├── webgl.test.ts
│       │   │   │   │   │   └── webgpu.test.ts
│       │   │   │   │   ├── replay
│       │   │   │   │   │   ├── __image_snapshots__
│       │   │   │   │   │   │   ├── base64-image-compression-replay.png
│       │   │   │   │   │   │   ├── base64-image-replacement-with-stripes.png
│       │   │   │   │   │   │   ├── dialog-test-ts-test-replay-dialog-test-ts-dialog-closed-dialogs-show-nothing-1-snap.png
│       │   │   │   │   │   │   ├── dialog-test-ts-test-replay-dialog-test-ts-dialog-should-add-an-opened-dialog-with-show-modal-in-incremental-snapshot-alternative.png
│       │   │   │   │   │   │   ├── dialog-test-ts-test-replay-dialog-test-ts-dialog-should-add-an-opened-dialog-with-show-modal-in-incremental-snapshot.png
│       │   │   │   │   │   │   ├── dialog-test-ts-test-replay-dialog-test-ts-dialog-should-close-dialog-again-when-open-attribute-gets-removed.png
│       │   │   │   │   │   │   ├── dialog-test-ts-test-replay-dialog-test-ts-dialog-should-open-dialog-with-show-in-full-snapshot.png
│       │   │   │   │   │   │   ├── dialog-test-ts-test-replay-dialog-test-ts-dialog-should-open-dialog-with-show-modal-in-full-snapshot.png
│       │   │   │   │   │   │   ├── dialog-test-ts-test-replay-dialog-test-ts-dialog-should-open-dialog-with-show-modal.png
│       │   │   │   │   │   │   ├── dialog-test-ts-test-replay-dialog-test-ts-dialog-should-switch-between-show-and-show-modal.png
│       │   │   │   │   │   │   ├── dialog-test-ts-test-replay-dialog-test-ts-dialog-should-switch-between-show-modal-and-show.png
│       │   │   │   │   │   │   ├── dialog-test-ts-test-replay-dialog-test-ts-dialog-show-the-dialog-when-open-attribute-gets-added.png
│       │   │   │   │   │   │   ├── hover-test-ts-test-replay-hover-test-ts-replayer-hover-should-trigger-hover-on-mouse-down-1-snap.png
│       │   │   │   │   │   │   ├── video-test-ts-test-replay-video-test-ts-video-will-be-paused-when-the-player-wasnt-started-yet-1-snap.png
│       │   │   │   │   │   │   ├── video-test-ts-test-replay-video-test-ts-video-will-play-from-the-correct-moment-1-snap.png
│       │   │   │   │   │   │   ├── video-test-ts-test-replay-video-test-ts-video-will-seek-to-the-correct-moment-1-snap.png
│       │   │   │   │   │   │   ├── video-test-ts-test-replay-video-test-ts-video-will-seek-to-the-correct-moment-without-media-interaction-events-1-snap.png
│       │   │   │   │   │   │   └── webgl-test-ts-test-replay-webgl-test-ts-replayer-webgl-should-output-simple-webgl-object-1-snap.png
│       │   │   │   │   │   ├── 2d-mutation.test.ts
│       │   │   │   │   │   ├── base64-image-compression.test.ts
│       │   │   │   │   │   ├── deserialize-args.test.ts
│       │   │   │   │   │   ├── dialog.test.ts
│       │   │   │   │   │   ├── hover.test.ts
│       │   │   │   │   │   ├── memory-leaks.test.ts
│       │   │   │   │   │   ├── preload-all-images.test.ts
│       │   │   │   │   │   ├── video.test.ts
│       │   │   │   │   │   ├── webgl-mutation.test.ts
│       │   │   │   │   │   └── webgl.test.ts
│       │   │   │   │   ├── integration.test.ts
│       │   │   │   │   ├── machine.test.ts
│       │   │   │   │   ├── record.test.ts
│       │   │   │   │   ├── replayer.test.ts
│       │   │   │   │   ├── rrdom.test.ts
│       │   │   │   │   ├── util.test.ts
│       │   │   │   │   └── utils.ts
│       │   │   │   ├── .gitignore
│       │   │   │   ├── CHANGELOG.md
│       │   │   │   ├── README.md
│       │   │   │   ├── package.json
│       │   │   │   ├── rollup.config.js
│       │   │   │   ├── tsconfig.json
│       │   │   │   ├── vite.config.entries.js
│       │   │   │   ├── vite.config.js
│       │   │   │   └── vitest.config.ts
│       │   │   ├── rrweb-snapshot
│       │   │   │   ├── record
│       │   │   │   │   └── package.json
│       │   │   │   ├── replay
│       │   │   │   │   └── package.json
│       │   │   │   ├── src
│       │   │   │   │   ├── css.ts
│       │   │   │   │   ├── index.ts
│       │   │   │   │   ├── rebuild.ts
│       │   │   │   │   ├── record.ts
│       │   │   │   │   ├── replay.ts
│       │   │   │   │   ├── snapshot.ts
│       │   │   │   │   ├── types.ts
│       │   │   │   │   └── utils.ts
│       │   │   │   ├── test
│       │   │   │   │   ├── __snapshots__
│       │   │   │   │   │   ├── integration.test.ts.snap
│       │   │   │   │   │   └── rebuild.test.ts.snap
│       │   │   │   │   ├── alt-css
│       │   │   │   │   │   └── alt-style.css
│       │   │   │   │   ├── css
│       │   │   │   │   │   ├── benchmark.css
│       │   │   │   │   │   ├── style-with-import.css
│       │   │   │   │   │   └── style.css
│       │   │   │   │   ├── html
│       │   │   │   │   │   ├── about-mozilla.html
│       │   │   │   │   │   ├── background-clip-text.html
│       │   │   │   │   │   ├── base64-images.html
│       │   │   │   │   │   ├── basic.html
│       │   │   │   │   │   ├── block-element.html
│       │   │   │   │   │   ├── compat-mode.html
│       │   │   │   │   │   ├── cors-style-sheet.html
│       │   │   │   │   │   ├── dialog.html
│       │   │   │   │   │   ├── dynamic-stylesheet.html
│       │   │   │   │   │   ├── form-fields.html
│       │   │   │   │   │   ├── hover.html
│       │   │   │   │   │   ├── iframe-inner.html
│       │   │   │   │   │   ├── iframe.html
│       │   │   │   │   │   ├── invalid-attribute.html
│       │   │   │   │   │   ├── invalid-doctype.html
│       │   │   │   │   │   ├── invalid-tagname.html
│       │   │   │   │   │   ├── mask-text.html
│       │   │   │   │   │   ├── monkey-patched-elements.html
│       │   │   │   │   │   ├── picture-blob-in-frame.html
│       │   │   │   │   │   ├── picture-blob.html
│       │   │   │   │   │   ├── picture-in-frame.html
│       │   │   │   │   │   ├── picture-with-inline-onload.html
│       │   │   │   │   │   ├── picture.html
│       │   │   │   │   │   ├── preload.html
│       │   │   │   │   │   ├── shadow-dom.html
│       │   │   │   │   │   ├── svg.html
│       │   │   │   │   │   ├── video.html
│       │   │   │   │   │   ├── with-relative-res.html
│       │   │   │   │   │   ├── with-script.html
│       │   │   │   │   │   ├── with-style-sheet-with-import.html
│       │   │   │   │   │   └── with-style-sheet.html
│       │   │   │   │   ├── iframe-html
│       │   │   │   │   │   ├── frame1.html
│       │   │   │   │   │   ├── frame2.html
│       │   │   │   │   │   └── main.html
│       │   │   │   │   ├── images
│       │   │   │   │   │   ├── compat-bottom.png
│       │   │   │   │   │   ├── compat-top-left.png
│       │   │   │   │   │   ├── compat-top-right.png
│       │   │   │   │   │   ├── robot.png
│       │   │   │   │   │   ├── rrweb-favicon-20x20.png
│       │   │   │   │   │   └── symbol-defs.svg
│       │   │   │   │   ├── js
│       │   │   │   │   │   └── a.js
│       │   │   │   │   ├── css.test.ts
│       │   │   │   │   ├── integration.test.ts
│       │   │   │   │   ├── rebuild.test.ts
│       │   │   │   │   ├── snapshot.test.ts
│       │   │   │   │   ├── stringify-stylesheet.bench.ts
│       │   │   │   │   ├── utils.test.ts
│       │   │   │   │   └── utils.ts
│       │   │   │   ├── .gitignore
│       │   │   │   ├── CHANGELOG.md
│       │   │   │   ├── README.md
│       │   │   │   ├── jsr.json
│       │   │   │   ├── package.json
│       │   │   │   ├── tsconfig.json
│       │   │   │   ├── vite.config.js
│       │   │   │   └── vitest.config.ts
│       │   │   ├── types
│       │   │   │   ├── src
│       │   │   │   │   └── index.ts
│       │   │   │   ├── .gitignore
│       │   │   │   ├── CHANGELOG.md
│       │   │   │   ├── README.md
│       │   │   │   ├── package.json
│       │   │   │   ├── tsconfig.json
│       │   │   │   └── vite.config.js
│       │   │   ├── utils
│       │   │   │   ├── src
│       │   │   │   │   └── index.ts
│       │   │   │   ├── CHANGELOG.md
│       │   │   │   ├── Readme.md
│       │   │   │   ├── package.json
│       │   │   │   ├── tsconfig.json
│       │   │   │   └── vite.config.js
│       │   │   ├── tsconfig.base.json
│       │   │   ├── vite.config.default.ts
│       │   │   ├── vitest.config.ts
│       │   │   └── vitest.workspace.ts
│       │   ├── types
│       │   │   ├── src
│       │   │   │   ├── __tests__
│       │   │   │   │   ├── __snapshots__
│       │   │   │   │   │   └── config-snapshot.spec.ts.snap
│       │   │   │   │   ├── config-snapshot.spec.ts
│       │   │   │   │   └── posthog-interface.spec.ts
│       │   │   │   ├── capture-log.ts
│       │   │   │   ├── capture.ts
│       │   │   │   ├── common.ts
│       │   │   │   ├── feature-flags.ts
│       │   │   │   ├── index.ts
│       │   │   │   ├── posthog-config.ts
│       │   │   │   ├── posthog.ts
│       │   │   │   ├── request.ts
│       │   │   │   ├── segment.ts
│       │   │   │   ├── session-recording.ts
│       │   │   │   ├── survey.ts
│       │   │   │   ├── toolbar.ts
│       │   │   │   └── tree-shakeable.ts
│       │   │   ├── .gitignore
│       │   │   ├── CHANGELOG.md
│       │   │   ├── README.md
│       │   │   ├── jest.config.mjs
│       │   │   ├── package.json
│       │   │   ├── rslib.config.ts
│       │   │   ├── tsconfig.build.json
│       │   │   └── tsconfig.json
│       │   ├── web
│       │   │   ├── src
│       │   │   │   ├── context.ts
│       │   │   │   ├── index.ts
│       │   │   │   ├── patch.ts
│       │   │   │   ├── posthog-web.ts
│       │   │   │   ├── storage.ts
│       │   │   │   └── types.ts
│       │   │   ├── test
│       │   │   │   └── posthog-web.spec.ts
│       │   │   ├── .eslintrc.cjs
│       │   │   ├── .gitignore
│       │   │   ├── .prettierrc
│       │   │   ├── CHANGELOG.md
│       │   │   ├── README.md
│       │   │   ├── babel.config.js
│       │   │   ├── jest.config.js
│       │   │   ├── package.json
│       │   │   ├── rollup.config.mjs
│       │   │   └── tsconfig.json
│       │   └── webpack-plugin
│       │       ├── src
│       │       │   ├── config.ts
│       │       │   └── index.ts
│       │       ├── CHANGELOG.md
│       │       ├── README.md
│       │       ├── package.json
│       │       ├── rslib.config.mjs
│       │       └── tsconfig.json
│       └── playground
│           ├── flags
│           │   ├── .npmrc
│           │   ├── README.md
│           │   ├── evaluation-tags-example.html
│           │   ├── package.json
│           │   ├── pnpm-lock.yaml
│           │   ├── pnpm-workspace.yaml
│           │   └── remote-config-example.js
│           ├── nextjs
│           │   ├── bin
│           │   │   └── localdev.sh
│           │   ├── pages
│           │   │   ├── api
│           │   │   │   ├── auth
│           │   │   │   │   ├── login.ts
│           │   │   │   │   └── logout.ts
│           │   │   │   └── socket.ts
│           │   │   ├── replay-examples
│           │   │   │   ├── animations.tsx
│           │   │   │   ├── canvas.tsx
│           │   │   │   ├── iframe.tsx
│           │   │   │   ├── long.tsx
│           │   │   │   └── media.tsx
│           │   │   ├── _app.tsx
│           │   │   ├── _document.tsx
│           │   │   ├── autocapture.tsx
│           │   │   ├── chat.tsx
│           │   │   ├── ecommerce.tsx
│           │   │   ├── external_chat.tsx
│           │   │   ├── hogflix.tsx
│           │   │   ├── index.tsx
│           │   │   ├── product-tours.tsx
│           │   │   ├── survey.tsx
│           │   │   ├── tiktok-proxy.tsx
│           │   │   ├── toolbar-tests.tsx
│           │   │   └── ua.tsx
│           │   ├── src
│           │   │   ├── AuthModal.tsx
│           │   │   ├── CookieBanner.tsx
│           │   │   ├── Header.tsx
│           │   │   ├── SessionInteractions.tsx
│           │   │   ├── auth.ts
│           │   │   └── posthog.ts
│           │   ├── styles
│           │   │   └── globals.css
│           │   ├── .gitignore
│           │   ├── .npmrc
│           │   ├── .pnpmfile.cjs
│           │   ├── README.md
│           │   ├── next.config.mjs
│           │   ├── package.json
│           │   ├── pnpm-workspace.yaml
│           │   ├── postcss.config.mjs
│           │   ├── tailwind.config.mjs
│           │   ├── tsconfig.json
│           │   ├── turbo.json
│           │   └── vercel.json
│           ├── react-nextjs
│           │   ├── app
│           │   │   ├── EventDisplay.tsx
│           │   │   ├── globals.css
│           │   │   ├── layout.tsx
│           │   │   ├── page.tsx
│           │   │   └── providers.tsx
│           │   ├── .gitignore
│           │   ├── .npmrc
│           │   ├── README.md
│           │   ├── next.config.js
│           │   ├── package.json
│           │   ├── pnpm-workspace.yaml
│           │   └── tsconfig.json
│           ├── remix
│           │   ├── app
│           │   │   ├── components
│           │   │   │   └── Header.tsx
│           │   │   ├── routes
│           │   │   │   ├── _index.tsx
│           │   │   │   ├── media.tsx
│           │   │   │   └── ph-relay-xyz123.$.tsx
│           │   │   ├── EventDisplay.tsx
│           │   │   ├── providers.tsx
│           │   │   └── root.tsx
│           │   ├── bin
│           │   │   └── localdev.sh
│           │   ├── .gitignore
│           │   ├── .npmrc
│           │   ├── .pnpmfile.cjs
│           │   ├── README.md
│           │   ├── package.json
│           │   ├── pnpm-workspace.yaml
│           │   ├── tsconfig.json
│           │   ├── turbo.json
│           │   └── vite.config.ts
│           ├── rollup
│           │   ├── src
│           │   │   └── index.ts
│           │   ├── .gitignore
│           │   ├── .npmrc
│           │   ├── package.json
│           │   ├── pnpm-workspace.yaml
│           │   ├── rollup.config.mjs
│           │   └── tsconfig.json
│           ├── vite
│           │   ├── public
│           │   │   └── vite.svg
│           │   ├── src
│           │   │   ├── counter.ts
│           │   │   ├── main.ts
│           │   │   ├── style.css
│           │   │   └── typescript.svg
│           │   ├── .gitignore
│           │   ├── .npmrc
│           │   ├── index.html
│           │   ├── package.json
│           │   ├── pnpm-lock.yaml
│           │   ├── pnpm-workspace.yaml
│           │   ├── tsconfig.json
│           │   └── vite.config.ts
│           ├── webpack
│           │   ├── src
│           │   │   ├── nested
│           │   │   │   └── index.ts
│           │   │   └── index.ts
│           │   ├── .npmrc
│           │   ├── package.json
│           │   ├── pnpm-lock.yaml
│           │   ├── pnpm-workspace.yaml
│           │   ├── tsconfig.json
│           │   └── webpack.config.ts
│           └── .pnpmfile.cjs
├── references
├── scripts
└── SKILL.md
```