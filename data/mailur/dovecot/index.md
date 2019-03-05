# Dovecot as main storage

When I posted the ["Alpha" (postgres based) version][alpha], it was [a good conversation on Reddit][reddit]. I was thinking about IMAP support after that. I didn't want to write my own IMAP server, so I started to look closer to [Dovecot][dovecot]. After first investigation I had an idea that probably I can use Dovecot as main storage, because I didn't want to duplicate emails over Dovecot and Postgres anyway. At summer 2017 I had a chance to evaluate the idea, after some period of deep work I got [a first Dovecot based prototype][gh9] and confidence that I can build a great webmail based on it.

[alpha]: /mailur/alpha/
[reddit]: http://redd.it/3t07mv
[gh9]: https://github.com/naspeh/mailur/issues/9
[dovecot]: https://www.dovecot.org/

#### The hardest things to deal with:
- unusual storage (limited IMAP instead of well known and powerful SQL)
- IMAP folders instead of tags
- I needed proper threads with ability to link them together

#### But at the same time it gives great features:
- already a part of mail stack (often used in home-grown setup)
- simple immutable storage, designed exactly for emails
- a bunch of email related plugins and integrations
- master-master replication

After trying few different approaches for hardest things I got pretty flexible storage.

## The current storage
IMAP keywords are used for system tags (like `#inbox`, `#spam` and `#trash`) and user-defined tags.

Just four IMAP folders for:
1. all original messages (no separate folder for Inbox, Spam or Trash)
2. all parsed messages for effective web representation
3. useful metadata (settings, linked threads, cache, etc.)
4. cleaned messages from `#spam` and `#trash` (autoexpunge in 30 days)

The most sensitive data is a folder with original messages and settings, parsed messages and metadata can be regenerated. [Dovecot ACL][dovecot-acl] is used to deny mailbox operations, expunging messages, etc. I use Dovecot's own high-performance mailbox format [single-dbox][dovecot-sdbox], so emails are never changed even during applying IMAP flags on them.

As for now, I don't rely on Gmail as storage anymore, so the Dovecot mailboxes are only source of truth, so I should be really careful with them. I use two servers from two different datacenters with [master-master replication][dovecot-replication] enabled, so far it has been working pretty well.

[dovecot-acl]: https://wiki2.dovecot.org/ACL
[dovecot-sdbox]: https://wiki2.dovecot.org/MailboxFormat/dbox
[dovecot-replication]: https://wiki.dovecot.org/Replication

From time to time, I want to check Inbox on mobile, so it has limited "general" IMAP support using [Dovecot virtual mailboxes][dovecot-virtual] and filtering by `#inbox`, `#spam` and `#trash` tags. I use it with [FairEmail for Android][fairemail] for fast notifications. Mailur also has a basic mobile view.

[dovecot-virtual]: https://wiki.dovecot.org/Plugins/Virtual
[fairemail]: https://email.faircode.eu/

As I have only one IMAP folder with all messages, it works pretty well with [Sieve scripts][sieve-rfc] using [IMAP FILTER=SIEVE][sieve-imap], because I don't need to move messages around and just mark them with a proper flag. Also it's easy to run them through all messages (available from UI).

[sieve-rfc]: https://tools.ietf.org/html/rfc5228
[sieve-imap]: https://wiki2.dovecot.org/Pigeonhole/Sieve/Plugins/IMAPFilterSieve

I use [Dovecot Lucene][dovecot-fts-lucene] for full text search indexing and it works pretty well for me.

[dovecot-fts-lucene]: https://wiki2.dovecot.org/Plugins/FTS/Lucene

## In conclusion
I like the current storage and I think it should be pretty stable from that point. It has good flexibility in storing different metadata. Metadata can change over time with new features, but as I said before metadata can be easily regenerated, so it shouldn't be a problem.

I think I'm pretty close to my initial goal to move away from Gmail. Even I still use Gmail as a transport (importing over IMAP and sending over SMTP), but I already can remove emails from Google and I'll do this soon. 
