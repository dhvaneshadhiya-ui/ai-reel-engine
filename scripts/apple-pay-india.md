# apple-pay-india — script + shot plan (editorial)

~95s @ HeyGen speed 1.05. ~300 words. Runtime band 60–120s (RULES.md §1).

## Corrections applied to the incoming brief

The brief listed five bullets. Two did not survive verification:

- **"Supports offline payments" — CUT.** No source supports it. See
  `explicitly_NOT_claimed` in the manifest.
- **"UPI support yet to be confirmed" — STRENGTHENED.** Reporting is more
  definite than that: UPI is *not* coming at launch, and the reason is
  specific (NPCI clearance + a sponsor bank). That absence became the reel's
  spine.
- **"Launching in October 2026" — REFRAMED as reporting.** Apple has confirmed
  nothing. The reel says so on camera rather than implying a confirmed date.

The unreported angle that became the payoff: the delay was a **fee fight** —
Apple wants 15–20 bps of interchange, banks countered at ~10, and it comes out
of bank revenue, not the customer's pocket.

## Script (as spoken)

Apple Pay is finally launching in India. Reportedly, by October. But the
biggest deal isn't that it's arriving. It's what it's arriving without.

Here's how it works. You add a Visa or Mastercard credit card to Apple Wallet.
Then you tap your iPhone, or your Apple Watch, on any contactless terminal.
That's it. Apple never sees your real card number. Your bank issues a device
specific number, and every tap uses a one time code.

Now, the part almost nobody noticed. There is no UPI. Not at launch. And
that's not an oversight. To route UPI payments, Apple needs clearance from the
NPCI, the body that runs UPI, plus a sponsor bank.

Which matters, because UPI is about eighty five percent of India's digital
payments. In May alone, twenty three point two billion transactions. Nearly
thirty trillion rupees. So Apple isn't taking on UPI. It's launching into the
slice UPI doesn't own. Premium credit cards.

But here's the real story. The hold up was never the technology. It was the
money. Apple has been negotiating with India's biggest banks for months. It
wants fifteen to twenty basis points of the interchange on every credit card
transaction. The banks countered at ten. And that fee doesn't come from you,
or from the shopkeeper. It comes out of the interchange the banks already earn.

One honest caveat. Apple has confirmed none of this. No date, no bank list, no
feature list. This is reporting.

So if you're waiting to replace your UPI app, keep waiting. But if you carry a
premium credit card, October could be interesting. Would you tap your watch
instead of scanning a QR code?

## Treatment split (why each source is used the way it is)

- **`apple-ad`** is live-action and photographic → survives a 9:16 centre crop
  → used **full-bleed** for the hook, the tap payoff and atmosphere.
- **`apple-support`** is device/UI motion graphics centred in 16:9 → a 9:16
  crop cuts card numbers and menu labels mid-word (verified on frames) → kept
  at **full 16:9 inside framed floatcards**, per the never-full-bleed-UI rule.
- Visa/Mastercard marks aren't on svgl → the networks are a **data-rendered
  specsheet**, not a mangled logo.
- NPCI's stats page 404s → UPI scale is a **rendered chart** from the
  NPCI-sourced figures, not a screenshot.

## Beat map

Every beat resolves to a manifest id, the avatar, or an MG component.
Validation gate: passed — no unbound beats. Exact durations come from whisper
word anchors at build time; see `tools/build_applepay.py`.

| # | anchor | visual |
|---|---|---|
| 1 | "launching in india" | MG:logoassemble Apple mark, cream |
| 2 | "by october" | `receipt-bt` |
| 3 | "isn't that it's arriving" | MG:split — `clip-ad-tap` top / face bottom |
| 4 | "arriving without" | `clip-ad-contactless` |
| 5 | "how it works" | `clip-su-logo` floatcard |
| 6 | "to apple wallet" | `clip-su-wallet` floatcard |
| 7 | "tap your iphone" | `clip-su-menu` floatcard |
| 8 | "apple watch" | `clip-su-watch` floatcard |
| 9 | "contactless terminal" | `clip-su-nfc` floatcard |
| 10 | "that's it" | `clip-ad-tap` full-bleed |
| 11 | "real card number" | avatar |
| 12 | "device specific number" | `clip-su-tap` floatcard |
| 13 | "one time code" | MG:specsheet — security model |
| 14 | "nobody noticed" | avatar |
| 15 | "not at launch" | MG:wordcascade — NO UPI |
| 16 | "not an oversight" | avatar |
| 17 | "sponsor bank" | MG:checklist — what UPI would require |
| 18 | "digital payments" | MG:chart — UPI 85% share |
| 19 | "billion transactions" | MG:chart — UPI May 2026 scale |
| 20 | "trillion rupees" | `clip-ad-store` |
| 21 | "taking on upi" | MG:specsheet — in / out at launch |
| 22 | "premium credit cards" | `clip-su-card` floatcard |
| 23 | "the real story" | avatar |
| 24 | "it was the money" | `clip-ad-counter` |
| 25 | "for months" | `receipt-bt` (second region) → replaced by MG if reused |
| 26 | "credit card transaction" | MG:chart — 15-20 bps vs 10 bps |
| 27 | "countered at ten" | MG:chart continues |
| 28 | "from the shopkeeper" | avatar |
| 29 | "banks already earn" | MG:specsheet — who pays |
| 30 | "confirmed none of this" | avatar |
| 31 | "no feature list" | MG:wordcascade — unconfirmed |
| 32 | "this is reporting" | `receipt-bt` |
| 33 | "keep waiting" | `clip-su-approved` floatcard |
| 34 | "could be interesting" | `clip-su-history` floatcard |
| 35 | "scanning a qr code" | avatar + CTA headline |
