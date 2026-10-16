# First MVQUEEN organic post batch

Updated October 16, 2026. **Three approved concepts are scheduled as nine automatic publications.** The owner approved the reviewed batch and proposed dates with “Let's publish.” Readback confirmed `draft=false`, `autoPublish=true`, the approved date/time, exact caption, destination network, media and alt text for every post. Instagram's network-specific automatic publication flag is enabled. Opening a planner link requires the owner's Metricool login.

The [schedule confirmation](schedule-confirmation.json) is the current record. The [original manifest](manifest.json) preserves the October 15 draft state and source media as historical evidence. Metricool assigns a new numeric ID when updating a post; UUIDs and planner links stayed the same. Scheduling is verified; successful live publication is not yet verified.

| Concept | Format | Open scheduled posts |
| --- | --- | --- |
| Meet MVQUEEN | Two-photo introduction | [Instagram](https://app.metricool.com/planner/calendar?blogId=7444403&openWithPostUuid=-1238410331914154915) · [Facebook](https://app.metricool.com/planner/calendar?blogId=7444403&openWithPostUuid=8609468006227987613) · [TikTok](https://app.metricool.com/planner/calendar?blogId=7444403&openWithPostUuid=658950530451129899) |
| Three colours. Your Arrival. | Three-photo fashion carousel | [Instagram](https://app.metricool.com/planner/calendar?blogId=7444403&openWithPostUuid=-8122033815735219509) · [Facebook](https://app.metricool.com/planner/calendar?blogId=7444403&openWithPostUuid=1756643130536771979) · [TikTok](https://app.metricool.com/planner/calendar?blogId=7444403&openWithPostUuid=-338252118756995964) |
| A place to get ready | Single-photo beauty-tool feature | [Instagram](https://app.metricool.com/planner/calendar?blogId=7444403&openWithPostUuid=1032837069329485744) · [Facebook](https://app.metricool.com/planner/calendar?blogId=7444403&openWithPostUuid=-7941925482282529323) · [TikTok](https://app.metricool.com/planner/calendar?blogId=7444403&openWithPostUuid=2030558057445803801) |

Destinations: Facebook **Mvqueen**, Instagram **@miss.mvqueen**, TikTok **@mvqueen_official**. These posts form a smaller initial batch; the existing 30-day calendar remains a separate production plan.

## Approved schedule

| Concept | Date | Time | Destinations |
| --- | --- | --- | --- |
| Meet MVQUEEN | October 17, 2026 | 12:00 noon America/New_York (16:00 UTC) | Facebook, Instagram, TikTok |
| Three colours. Your Arrival. | October 19, 2026 | 12:00 noon America/New_York (16:00 UTC) | Facebook, Instagram, TikTok |
| A place to get ready | October 21, 2026 | 12:00 noon America/New_York (16:00 UTC) | Facebook, Instagram, TikTok |

These approved dates replace the original October 16, 18 and 20 draft placeholders. Account identities, timezone and product availability were rechecked before scheduling. All nine updates were accepted. Each successful destination publication consumes one publication under Metricool's current counting rules. Verify each live post URL and publication status after its scheduled time. The scheduler timezone does not establish the owner's business country or target market.

## Product and media verification

- **Arrival Plus Size Dress**, product `9100061343942`: the public [product page](https://tsucu0-1i.myshopify.com/products/womens-solid-color-plus-size-dress) returned HTTP 200, and the public product data reported the white, red and dark-blue variants available. All three selected original catalogue photos match those colours. Styling accessories visible in the photographs are not described as included.
- **Anywhere Mirror Foldable LED Makeup Mirror**, product `9100794429638`: the public [product page](https://tsucu0-1i.myshopify.com/products/portable-foldable-led-makeup-mirror-with-built-in-lights) returned HTTP 200 and the public product data reported availability. The catalogue supports the foldable mirror, LED lighting and three light tones. The selected original photo shows the black variant without promotional text overlays.
- The public [MVQUEEN brand page](https://tsucu0-1i.myshopify.com/pages/mvqueen) returned HTTP 200. Facebook captions use this page or the specific product page with distinct organic campaign UTM parameters.
- Instagram and TikTok use follow/save/discussion prompts because their profile website fields have not been verified. No unsupported shipping promises, discounts, popularity, health or performance claims were added.
- Facebook and Instagram use original 1350-square dress photos and the original 800-square mirror photo. TikTok uses Shopify CDN `width=1080` versions of the dress photos, verified as 1080×1080 JPEGs; the 800-square mirror photo is unchanged. Captions and alt text match the selected media. No generated product imagery or music was added.

Availability is a point-in-time check. Catalogue presence does not independently document supplier image licensing. No order, charge, ad campaign, paid upgrade or public theme publication was performed for this batch.

## Verification and references

Each create and update operation was followed by a planner readback. The final readback contains nine unique concept/network combinations with two images for each introduction, three for each dress feature and one for each mirror feature. Captions and media are unchanged from the reviewed batch. Provider status is `PENDING`, with `draft=false` and `autoPublish=true`, confirming these are scheduled posts awaiting publication. TikTok retains `PUBLIC_TO_EVERYONE` privacy and the own-brand commercial disclosure.

The first update was rejected because the read response included an inactive `twitterData` section. Readback confirmed no change. Removing only inactive network sections, as required by Metricool's update schema, allowed the corrected update. No duplicate posts were created. The schedule record preserves the new numeric IDs and stable UUIDs without account-owner personal fields.

The review page was checked at desktop and 390px/320px mobile widths: all captions, images, platform tabs, carousel controls and copy fallback passed, with no overflow or JavaScript errors. Direct `file://` navigation was blocked by the managed browser; local HTTP preview was used for rendering checks.

- [Metricool draft API guidance](https://help.metricool.com/basic-guide-for-api-integration-r97af)
- [TikTok photo and video scheduling](https://help.metricool.com/schedule-and-post-on-tiktok-bkepi)
- [Media publishing requirements](https://help.metricool.com/publishing-requirements-for-images-and-videos-from-metricool-vfc8n)
- [Account and connection record](../SETUP_AND_CONNECTIONS.md)
- [Remaining launch checks](../../../PRODUCTION_READINESS/LAUNCH_COMPLETION_PLAN_2026-10-14.md)
