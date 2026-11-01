# E9 Design website: setup handoff

**For:** the Claude session that controls Patrick's browser (Claude in Chrome).
**From:** the Claude Code session that built the new e9design.net site.
**Owner:** Patrick Malloy, GitHub account `patrickjmalloy-commits`. The Netlify account is the same one that hosts the Revelance site (revelanceoh.com).

## What this is

A new static website for Emergency Nine Design (E9, design/build of golf entertainment spaces, Mason OH) has been built and is waiting to be published. Right now the code exists only inside a temporary cloud session. Your job is to set up GitHub and Netlify in the browser so the code can be pushed and published, using the same release process as the Revelance site:

- the `staging` branch publishes to a Netlify **staging** site, for review;
- the `main` branch publishes to the **live** site (e9design.net);
- `main` only changes when Patrick clicks **Approve** in GitHub.

## Rules for you (the browser agent)

1. **Patrick signs in himself.** Never type, guess or store passwords, 2FA codes or recovery codes. If a login or 2FA screen appears, stop and ask Patrick to complete it.
2. **Stop and ask before anything you can't undo**, or that isn't in this document: deleting a repo or site, changing DNS or nameservers, changing billing, or making a repo private or public after it has been created.
3. **Do not touch the Revelance site or the `revelance-site` repo.** Only work on the E9 items named here.
4. **Do not change DNS** (Part 5) unless Patrick is watching and has said yes in this chat. A DNS mistake can take down the site **and Patrick's E9 email**.
5. Screens change over time. If a button isn't where this document says, look for the closest match, and describe what you see instead of guessing.
6. At the end of each part, report back the exact values listed under **Report**.

---

## Part 1: Create the GitHub repository (browser, about 5 minutes)

1. Go to https://github.com/new (Patrick must already be signed in as `patrickjmalloy-commits`).
2. Fill in:
   - **Owner:** `patrickjmalloy-commits`
   - **Repository name:** `e9design-site`
   - **Description:** `E9 Design website (e9design.net)`
   - **Visibility: Public.** This is deliberate. The approval gate (step 6 below) needs "required reviewers", which free GitHub accounts only get on public repos. The Revelance repo is public for the same reason. The site's code holds no secrets.
   - **Leave every "Initialize" option OFF**: no README, no .gitignore, no license. The repo must be completely empty, or the push in Part 2 will be rejected.
3. Click **Create repository**.
4. Go to **Settings → Actions → General**. Under **Workflow permissions**, select **Read and write permissions** and click **Save**.
5. Go to **Settings → Environments → New environment**. Name it exactly `production` (lowercase) and click **Configure environment**.
6. Tick **Required reviewers**, add `patrickjmalloy-commits`, and click **Save protection rules**.
   - **This must be done before Part 2.** Without it, the first push would publish to the live site with no approval step.

**Report:** the repo URL, and confirm (yes/no) that the `production` environment exists with Patrick as required reviewer.

---

## Part 2: Push the code (Patrick, in the other session; not the browser)

Patrick goes back to the Claude Code session that built the site and says:

> The repo `patrickjmalloy-commits/e9design-site` is created and the production environment is set. Push the site.

That session will push the code to a `staging` branch. **Wait until it confirms the push before starting Part 3.**

The Actions tab will show a "Promote staging to production" run. It will pass its checks and then wait for approval. **Don't approve it yet**: the staging site doesn't exist until Part 3.

---

## Part 3: Netlify, two sites (browser, about 15 minutes)

Go to https://app.netlify.com. Patrick's team holds the Revelance sites; leave those alone.

### 3a. Check what already exists

Patrick says an E9 site already exists in this Netlify account. Search the site list for "e9", "emergency" or "e9design".

- **If you find one:** open it and note its name, its `*.netlify.app` address, whether it's connected to a Git repo (Site configuration → Build & deploy → Continuous deployment), and whether `e9design.net` is listed under Domain management. **Don't delete or change it yet.** Report what you found and ask Patrick whether to reuse it as the live site (3c) or create a new one.
- **If none exists:** continue below.

Note: e9design.net currently points to an old WordPress host (IP 66.96.162.129), not Netlify. Nothing in Parts 3–4 changes that, so the old site stays live until Part 5.

### 3b. Staging site (deploys the `staging` branch)

