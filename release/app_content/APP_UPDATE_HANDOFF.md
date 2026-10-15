# App update handoff

1. Use the newest `The_Closer_Project_Content_*.zip` whose manifest names the source commit you intend to import.
2. Compare `manifest.json` file hashes with the bundle already in the app.
3. Import changed activities, prompts, and assets. Do not rewrite stored journal answers.
4. If `requires_app_update` is true on an activity, ship an app change before relying on that activity's new interaction.
5. A schema other than `closer-content/1` should be refused, leaving the previous bundle and every journal entry in place.
6. This package contains public book text only.
