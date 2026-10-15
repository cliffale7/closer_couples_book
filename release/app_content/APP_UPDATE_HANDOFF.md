# App update handoff

1. Use the newest `The_Closer_Project_Content_*.zip` whose manifest names the source commit you intend to import.
2. Compare `manifest.json` file hashes with the bundle already in the app. `CHANGES.json` is the same comparison when a previous zip was supplied. An `initial` baseline is the first bundle, not a later diff.
3. Import changed activities, prompts, and assets. Do not rewrite stored journal answers. Tombstoned prompt ids stay in the registry so old answers keep their question.
4. If `requires_app_update` is true, the activity has cards or a covered key. Ship app code before treating that activity as playable in the app. Prose remains in the bundle either way.
5. A schema other than `closer-content/1` should be refused, leaving the previous bundle and every journal entry in place.
6. This package contains public book text only. On-device import is not tested in the book project.
