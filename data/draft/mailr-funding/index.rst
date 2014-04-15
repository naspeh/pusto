Mailr
=====
.. epigraph::

    | With the right instruments
    | Folowing the right way
    | You can reach big results
    | Not so far away
    |
    | -- Grisha aka naspeh

**Open Source webmail client with Gmail like conversations.**

I love Open Source. I love emails.

These days many people are trying to invent a new generation of emails. There is a number of services made by 
corporations like gmail.com, mail.yahoo.com, outlook,com, mailboxapp.com, mail.yandex.com 
and smaller companies like fastmail.fm, hashmail.com, inboxapp.com and some small open 
source teams like mailpile.is, Geary (desktop email client with Gmail-like conversations). 
I think many webmails have too old interfaces, others are too complicated and some don't 
give me simple first trying with full functionality. I need something with simple and 
powerful web interface with some good innovations. And Mailr is intended to fit that and be a 
good alternative for other services with no ads and little privacy in the end.

I've been using Gmail during the last seven years. I tried to abandon many times, but 
always returned. I tried probably all possible alternatives and nothing could fit 
me as the best conversations made by Google.

I have several daily used devices: laptop with small screen for all my work, iPad Mini 
for reading and surfing. When I need only a browser for webmail that's amazing. So I 
want Mailr to be really suitable for small screens and for big monitors as well
(I have a big one for testing, but usually watch movies on it).

The most similar project to Mailr is Mailpile. They're both open sourced, both web based and both 
using Python. But they have different ways?????????.

I think the main principle of Mailpile is **security**.

The main principle of Mailr is **simplicity**.
 - simple, but flexible and useful interface
 - codebase created with simplicity in mind (less dependencies, less code - means simplier for 
   maintaining in the future)
 - simple installation and deployment

I started Mailr few months ago and it already has a pretty good `public demo`__ with narrow feature 
set. I can read all my emails through Mailr interface and I really like it (sure, because 
I've been making it). I want to build the first powerful version in **five months** for 
replacing Gmail in my daily using.

__ http://mail.pusto.org

Code is available on github__ and is first introduced here__ (it is still useful for additional 
information).

__ https://github.com/naspeh/mailr
__ http://pusto.org/en/mailr/

Why do I think I can do this?
-----------------------------
1. **Right instruments**

   **Python** is really the right language. I love Python. It has a powerful standard library 
   and lots of useful third party libraries, that give us the power. Mailpile and InboxApp 
   both have been made using Python.

   **PosgresSQL** is the right storage. It can be used with transactions, replications and 
   backups for saving my emails carefully. It has a useful feature set for searching and 
   indexing, so I don't need to reinvent the wheel for these things. All emails with attachments are in 
   the database, so just a simple backup and all my data is with me again.

   **Less** is used instead of CSS for better theming.

2. **Right way** (for getting the first usable version as soon as possible)

   **Gmail** is used as the first backend through IMAP with bidirectional synchronization.
   Gmail has a good storage for emails, filters for incoming messages, powerful spam filter, email 
   clients for smartphones and tablets. And I always can return to Gmail again and use it 
   as usual or just use it in parallel mode.

   So with Gmail I can do most important features first and some can wait. I can already
   read emails through Mailr, the next feature is writing emails. And I need to 
   implement, optimize, and polish a big set of features: conversations, email 
   parsing, synchronizing, search, detecting and folding quotes, hotkeys, settings, 
   themes, label handling, filtering of incoming messages, SSL support, etc.

   **Mailgun** will be used as the second backend. Setting up and supporting my own email server with good spam 
   filter and good reliability is a horrible thing. So services like Mailgun can help me 
   with this stuff.

   If I implement Mailgun and make good replication for my PosgreSQL I will be able to remove 
   synchronization with Gmail (not from supporting, just from usage)????????. That will simplify and 
   speed up Mailr installation, because synchronization part is always complicated and can be 
   slow sometimes.

   **Other IMAP servers** afterwards (so that Mailr could be used with my own full setup).

I need $15,000 for five months of my work
-----------------------------------------
I will work full-time on Mailr in two iterations (each in two and half months).

The first iteration named "I have moved away from Gmail but with Gmail behind my back":
 - composing and sending email
 - improving conversation with all important actions
 - improving and optimizing synchronization through IMAP
 - improving email parsing
 - improving detecting and folding quotes and signatures
 - improving database schema
 - preparing docker image and ansible playbook
 - preparing instructions for installation
 - publishing

After the first iteration I suppose I will switch to Mailr on daily basis.

Second iteration, named "Really, I have moved away from Gmail!"
 - improving and optimization of all existing features
 - improving themes and implementing new ones
 - filtering incoming messages
 - multi-account support (one tab for all email accounts)
 - Mailgun support
 - preparing some documentation
 - publishing

After the second iteration I expect Mailr to be a perfect alternative for webmail.

Who am I?
---------
My name is Grisha Kostyuk aka naspeh. My email is naspeh[at]gmail.com. I was born on
Apr 15, 1983. I'm a passionate programmer from Ukraine with experience of about seven years in 
web development, more than four last years with Python. I usually work as full-stack web 
developer on full-time position (often remote). My last job was about backend part only.

Why fundraiser?
---------------
Since last April I have spent my time mostly on my own projects (including my newborn first 
son) and Mailr is the last thing I have been working on during the recent four months, including 
research, first prototype (which I gave up) and start of developing Mailr from scratch 
(current version took about two months and half).

Now I have spent almost all the money I had (I haven't earnt anything since last April) 
and I need to get a job for supporting my family. But I want to develop Mailr. Now I'm 
deep in the context of Mailr, I have a lot of enthusiasm and this is the right time, because if I 
get a job I will dive deep in a new role and a new project and Mailr may be late for about 
year. So I really want to work on email stuff and I need some money.

Some examples of campaigns (will be removed before publishing)
--------------------------------------------------------------
- https://www.indiegogo.com/projects/mailpile-taking-e-mail-back

  Funding duration: August 03, 2013 - September 10, 2013 (11:59pm PT).

  | https://news.ycombinator.com/item?id=6152046
  | Mailpile: Lets take email back
  | 507 points by threedaymonk 8 months ago 234 comments
  | 2013-08-03T13:48:10.000Z

  | https://news.ycombinator.com/item?id=6243936
  | Mailpile taking e-mail back
  | 316 points by tim_hutton 8 months ago 151 comments
  | 2013-08-20T14:36:59.000Z

  | https://news.ycombinator.com/item?id=6333203
  | PayPal Freezes Mailpile Campaign Funds 507 points
  | 507 points by capgre 7 months ago 351 comments
  | 2013-09-05T10:20:21.000Z

- https://www.bountysource.com/teams/neovim/fundraiser

  | https://news.ycombinator.com/item?id=7449663
  | Bram Moolenaar responds to Neovim
  | 208 points by dviola 2 months ago 149 comments
  | 2014-02-23T21:26:12.000Z

  | https://news.ycombinator.com/item?id=7278214
  | Neovim  838 points by tarruda 2 months ago 367 comments
  | 2014-02-21T17:48:07.000Z

- https://www.bountysource.com/teams/rvm/fundraiser