1. **Add new site → Import an existing project → GitHub.** If Netlify asks to install or configure its GitHub app, give it access to `e9design-site` (adding to the existing selection; don't remove `revelance-site`).
2. Pick `patrickjmalloy-commits/e9design-site`.
3. Settings:
   - **Branch to deploy:** `staging`
   - **Base directory:** empty
   - **Build command:** empty
   - **Publish directory:** `.` (the repo's `netlify.toml` already says this)
4. Deploy. Then **Site configuration → Change site name** to `e9design-staging`. If that name is taken, use `e9design-staging-oh` or similar.
5. **Forms:** go to **Forms** and click **Enable form detection** if that button appears, then **Deploys → Trigger deploy → Deploy site** once, so Netlify picks up the contact form.
6. **Keep staging out of Google:** this is handled in the site code. Nothing to do.

### 3c. Live site (deploys the `main` branch)

`main` doesn't exist yet. It's created the first time Patrick approves a release (Part 4). So:

- Do Part 4 first, then come back here.
- Then: **Add new site → Import an existing project → GitHub → e9design-site**, with **Branch to deploy: `main`** and the same empty build settings. (If Patrick chose in 3a to reuse the existing E9 site, link that site to the repo instead: Site configuration → Build & deploy → Link repository, branch `main`.)
- Rename it to `e9design` (or the closest available name).
- Enable form detection and redeploy, as in 3b step 5.
- **Form notifications:** Site configuration → Notifications → Emails and webhooks → **Add notification → Email notification** → event "New form submission". **Ask Patrick which inbox to use** — it must be one he actually reads today. Do NOT use info@ or support@e9design.net: those mailboxes are not set up.
- Do the same on the **staging** site, so test submissions from Part 4 reach Patrick too.

### 3d. Tell GitHub the staging address

1. In GitHub: `e9design-site` → **Settings → Secrets and variables → Actions → Variables tab → New repository variable**.
2. **Name:** `STAGING_URL`. **Value:** the staging site's full address with no trailing slash, e.g. `https://e9design-staging.netlify.app`.

**Report:** the staging URL, the live-site URL (`*.netlify.app`), and whether form detection is on for both.

---

## Part 4: Review and approve the first release (Patrick, about 5 minutes)

1. Patrick opens the staging URL and checks every page: Home, Services, Process, Showroom, Contact. He sends a test message through the contact form; it should land on a "Thanks" page and appear under Netlify → Forms.
2. In GitHub: `e9design-site` → **Actions** → latest **Promote staging to production** run. If it ran before `STAGING_URL` existed, click **Re-run all jobs** so the staging smoke test runs.
3. When it shows **Waiting for review**, click **Review deployments → tick production → Approve and deploy.** Only Patrick should click this.
4. The run creates the `main` branch. Now go back and finish **Part 3c**.

From then on, every change works this way: push to `staging` → check the staging site → approve in GitHub → live.

**Report:** that the run succeeded and `main` exists.

---

## Part 5: Point e9design.net at Netlify (browser, ONLY with Patrick watching)

**Risk:** e9design.net's DNS is at **Domain.com** (nameservers ns1/ns2.domain.com, checked Nov 1 2026). Its MX (email) records point to Domain.com mail servers (`m1.dnsix.com`, `mx.e9design.net`). Patrick believes no E9 mailboxes are in use, but leave all email-related records alone anyway: deleting them can't help the website and could break email set up later.

**Do this:**

1. DNS is managed at Domain.com (https://www.domain.com). Patrick signs in there.
2. Sign in to that DNS provider (Patrick signs in). **Screenshot or copy the full current DNS record list** before changing anything, and paste it into this chat. Pay special attention to MX and TXT records (email).
3. In Netlify, open the **live** site → **Domain management → Add a domain** → `e9design.net`. Netlify will offer:
   - **Netlify DNS (changing nameservers): do NOT pick this** unless Patrick explicitly agrees after you've shown him the email (MX) records. It moves all DNS to Netlify, and email breaks if MX records aren't recreated exactly.
   - **External DNS: pick this.** Netlify will show the exact records to add.
4. At the DNS provider, change **only** these records, using the values Netlify shows on screen (they're normally an A record for the bare domain pointing to Netlify's load-balancer IP, and a CNAME for `www` pointing to the site's `*.netlify.app` address):
   - `@` (bare domain) A record → the IP Netlify shows (replacing 66.96.162.129)
   - `www` → CNAME to the live site's `*.netlify.app` address
   - **Do not edit or delete MX, TXT, SPF, DKIM, or any other records** — including the `mx` host record (`mx.e9design.net`), which the email MX record points to.
5. Back in Netlify: under Domain management, make `e9design.net` the **primary domain**. Wait for **HTTPS / SSL certificate** to show as provisioned (minutes to a few hours), then make sure **Force HTTPS** is on.
6. Test: http://e9design.net, https://e9design.net and https://www.e9design.net should all end up on the new site at https://e9design.net. Old addresses like https://e9design.net/contact-us/ should redirect to the new pages.

**Leave the old WordPress hosting plan running for at least 30 days** after the switch, as a fallback. Cancelling it is Patrick's decision; check first whether the plan also includes the domain registration or email.

**Report:** the DNS records before and after, and SSL status.

---

## Part 6: Email forwarding for info@e9design.net (browser, with Patrick)

**Goal:** mail sent to `info@e9design.net` arrives in an inbox Patrick already reads. **Ask Patrick for the destination address**; never guess it. Forwarding only receives: replies will come from Patrick's own address. That's expected.

This part is independent of Part 5. It can be done before or after the website switch.

### 6a. Check Domain.com first (no DNS changes)

1. Patrick signs in at https://www.domain.com.
2. Open the e9design.net domain and look for **Email**, **Email Forwarding** or **Mailboxes**.
3. Report exactly what you see: whether forwarding is included free, needs a paid upgrade (and the price shown), or isn't offered. **Do not buy anything.** Patrick decides.
4. If free forwarding is included: create `info@e9design.net` → Patrick's destination address. Then skip to 6c.

### 6b. Otherwise, use ImprovMX (free plan)

1. Go to https://improvmx.com. Patrick creates the account himself (his email and password; don't fill them in).
2. Add domain `e9design.net`, and alias `info` → Patrick's destination address.
3. ImprovMX will show the DNS records it needs (normally two MX records and one SPF TXT record). **Use the exact values ImprovMX shows on screen.**
4. At Domain.com → DNS for e9design.net, **show Patrick the current records first** (copy them into this chat). Then:
   - **MX records:** delete the existing two (`m1.dnsix.com` and `mx.e9design.net`) and add the two ImprovMX MX records. Patrick has said no E9 mailboxes are in use, but confirm with him before deleting.
   - **SPF (TXT starting with `v=spf1`):** a domain may have only one SPF record. **Don't add a second one.** Edit the existing record and add ImprovMX's `include:` part to it, e.g. `v=spf1 include:spf.improvmx.com ip4:66.96.128.0/18 include:websitewelcome.com ~all`. (Use ImprovMX's include value if it differs.)
   - Leave the website records (`@`, `www`) and the `mx` host record alone.
5. Back in ImprovMX, click **Check again / Refresh** until the domain shows as verified. This can take from minutes to a few hours.

### 6c. Test

1. Patrick sends an email **from a different account** (e.g. a phone's other email app or a friend) to `info@e9design.net`. Forwarders often hide messages you send to yourself.
2. Confirm it arrives in the destination inbox (check spam too).

**Report:** which option was used, the DNS records before and after, and the test result. Then Patrick tells the Claude Code session "info@ forwarding works". It will put the address back on the website and can point form notifications to it.

---

## Afterwards (optional)

- **Google Search Console:** add the property `https://e9design.net` and submit `https://e9design.net/sitemap.xml`.
- **Google Analytics (GA4):** if Patrick wants it, create a GA4 property for e9design.net and give the **Measurement ID** (`G-XXXXXXXXXX`) to the Claude Code session. It will add the tracking code; phone and email click tracking is already built in and waiting.
- **Google Business Profile:** if E9 has one, update its website link to https://e9design.net.

## Quick reference

| Item | Value |
|---|---|
| GitHub repo | `patrickjmalloy-commits/e9design-site` (public) |
| Branches | `staging` (review), `main` (live; changed only by approval) |
| GitHub environment | `production`, required reviewer `patrickjmalloy-commits` |
| GitHub variable | `STAGING_URL` = staging site URL |
| Netlify staging site | `e9design-staging` → branch `staging` |
| Netlify live site | `e9design` → branch `main` → domain e9design.net |
| Build settings | leave the build command empty in the Netlify UI (netlify.toml supplies one that strips repo notes), publish directory `.` |
| Contact form | Netlify Forms, form name `contact`, notifications → an inbox Patrick reads (not info@/support@, which don't exist) |
| Old site | WordPress at 66.96.162.129; keep for 30 days after switch |
