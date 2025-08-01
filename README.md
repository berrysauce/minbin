<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/berrysauce/minbin/refs/heads/main/templates/assets/img/logo-dark.webp">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/berrysauce/minbin/refs/heads/main/templates/assets/img/logo.webp">
  <img alt="minbin" src="https://raw.githubusercontent.com/berrysauce/minbin/refs/heads/main/templates/assets/img/logo-dark.webp" style="width: 150px; height: auto;"
>
</picture>
<br>

a minimal, ephemeral pastebin service.

<br>

[![CodeQL](https://github.com/berrysauce/minbin/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/berrysauce/minbin/actions/workflows/github-code-scanning/codeql)
[![Pylint](https://github.com/berrysauce/minbin/actions/workflows/pylint.yml/badge.svg)](https://github.com/berrysauce/minbin/actions/workflows/pylint.yml)
![Uptime](https://uptime.berrysauce.dev/api/badge/10/uptime)
![GitHub repo size](https://img.shields.io/github/repo-size/berrysauce/minbin)

<br>

minbin is a minimal, ephemeral pastebin service built with simplicity and privacy in mind. it's self-hostable, open source, and ideal for quick, temporary sharing of snippets, logs, or notes.

pastes expire automatically after 1 hour, or immediately after being viewed (optional). you can view pastes through a clean HTML interface or directly as raw plaintext. a QR code is generated for each paste to make sharing even easier.

**→ check it out at [minb.in](https://minb.in/)**

<br>

### features

- ⚡ minimal UI
- ⏱️ ephemeral pastes (1 hour or one-time view)
- 🌐 accessible via browser or HTTP POST
- 👀 view in browser or as raw text
- 📱 QR code generation for easy sharing
- 🏠 self-hostable

### how to use

1. go to [minb.in](https://minb.in/)
2. paste your text/snippet
3. publish to get a short URL and QR code
4. share the link (e.g. `https://minb.in/aB01`)
5. view it raw: `https://minb.in/raw/aB01`
6. paste expires after 1 hour or after viewing once

you can also use minbin from your command line:

```bash
# share a file
curl --data-binary @example.txt https://minb.in

# share a string
curl https://minb.in -d "hello from the terminal!"
```

### self-hosting

minbin can be self-hosted by deploying it as a Docker container [(see GitHub package registry)](https://github.com/berrysauce/minbin/pkgs/container/minbin) or by deploying it on [Railway](https://railway.com?referralCode=xKqS3I) *(referral link)*.

| Variable         | Description                           | Default            |
| ---------------- | ------------------------------------- | ------------------ |
| `APP_DOMAIN`     | public domain used in generated links | `minb.in`          |
| `DB_HOST`        | redis hostname or container name      | `dragonfly`        |
| `DB_PORT`        | redis port                            | `6379`             |
| `DB_USER`        | redis username (if using Redis ACL)   | *(optional)*       |
| `DB_PASS`        | redis password                        | *(optional)*       |
| `PASTE_EXPIRY`   | paste expiration time in **minutes**  | `60` (1 hour)      |
| `MAX_PASTE_SIZE` | maximum paste size in **bytes**       | `26214400` (25 MB) |

you can override these by passing them into Docker or setting them in your hosting environment. the standard configuration uses [DragonflyDB](https://www.dragonflydb.io/docs/getting-started) for the database, but any Redis-compatible database should do. 

### license

```txt
minbin – a minimal, ephemeral pastebin service
Copyright (C) 2025 Paul Haedrich

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses/.
```
