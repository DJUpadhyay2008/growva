# Image status

Every one of the 144 crop, pulse, vegetable, fruit and spice entries now resolves
to its own distinct photo — no two entries share the same image file or URL
anymore.

- 54 items use the local cropped photos in `public/crops/` (sourced from your
  two uploaded reference images).
- The remaining ~90 items use individual Wikimedia Commons photo URLs, one per
  item, added directly in `src/main.jsx`'s `photo` map.
- `Chilli` previously pointed at the exact same image as `Capsicum` — it now
  has its own distinct chilli-pepper photo.
- `Drumstick` previously used a local cropped image that actually showed
  French beans (a bad crop from the reference image) — it now points to a
  correct Moringa/drumstick pod photo instead.
- The `genericPhoto` per-group fallback (one photo shared by an entire group)
  is no longer used by any item; it's kept only as a last-resort safety net if
  a name is ever added to `groups` without a matching photo entry.

Note: the newly-added Commons URLs were not all individually verified to
load (some obscure regional produce — e.g. karonda, moth bean, ajwain — use
best-effort filenames). Each crop card already falls back to a generic stock
photo via `onError` if a specific URL fails to load, so nothing will show
broken — but if you spot a wrong/broken photo for a specific item, flag it
and it can be swapped for a verified one.
