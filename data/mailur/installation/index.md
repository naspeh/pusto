# Installation
The easiest way to install Mailur is to run [bin/install][install] script.

Replace `example.com` everywhere with name of your server.

**Pre-requirements:** a server or [LXC container][run-lxc] with `CentOS 7.`
**Default username and password:** demo / demo

```bash
# prepare code
yum install -y git
git clone https://github.com/naspeh/mailur.git /opt/mailur
cd /opt/mailur

# run script
bin/install
```

Open `http://example.com:5000` in the browser.

[install]: https://github.com/naspeh/mailur/blob/master/bin/install
[run-lxc]: https://github.com/naspeh/mailur/blob/master/bin/run-lxc

## Customization
Change config in `bin/env` that looks like:
```bash
#!/bin/sh
# used for creation of virtual mailboxes
# use a space separator for multiple users
user=demo

# comment next line if you modify "/etc/dovecot/passwd.users"
pass={plain}demo

# used in "bin/deploy" for nginx and certbot
domain=example.com

secret=5969dd9f462f403b8a2866f6d79fa399

export MLR_SECRET=$secret
export MLR_MASTER=root:$secret
export MLR_SIEVE=sieve:$secret
export MLR_IMAP_OFF=''
```
and run `bin/install` again, it's safe to run multiple times.

## Deploy with https
Ensure proper `$domain` is set in `bin/env.`

Run `bin/deploy`. It will deploy all stuff behind nginx with free SSL certificate from [Let's Encrypt.](https://letsencrypt.org/)

Open `https://example.com` in the browser.

`IMAPS` will be available on server too.

## Import email from Gmail
**Note:** If you want use it without Gmail, you should deliver emails to `/home/vmail/demo/mlr` mailbox. In the future, it would be possible to import from other IMAP servers as well.

I use two-factor authentication for Gmail with [app password](https://support.google.com/accounts/answer/185833?hl=en) for Mailur.
```bash
. bin/activate
mlr gmail demo set {gmail-username} {gmail-password}
mlr gmail demo --parse
# and install systemd service
user=demo bin/install-idle-sync
```

## Master-master replication

I use two servers with master-master replication enabled.

For that for each user you should add `userdb_mail_replica` parameter with your second server in `/etc/dovecot/passwd.users` like:
```
demo:{plain}demo::::::userdb_mail_replica=tcps:replica.example.com
```
