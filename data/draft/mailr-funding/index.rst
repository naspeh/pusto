Mailr
=====
**Open Source webmail client with gmail like conversations.**

I have been using Gmail during last seven years. I had tried to move away many times, but 
always returned back. I have tried probably all possible alternatives and no one can't fit 
for me as the best conversations making by Google.

Now many who trying to invent new generation of emails. There are services made by 
corporations like gmail.com, mail.yahoo.com, outlook,com, mailboxapp.com, mail.yandex.com 
and smaller companies with fastmail.fm, hashmail.com, inboxapp.com and some small open 
source teams like mailpile.is, Geary (desktop replacement for Gmail). And Mailr wants to 
be a good alternative for them.

The most similar to Mailr is Mailpile. They both Open Sourced, both web based and both 
using Python.

I think Mailpile has main principle **security**.

Mailr has main principle **simplicity**
 - simple, but flexible and useful interface
 - codebase with simplicity in mind (less dependencies, less code - means simpler for 
   supporting in the future)
 - simple way for installation and deployment

I started Mailr couple months ago and it has pretty well public demo with narrow feature 
set. I can read all my emails through Mailr interface and I really like it (sure, because 
I've been making it). I want to build the first powerful version in four months for 
replacing gmail in my daily using.

Why I think I can do this?
--------------------------
1. Right instruments

   **Python** is really right language. I love Python. It has powerful standard library 
   and lots of useful third party libraries (sqlalchemy, werkzeug, jinja2, lxml). Mailpile 
   and InboxApp both have been making with Python.

   **PosgresSQL** is right storage. It can be use with transactions, replication and 
   backups for saving my emails carefully. It has useful feature set for searching and 
   indexing, so I don't need invent wheel for these things.

2. Right way (for getting the first usable version as soon as possible)

    **Gmail** as first backend through IMAP with bidirectional synchronization. Gmail has 
    good storage for emails, filters for incoming messages, powerful spam filter, email 
    clients for smartphones and tablets. So I can concentrate on useful interface and 
    other thing can wait for later. And I always can return to Gmail again and use it as 
    usual or just use it in parallel mode.

    So with Gmail I can do most important features first and some can wait for later. I 
    can read emails through Mailr, next feature is writing emails. And I need to 
    implement, to optimize and to polish big set of features: conversations, search, 
    detecting and folding quotes, hotkeys, settings, themes, label handling, filtering of 
    incoming messages, SSL support and etc.

    Probably **Mailgun** as second backend. Setup and supporting my own email server with 
    good spam filter and good reliability is horrible thing. So services like Mailgun can 
    help me with this stuff.

    If I'd implement Mailgun and make good replication for my PosgreSQL I can remove 
    synchronization with Gmail (not from supporting, just from usage), that simplify and 
    speed Mailr installation, because synchronization part is complicated and sometimes 
    slow.

    And then other IMAP servers (so Mailr can be used with full own setup).

::

  I even make up quatrain
    With right instruments
    During right way
    You can get big resultants
    Not far away

So four months and two iterations (each in two months)
------------------------------------------------------
First iteration, named "I move away from Gmail but with Gmail behind my back":
 - composing and sending email
 - improving conversation with all possible actions
 - improving detecting and folding quotes and signatures
 - improving and optimizing synchronization through IMAP
 - preparing docker image and ansible playbook
 - preparing instructions for installation

After first iteration I suppose I will switch to Mailr in daily basis.

Second iteration, named "Really? I move away from Gmail!"
 - improving all optimization all existing features
 - improving themes and implementing new ones
 - filtering incoming messages
 - multi-accounts support
 - Mailgun support

After second iteration I suppose Mailr will be perfect alternative for webmail.

Why crowdfunding?
-----------------
I have family and I usually work as Python Developer on full-time position. Last year I 
have spend my time mostly on my own projects and Mailr is last one which I have been 
working maybe last four months, including researching and the first prototype which I left 
and start developing Mailr from scratch. Now I have spent mostly all the money which I 
have (I didn't earn anything during last year) and I need to get job. But I want to 
develop Mailr. Now I dive in context, I have enthusiasm and this is right time, because if 
I get job I will deep dive in new role and new project and Mailr can late for about year. 
So I really want to work on email stuff and I need some money.
