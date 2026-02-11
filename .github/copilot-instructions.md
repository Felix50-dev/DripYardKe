## Purpose

This file gives succinct, repo-specific guidance for AI coding assistants (GitHub Copilot-style agents) to be immediately productive in DripYardKe.

Follow these actionable constraints: prefer edits that are minimal, compile-clean, and follow the project's patterns (Kotlin + Jetpack Compose Android app + Python Firebase functions).

## Big picture (high level)

- Two main parts:
  - Android app (Kotlin + Jetpack Compose) in `app/`.
    - Key build file: `app/build.gradle.kts` (Compose, Kotlin, Firebase SDKs, JVM target 11).
    - Namespace: `com.coperative.dripyardke`; launcher `MainActivity` declared in `app/src/main/AndroidManifest.xml`.
  - Serverless functions in `user/` (Python, uses `firebase_admin` and GCP functions). Example: `user/main.py` defines `create_cashier` which checks `users` collection role == `ADMIN`.

Integration points: Firebase (google-services.json), Firestore, Auth, Storage, Cloud Functions. See `firebase.json` and `google-services.json` at repo root / `app/`.

Versioning & plugins

- Centralized version catalog: `gradle/libs.versions.toml` (use `libs` aliases as seen in `app/build.gradle.kts`).
- Kotlin jvmTarget = 11. Compile SDK = 36. Min SDK = 24.

Developer workflows (run these from repo root using the Gradle wrapper)

- Build debug APK: `./gradlew assembleDebug`
- Run unit tests: `./gradlew test` (or `./gradlew testDebugUnitTest` for module-specific runs)
- Run instrumentation tests on a connected device/emulator: `./gradlew connectedAndroidTest`
- Lint and static analysis: `./gradlew lint` and `./gradlew detekt`
- Produce release AAB/APK (careful: minify/proguard enabled in `release`): `./gradlew assembleRelease`

Firebase functions (python) — local/dev notes

- Functions live in `user/` (Python). They use `firebase_admin` and interact with Firestore and Auth.
- Assumption: functions are deployed to Google Cloud Functions / Firebase Functions separately from the Android build. Possible commands:
  - Local emulation (if `firebase.json` config exists): `firebase emulators:start --only functions,firestore,auth,storage`
  - Deploy (if configured): `firebase deploy --only functions` or use `gcloud functions deploy` for Python functions. Confirm `firebase.json` and function config before deploying.

Project-specific patterns & conventions (do not deviate)

- Use the version catalog `libs` for dependencies (do not hardcode versions in module build files).
- Compose + Material3 is the UI system. Prefer Compose idioms for UI changes (look under `app/src/main/java` for examples).
- Firebase data model: `users` collection stores `role` (e.g., `ADMIN`, `CASHIER`) and `shopId`. Server-side functions enforce role checks (see `user/main.py:create_cashier`). When modifying auth/roles, update both mobile client logic and server functions.
- Release builds enable R8/ProGuard; update `proguard-rules.pro` when adding reflective or serialized types.

Safety checks and quick validation for PRs

- Run `./gradlew assembleDebug` and `./gradlew lint` before creating a PR.
- Run unit tests and detekt: `./gradlew test` && `./gradlew detekt`.
- If you changed Android resources, ensure `./gradlew :app:mergeDebugResources` runs clean.

Examples to copy/paste when editing

- Role check in Python functions (from `user/main.py`):

  ```py
  admin_doc = db.collection("users").document(admin_uid).get()
  if not admin_doc.exists or admin_doc.get("role") != "ADMIN":
      raise ...
  ```

- Gradle/Kotlin compile options in `app/build.gradle.kts` to preserve:
  - `kotlinOptions { jvmTarget = "11" }`

Where to look for more context

- `app/build.gradle.kts` — main Android module build rules and dependencies
- `settings.gradle.kts` — included modules
- `gradle/libs.versions.toml` — dependency versions and plugin aliases
- `app/src/main/AndroidManifest.xml` — entry activity and app metadata
- `user/main.py` — Python cloud functions and Firestore/auth patterns
- `firebase.json` and `google-services.json` — Firebase integration and emulator/deploy config

Editing policy for AI changes

- Keep edits minimal and localized; prefer small PRs. If adding new dependency, update the version catalog and justify in PR description.
- When editing Kotlin/Android code, ensure the project still builds (`./gradlew assembleDebug`) and run `./gradlew detekt` if code style changed.
- For Python functions, include requirements in `user/requirements.txt` (if present) and validate with a quick unit test or emulator run.

If anything here is unclear or you want the file to emphasize other areas (CI, release process, emulator usage, or Cloud Build), tell me which sections to expand and I will iterate.
